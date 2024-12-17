import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

# MongoDB 連接設置
def connect_to_mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    print("成功連接到 MongoDB")
    return client

# 初始化 FastAPI 應用
app = FastAPI()

# 連接到 MongoDB
client = connect_to_mongodb()
db = client["output_database"]

# 維護學期選項的集合
semester_collection = db["semesters"]

# 定義最大學期數量
MAX_SEMESTERS = 4

# 定義新學期導入處理
def add_new_semester(new_semester):
    try:
        # 檢查新學期是否已存在
        if semester_collection.find_one({"semester": new_semester}):
            print(f"學期 {new_semester} 已存在，無需新增。")
            return

        # 插入新學期
        semester_collection.insert_one({"semester": new_semester})
        print(f"新增學期: {new_semester}")

        # 確保學期數量不超過 MAX_SEMESTERS
        all_semesters = list(semester_collection.find().sort("_id", 1))
        if len(all_semesters) > MAX_SEMESTERS:
            oldest_semester = all_semesters[0]["semester"]
            semester_collection.delete_one({"semester": oldest_semester})
            print(f"刪除最舊學期: {oldest_semester}")

    except Exception as e:
        print(f"無法處理新學期 {new_semester}: {str(e)}")

# 定義 API 路由
@app.get("/semesters")
async def get_semesters():
    """
    獲取所有學期，按最新到最舊排序。
    """
    try:
        all_semesters = list(semester_collection.find().sort("_id", -1))  # 按插入順序降序
        return {"semesters": [doc["semester"] for doc in all_semesters]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"無法獲取學期清單: {str(e)}")

@app.post("/semesters/import")
async def import_new_semester(new_semester: str):
    """
    導入新學期，並維護學期清單。
    """
    try:
        add_new_semester(new_semester)
        return {"message": f"學期 {new_semester} 已導入並維護完成"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"無法導入新學期: {str(e)}")

# 定義 JSON 文件導入邏輯
def import_json_files(json_dir):
    """
    將指定資料夾中的 JSON 文件導入 MongoDB，並根據學期更新學期集合。
    """
    for file_name in os.listdir(json_dir):
        if file_name.endswith(".json"):
            semester = os.path.splitext(file_name)[0]
            print(f"處理 JSON 文件: {file_name}")
            add_new_semester(semester)

# 主程序
if __name__ == "__main__":
    json_directory = "output_data"  # 指定 JSON 資料夾
    import_json_files(json_directory)  # 自動導入 JSON 檔案中的學期
