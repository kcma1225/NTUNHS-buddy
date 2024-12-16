from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import re


# MongoDB 連接設置
def connect_to_mongodb():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        print("成功連接到 MongoDB")
        return client
    except Exception as e:
        print(f"無法連接到 MongoDB: {str(e)}")
        raise HTTPException(status_code=500, detail=f"無法連接到 MongoDB: {str(e)}")

# 初始化 FastAPI 應用
app = FastAPI()

# 連接到 MongoDB
client = connect_to_mongodb()
db = client["output_database"]

# 定義請求模型
class SearchRequest(BaseModel):
    education_types: list = None  # 學制可多選，預設為 None
    departments: list = None  # 系所可多選，預設為 None
    semesters: list = None  # 學期可多選，預設為 ["1132"]
    grades: list = None  # 年級可多選，預設為 ["1", "2", "3", "4"]
    course_types: list = None  # 課別可多選，預設為 None
    course_categories: list = None  # 課程內容分類可多選，默認略過
    weekdays: list = None  # 星期可多選，預設為 ["1", "2", ..., "7"]
    class_periods: list = None  # 節次可多選，預設為 ["1", "2", ..., "14"]
    keyword: str = None
# 提供所有學制
@app.get("/education-types")
async def get_education_types():
    """
    獲取所有學制（MongoDB 的 Collection 名稱）。
    """
    try:
        collections = db.list_collection_names()
        return {"education_types": sorted(collections)}  # 對學制名稱進行排序
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"無法獲取學制清單: {str(e)}")



# 提供指定學制中的系所
@app.post("/departments")
async def get_departments(request: dict):
    """
    根據學制獲取系所清單。
    """
    education_types = request.get("education_types", [])
    try:
        departments = set()
        for collection_name in education_types:
            if collection_name in db.list_collection_names():
                collection = db[collection_name]
                distinct_departments = collection.distinct("系所")
                departments.update(distinct_departments)

        return {"departments": sorted(list(departments))}  # 按字母順序排序
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"無法獲取系所清單: {str(e)}")




# 搜索 API
@app.post("/search")
async def search_data(request: SearchRequest):
    """
    搜索 API，支持學制、系所、學期、年級、星期和節次的多層級選擇。
    """
    education_types = request.education_types or db.list_collection_names()  # 預設為所有學制
    departments = request.departments or []
    semesters = request.semesters or ["1132"]  # 預設為 1132
    grades = request.grades or ["1", "2", "3", "4"]  # 預設為所有年級
    course_types = request.course_types or []  # 預設為全部課別
    
    course_categories = request.course_categories if request.course_categories else [
    "跨校", "跨域課程", "全英語授課", "EMI全英語授課",
    "同步遠距教學", "非同步遠距教學", "混合式遠距教學",
    "遠距教學課程", "遠距輔助課程", "無"
    ]


    weekdays = request.weekdays or ["1", "2", "3", "4", "5", "6", "7"]  # 預設為星期 1-7
    class_periods = request.class_periods or [str(i) for i in range(1, 15)]  # 預設為節次 1-14
    
    
    try:
        results = []
        for collection_name in education_types:
            if collection_name not in db.list_collection_names():
                continue

            collection = db[collection_name]
            query = {"$and": []}

            # 加入系所條件
            if departments:
                query["$and"].append({"系所": {"$in": departments}})

            # 加入學期條件
            if semesters:
                query["$and"].append({"學期": {"$in": semesters}})

            # 加入年級條件
            if grades:
                query["$and"].append({"年級": {"$in": grades}})

            # 加入課別條件
            if course_types:
                query["$and"].append({"課別": {"$in": course_types}})

            # 加入課程內容分類條件（僅當提供時）
            if course_categories:
                query["$and"].append({"課程內容分類": {"$in": course_categories}})
      


            # 加入星期條件
            if weekdays:
                query["$and"].append({"星期": {"$in": weekdays}})

            # 加入節次條件
            if class_periods:
                query["$and"].append({
                    "$expr": {
                        "$and": [
                            {"$setIsSubset": [{"$split": ["$節次", ","]}, class_periods]},  # 節次必須全部在選擇中
                            {"$ne": [{"$size": {"$split": ["$節次", ","]}}, len(class_periods)]}  # 不允許多餘的節次
                        ]
                    }
                })



            # 查詢數據
            cursor = collection.find(query)
            for document in cursor:
                document["_id"] = str(document["_id"])  # ObjectId 字符串化
                results.append(document)

        return {"results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢失敗: {str(e)}")
