from fastapi import FastAPI, HTTPException, Query
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

# 預設學制清單數字映射
EDUCATION_MAPPING = {
    "1": "二技",
    "2": "二技(三年)",
    "3": "四技",
    "4": "學士後多元專長",
    "5": "碩士班",
    "6": "博士班",
    "7": "學士後學位學程",
    "8": "學士後系"
}
DEFAULT_EDUCATION_IDS = ["1", "2", "3", "4", "5", "6", "7", "8"]  # 預設學制數字

# 新增學期預設與映射
DEFAULT_SEMESTERS = ["1132"]  # 預設學期
SEMESTER_MAPPING = {
    "1131": "1131",
    "1132": "1132",
    "1121": "1121",
    "1122": "1122"
}

# 年級預設值與映射
DEFAULT_GRADES = ["1", "2", "3", "4"]  # 預設為全年級
GRADE_MAPPING = {"1": "1", "2": "2", "3": "3", "4": "4"}


# 課別預設值與映射
DEFAULT_COURSE_CATEGORIES = ["1", "2", "3", "4"]  # 預設選全部
COURSE_CATEGORY_MAPPING = {
    "1": "通識必修(通識)",
    "2": "專業必修(系所)",
    "3": "通識選修(通識)",
    "4": "專業選修(系所)"
}

# 課程內容分類預設值與映射
DEFAULT_COURSE_CONTENTS = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"
]
COURSE_CONTENT_MAPPING = {
    "1": "跨校",
    "2": "跨域課程",
    "3": "全英語授課",
    "4": "EMI全英語授課",
    "5": "同步遠距教學",
    "6": "非同步遠距教學",
    "7": "混合式遠距教學",
    "8": "遠距教學課程",
    "9": "遠距輔助課程",
    "10": "無"
}


# 星期預設值與映射
DEFAULT_WEEKDAYS = ["1", "2", "3", "4", "5", "6", "7"]  # 預設全選
WEEKDAY_MAPPING = {str(i): f"星期{i}" for i in range(1, 8)}

# 節次預設值與映射
DEFAULT_PERIODS = [str(i) for i in range(1, 15)]  # 節次 1 到 14
PERIOD_MAPPING = {str(i): f"第{i}節" for i in range(1, 15)}



# 定義請求模型
class EducationQuery(BaseModel):
    education_types: str = None  # 數字字串，以逗號分隔，允許為 None

class DepartmentQuery(BaseModel):
    departments: str = None  # 系所參數

# 定義學期請求模型
class SemesterQuery(BaseModel):
    semesters: str = None  # 學期參數，數字字串以逗號分隔，允許為 None

# 定義年級請求模型
class GradeQuery(BaseModel):
    grades: str = None  # 年級參數，數字字串以逗號分隔，允許為 None

# 定義課別請求模型
class CourseCategoryQuery(BaseModel):
    course_categories: str = None  # 課別參數，數字字串以逗號分隔
# 定義課程內容分類請求模型
class CourseContentQuery(BaseModel):
    course_contents: str = None  # 課程內容分類參數，數字字串以逗號分隔
# 定義星期請求模型
class WeekdayQuery(BaseModel):
    weekdays: str = None  # 星期參數，數字字串以逗號分隔

# 定義節次請求模型
class PeriodQuery(BaseModel):
    periods: str = None  # 節次參數，數字字串以逗號分隔


@app.post("/available-education-types")
async def available_education_types(request: EducationQuery):
    """
    接收數字化的學制清單，回傳對應的學制名稱。
    若未提供學制，則回傳預設學制。
    """
    education_ids = request.education_types.split(",") if request.education_types else DEFAULT_EDUCATION_IDS
    selected_educations = [EDUCATION_MAPPING.get(eid, None) for eid in education_ids if eid in EDUCATION_MAPPING]
    return {"selected_education_types": selected_educations}


@app.get("/departments")
async def get_departments(education_types: str = Query(None)):
    """ 根據學制篩選系所並加上索引 """
    education_ids = education_types.split(",") if education_types else DEFAULT_EDUCATION_IDS
    selected_collections = [EDUCATION_MAPPING.get(eid) for eid in education_ids if EDUCATION_MAPPING.get(eid)]

    departments_set = set()
    for collection_name in selected_collections:
        if collection_name in db.list_collection_names():
            collection = db[collection_name]
            departments = collection.distinct("系所")
            departments_set.update(departments)

    departments_list = sorted(list(departments_set))
    indexed_departments = {str(i + 1): dept for i, dept in enumerate(departments_list)}
    return {"departments": indexed_departments, "count": len(departments_list)}



@app.post("/selected-departments")
async def selected_departments(request: DepartmentQuery, education_types: str = Query(None)):
    """ 接收系所數字索引並返回對應名稱 """
    # 獲取 departments 列表，需先傳入學制參數
    departments_mapping = await get_departments(education_types)
    indexed_departments = departments_mapping["departments"]

    # 根據索引選擇系所
    selected_indices = request.departments.split(",") if request.departments else []
    selected_departments = [indexed_departments.get(index) for index in selected_indices if index in indexed_departments]

    if not selected_departments:
        selected_departments = list(indexed_departments.values())  # 預設全選

    return {"selected_departments": selected_departments}

@app.post("/available-semesters")
async def available_semesters(request: SemesterQuery):
    """
    接收數字化的學期清單，回傳對應的學期名稱。
    若未提供學期，則回傳預設學期。
    """
    semester_ids = request.semesters.split(",") if request.semesters else DEFAULT_SEMESTERS
    selected_semesters = [SEMESTER_MAPPING.get(sid) for sid in semester_ids if sid in SEMESTER_MAPPING]
    return {"selected_semesters": selected_semesters}


@app.post("/available-grades")
async def available_grades(request: GradeQuery):
    """
    接收數字化的年級清單，回傳對應的年級。
    若未提供年級，則回傳預設值 (1, 2, 3, 4)。
    """
    grade_ids = request.grades.split(",") if request.grades else DEFAULT_GRADES
    selected_grades = [GRADE_MAPPING.get(gid) for gid in grade_ids if gid in GRADE_MAPPING]
    return {"selected_grades": selected_grades}



@app.post("/available-course-categories")
async def available_course_categories(request: CourseCategoryQuery):
    """
    接收數字化的課別清單，回傳對應的課別名稱。
    若未提供課別，則回傳預設值。
    """
    category_ids = request.course_categories.split(",") if request.course_categories else DEFAULT_COURSE_CATEGORIES
    selected_categories = [COURSE_CATEGORY_MAPPING.get(cid) for cid in category_ids if cid in COURSE_CATEGORY_MAPPING]
    return {"selected_course_categories": selected_categories}

@app.post("/available-course-contents")
async def available_course_contents(request: CourseContentQuery):
    """
    接收數字化的課程內容分類，回傳對應的課程分類名稱。
    若未提供，則回傳預設值。
    """
    content_ids = request.course_contents.split(",") if request.course_contents else DEFAULT_COURSE_CONTENTS
    selected_contents = [COURSE_CONTENT_MAPPING.get(cid) for cid in content_ids if cid in COURSE_CONTENT_MAPPING]
    return {"selected_course_contents": selected_contents}


@app.post("/available-weekdays")
async def available_weekdays(request: WeekdayQuery):
    """
    接收星期清單，回傳對應的星期名稱。
    若未提供，則回傳預設值。
    """
    weekday_ids = request.weekdays.split(",") if request.weekdays else DEFAULT_WEEKDAYS
    selected_weekdays = [WEEKDAY_MAPPING.get(wid) for wid in weekday_ids if wid in WEEKDAY_MAPPING]
    return {"selected_weekdays": selected_weekdays}


@app.post("/available-periods")
async def available_periods(request: PeriodQuery):
    """
    接收節次清單，回傳對應的節次名稱。
    若未提供，則回傳預設值。
    """
    period_ids = request.periods.split(",") if request.periods else DEFAULT_PERIODS
    selected_periods = [PERIOD_MAPPING.get(pid) for pid in period_ids if pid in PERIOD_MAPPING]
    return {"selected_periods": selected_periods}



def filter_results_by_keyword(results, keyword):
    """
    在初步篩選後的資料中進一步按關鍵字篩選。
    """
    if not keyword:  # 如果關鍵字未提供，返回原結果
        return results

    filtered = []
    for record in results:
        # 處理教師姓名，只取第一個 "\n\n" 前的內容
        if "教師姓名" in record and "\n\n" in record["教師姓名"]:
            record["教師姓名"] = record["教師姓名"].split("\n\n")[0]

        # 進行關鍵字比對
        if any(keyword.lower() in str(record.get(field, "")).lower() for field in ["系所", "班組", "科目代號", "課程名稱", "教師姓名", "地點"]):
            filtered.append(record)

    return filtered

@app.get("/final-course-selection")
async def get_final_course_selection(
    education_types: str = Query(None),
    departments: str = Query(None),
    semesters: str = Query(None),  # 新增學期參數
    grades: str = Query(None),  # 新增年級參數
    course_categories: str = Query(None),  # 新增課別參數
    course_contents: str = Query(None),  # 新增課程內容分類參數
    weekdays: str = Query(None),  # 新增星期參數
    periods: str = Query(None),  # 新增節次參數
    keyword: str = Query(None)  # 新增關鍵字參數
):
    """
    綜合學制、系所和學期條件篩選最終課程。
    """
# 解析參數
    education_ids = education_types.split(",") if education_types else DEFAULT_EDUCATION_IDS
    selected_collections = [EDUCATION_MAPPING.get(eid) for eid in education_ids if EDUCATION_MAPPING.get(eid)]
    departments_filter = [dept.strip().lower() for dept in departments.split(",")] if departments else None



    semesters_filter = semesters.split(",") if semesters else DEFAULT_SEMESTERS  # 使用預設學期
    grades_filter = grades.split(",") if grades else DEFAULT_GRADES  # 使用預設年級
    course_categories_filter = course_categories.split(",") if course_categories else DEFAULT_COURSE_CATEGORIES
    course_contents_filter = course_contents.split(",") if course_contents else DEFAULT_COURSE_CONTENTS
    weekdays_filter = weekdays.split(",") if weekdays else DEFAULT_WEEKDAYS
    periods_filter = periods.split(",") if periods else DEFAULT_PERIODS
    
    results = []

    for collection_name in selected_collections:
        if collection_name in db.list_collection_names():
            collection = db[collection_name]
            query = {"$and": []}

            if departments_filter:
                query["$and"].append({
                    "$expr": {
                        "$in": [{"$toLower": "$系所"}, departments_filter]
                    }
                })

            if semesters_filter:
                query["學期"] = {"$in": semesters_filter}
            if grades_filter:
                query["年級"] = {"$in": grades_filter}
            if course_categories_filter:
                query["課別"] = {"$in": [COURSE_CATEGORY_MAPPING[cid] for cid in course_categories_filter]}
            if course_contents_filter:
                query["課程內容分類"] = {"$in": [COURSE_CONTENT_MAPPING[cid] for cid in course_contents_filter]}
            if weekdays_filter:
                query["星期"] = {"$in": weekdays_filter}
           # 加入節次條件
            if periods_filter:
                query["$and"].append({
                    "$expr": {
                        "$setIsSubset": [{"$split": ["$節次", ","]}, periods_filter]
                    }
                })


            # 執行查詢
            # 執行初步查詢
            cursor = collection.find(query, {"_id": 0})
            results.extend(list(cursor))

    # 關鍵字篩選（若提供關鍵字）
    final_results = filter_results_by_keyword(results, keyword)

    return {
        "selected_education_types": selected_collections,
        "selected_departments": departments_filter if departments_filter else "全選",
        "selected_semesters": semesters_filter,
        "selected_grades": grades_filter,
        "selected_course_categories": course_categories_filter,
        "selected_course_contents": course_contents_filter,
        "selected_weekdays": weekdays_filter,
        "selected_periods": periods_filter,
        "selected_keyword": keyword if keyword else "未提供關鍵字",
        "results": final_results,  # 返回關鍵字過濾後的結果
        "count": len(final_results)  # 計算過濾後的筆數
    }



