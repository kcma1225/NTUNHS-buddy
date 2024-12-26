from fastapi import FastAPI, HTTPException, UploadFile , Response, Request, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from pymongo import MongoClient
from bcrypt import hashpw, gensalt, checkpw
from typing import List, Optional, Dict
import json
import re  
from bson import ObjectId
from jose import JWTError,jwt
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
# 常數設置
#SECRET_KEY = "my_secret_key_123456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10



# MongoDB 連接設置
def connect_to_mongodb():
    try:
        #client = MongoClient("mongodb://mongo:27017/")
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
db_account = client["account_database"]
db_course_favorites = client["course_favorites_database"]


SECRET_KEY = "my_secret_key_123456"

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://192.168.1.109:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#密碼帳號加密:
# 學生資料模型
class Student(BaseModel):
    帳號: str
    密碼: str
    姓名: str

class StudentList(BaseModel):
    students: List[Student]

# 模型定義
class LoginRequest(BaseModel):
    username: str
    password: str

class CourseUpdateRequest(BaseModel):
    _id: str
    update_data: Dict[str, str]

class StudentDetailsRequest(BaseModel):
    account: str
    
# 密碼加密
def hash_password(plain_password):
    return hashpw(plain_password.encode(), gensalt()).decode()

def verify_password(plain_password, hashed_password):
    return checkpw(plain_password.encode(), hashed_password.encode())

# Token 工具函數
def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="無效的 Token 或已過期")

# 驗證角色
def verify_role(request: Request, role: str):
    token = request.cookies.get("auth_token")
    if not token:
        raise HTTPException(status_code=401, detail="未登入或 Token 遺失")
    payload = verify_token(token)
    if payload.get("role") != role:
        raise HTTPException(status_code=403, detail=f"需要 {role} 權限")

# 登入 API

@app.post("/login")
async def login_user(login_request: LoginRequest):
    username = login_request.username
    password = login_request.password

    # 檢查帳號是否存在
    if username not in db_account.list_collection_names():
        raise HTTPException(status_code=404, detail="帳號不存在")

    # 驗證密碼
    user_data = db_account[username].find_one()
    if not user_data or "password" not in user_data:
        raise HTTPException(status_code=400, detail="帳號資料有誤")

    hashed_password = user_data["password"]
    if not checkpw(password.encode(), hashed_password.encode()):
        raise HTTPException(status_code=403, detail="密碼錯誤")

    # 獲取角色
    position = user_data.get("position", 2)  # 預設為學生
    role = "admin" if position == 1 else "student"

    # 獲取姓名
    name = user_data.get("name", "")  # 若無姓名則返回空字串


    # 生成 Token
    token = create_token({"sub": username, "role": role})

    # 回傳 Token 和角色
    return {
        "message": "登入成功",
        "role": role,
        "username": username,
        "name": name,
        "token": token  # 將 Token 包含在返回結果中
    }


   
    # 設定 Cookie 並回傳
    response = JSONResponse(
        content={
            "message": "登入成功",
            "role": role,
            "username": username,
            "name": name,
            "token": token  # 將 Token 包含在返回結果中
        }
    )
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        samesite='none',
        secure=False,
    )
    return response




    # 設定 Cookie 並回傳
    response = JSONResponse(content={"message": "登入成功", "role": role, })
    response.set_cookie(key="auth_token", value=token, httponly=True, samesite='none', secure=False,)
    return response



@app.post("/get-student-details")
async def get_student_details(request: Request, details_request: StudentDetailsRequest):
    """
    查詢指定學號的學生詳細資料。
    僅限管理員使用。
    """
    # 驗證角色為 admin
    #verify_role(request, "admin")

    account = details_request.account

    # 檢查帳號是否存在於資料庫
    if account not in db_account.list_collection_names():
        raise HTTPException(status_code=404, detail="帳號不存在")

    # 查詢該帳號的詳細資料
    student_collection = db_account[account]
    student_data = student_collection.find_one({}, {"_id": 0})  # 排除 _id 欄位

    if not student_data:
        raise HTTPException(status_code=404, detail="該帳號沒有相關資料")

    return {"status": "success", "student_details": student_data}



#這個很重要不能刪到
@app.post("/upload-students")
async def upload_students(file: UploadFile, request: Request):
    """
    從上傳的 JSON 檔案匯入學生資料
    """

    #verify_role(request, "admin") 

    try:
        # 讀取 JSON 檔案
        content = await file.read()
        students = json.loads(content)

        skipped_accounts = []  # 記錄已存在的帳號
        imported_accounts = []  # 記錄成功匯入的帳號

        for student in students:
            account_collection_name = student["帳號"]

            # 如果帳號已存在，跳過
            if account_collection_name in db_account.list_collection_names():
                skipped_accounts.append(account_collection_name)
                print(f"帳號 {account_collection_name} 已存在，跳過")
                continue

            hashed_password = hash_password(student["密碼"])

            # 插入到 account_database
            db_account[account_collection_name].insert_one({
                "password": hashed_password,
                "name": student["姓名"],
                "position": 2  # 預設職位為 2 (學生)
            })
            print(f"已新增學生帳號: {account_collection_name}")
            imported_accounts.append(account_collection_name)

            # 插入到 course_favorites_database
            if account_collection_name not in db_course_favorites.list_collection_names():
                db_course_favorites[account_collection_name].insert_one({})
                print(f"已新增課程收藏帳號: {account_collection_name}")
            else:
                print(f"課程收藏帳號 {account_collection_name} 已存在，跳過")

        return {
            "status": "success",
            "imported_accounts": imported_accounts,
            "skipped_accounts": skipped_accounts,
            "message": f"成功匯入 {len(imported_accounts)} 個帳號，跳過 {len(skipped_accounts)} 個已存在的帳號"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"匯入失敗: {str(e)}")


@app.post("/import-courses")
async def import_courses(file: UploadFile, request: Request):
    """
    管理員權限專屬：匯入課程資料並按學制和系所分類存入 MongoDB。
    """
    # 驗證管理員權限
    #verify_role(request, "admin")

    try:
        # 讀取 JSON 文件內容
        content = await file.read()
        courses = json.loads(content)

        if not isinstance(courses, list):
            raise HTTPException(status_code=400, detail="上傳文件格式錯誤，應為 JSON 陣列")

        imported_count = 0
        for course in courses:
            # 排除不需要的欄位
            course.pop("編號", None)

            # 按學制分類
            education_type = course.get("學制", "未分類")
            department = course.get("系所", "未分類")

            if not education_type or not department:
                raise HTTPException(status_code=400, detail="課程資料缺少必要欄位")

            #獲取學制 Collection
            education_collection = db[education_type]  # 使用 db 而非 output_db

            # 插入資料至學制內的系所
            department_data = {
                **course,
                "_id": str(ObjectId())  # 為每筆資料生成唯一 _id
            }
            education_collection.update_one(
                {"系所": department},
                {"$push": {"courses": department_data}},
                upsert=True
            )

            imported_count += 1

        return {
            "status": "success",
            "message": f"成功匯入 {imported_count} 筆課程資料",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"匯入過程發生錯誤: {str(e)}")



# Step 1: 根據 _id 取得課程
@app.post("/edit-course")
async def edit_course(request: Request, _id: str):
    #verify_role(request, "admin")  # 確保是管理員
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        document = collection.find_one({"_id": ObjectId(_id)})
        if document:
            document["_id"] = str(document["_id"])  # 確保 _id 是字串
            return {"status": "success", "course": document}
    raise HTTPException(status_code=404, detail="課程未找到")



# Step 2: 根據 _id 取得課程詳細內容
@app.get("/get-course-by-id")
async def get_course_by_id(request: Request, _id: str):
    #verify_role(request, "admin")  # 確保是管理員
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        document = collection.find_one({"_id": ObjectId(_id)})
        if document:
            document["_id"] = str(document["_id"])  # 確保 _id 是字串
            return {"status": "success", "course": document}
    raise HTTPException(status_code=404, detail="課程未找到")



# Step 3
@app.post("/update-course")
async def update_course(request: Request, course_request: Dict[str, dict]):
    """
    更新課程資料，限制不能修改 '學制'、'系所' 和 '教師姓名'。
    """
    #verify_role(request, "admin")  # 確保使用者是管理員

    _id = course_request.get("_id")
    update_data = course_request.get("update_data")

    if not _id or not update_data:
        print("Missing _id or update_data")
        raise HTTPException(status_code=400, detail="缺少必要的 _id 或更新資料")

    try:
        object_id = ObjectId(_id)
        print(f"ObjectId conversion successful: {object_id}")
    except Exception as e:
        print(f"ObjectId conversion failed: {e}")
        raise HTTPException(status_code=400, detail="提供的 _id 無效")

    restricted_fields = {"學制", "系所", "教師姓名"}
    for field in restricted_fields:
        if field in update_data:
            print(f"Restricted field found: {field}")
            raise HTTPException(
                status_code=400,
                detail=f"Field '{field}' cannot be updated"
            )

    for collection_name in db.list_collection_names():
        print(f"Checking collection: {collection_name}")
        collection = db[collection_name]
        existing_course = collection.find_one({"_id": object_id})
        if existing_course:
            print(f"Existing course found: {existing_course}")
            result = collection.update_one({"_id": object_id}, {"$set": update_data})
            print(f"Update query: {{'_id': {object_id}}}")
            print(f"Update data: {update_data}")
            print(f"Update result: {result.modified_count}")
            if result.modified_count > 0:
                return {"status": "success", "message": "課程更新成功"}
            raise HTTPException(
                status_code=304, detail="No changes were made to the course"
            )

    print("Course not found")
    raise HTTPException(status_code=404, detail="課程未找到")



# Step 4: 根據 _id 刪除課程
@app.post("/delete-course")
async def delete_course(request: Request, course_request: Dict[str, str]):
    #verify_role(request, "admin")  # 確保是管理員
    _id = course_request.get("_id")  # 從請求中提取 _id

    # 確保 _id 被正確轉換為 ObjectId
    try:
        object_id = ObjectId(_id)
    except Exception:
        raise HTTPException(status_code=400, detail="提供的 _id 無效")

    # 遍歷所有學制 Collection
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        result = collection.find_one_and_delete({"_id": object_id})
        if result:
            return {"status": "success", "message": "課程刪除成功"}

    # 如果未找到對應的 _id
    raise HTTPException(status_code=404, detail="課程未找到或刪除失敗")

#=================================================================
#學生:


@app.post("/add-to-favorites")
async def add_to_favorites(account_id: str, course_id: str):
    """
    新增課程到學生的收藏，僅允許學生操作。
    """
    # 檢查是否提供帳號和課程 ID
    if not account_id or not course_id:
        raise HTTPException(status_code=400, detail="請提供有效的帳號和課程 ID")

    # 確保學生收藏的資料存在
    if account_id not in db_course_favorites.list_collection_names():
        raise HTTPException(status_code=404, detail="帳號不存在")

    favorites_collection = db_course_favorites[account_id]

    # 檢查是否已存在相同的課程 ID
    existing_favorite = favorites_collection.find_one({"course_id": course_id})
    if existing_favorite:
        raise HTTPException(status_code=400, detail="課程已在收藏中")

    # 新增課程 ID
    favorites_collection.insert_one({"course_id": course_id})
    return {"status": "success", "message": "課程已成功加入收藏"}

@app.get("/get-favorites-details")
async def get_favorites_details(account_id: str):
    """
    獲取學生收藏的課程詳細資料。
    """
    # 直接使用傳入的 account_id 作為參數，不再驗證 Token
    if not account_id:
        raise HTTPException(status_code=400, detail="請提供有效的帳號")

    # 獲取收藏的課程 ID
    favorites_collection = db_course_favorites[account_id]
    favorite_courses = list(favorites_collection.find({}, {"_id": 0, "course_id": 1}))

    # 過濾掉空白或無效的資料
    valid_favorite_courses = [
        course for course in favorite_courses
        if "course_id" in course and course["course_id"].strip()
    ]

    if not valid_favorite_courses:
        return {"status": "success", "favorites": [], "message": "無收藏課程"}

    # 檢查 output_database 中的課程詳細資料
    detailed_courses = []
    valid_ids = set()  # 用於記錄有效的 course_id

    for course in valid_favorite_courses:
        try:
            # 將 course_id 轉換為 ObjectId
            course_id = ObjectId(course["course_id"])
            for collection_name in db.list_collection_names():
                collection = db[collection_name]
                document = collection.find_one({"_id": course_id})
                if document:
                    # 如果找到課程，記錄為有效
                    valid_ids.add(course["course_id"])
                    document["_id"] = str(document["_id"])  # 確保 _id 為字串
                    detailed_courses.append(document)
                    break  # 如果找到資料，停止繼續查找
        except Exception:
            # 如果 course_id 無效，從收藏中刪除
            favorites_collection.delete_one({"course_id": course["course_id"]})

    # 移除 output_database 中未找到的課程
    for course in valid_favorite_courses:
        if course["course_id"] not in valid_ids:
            favorites_collection.delete_one({"course_id": course["course_id"]})

    # 返回結果
    return {"status": "success", "favorites": detailed_courses}

@app.post("/remove-from-favorites")
async def remove_from_favorites(account_id: str, course_id: str):
    """
    從學生的收藏中移除指定課程。
    """
    # 確保提供帳號和課程 ID
    if not account_id or not account_id.strip():
        raise HTTPException(status_code=400, detail="請提供有效的帳號")
    if not course_id or not course_id.strip():
        raise HTTPException(status_code=400, detail="請提供有效的課程 ID")

    # 確保學生的收藏資料集合存在
    favorites_collection = db_course_favorites[account_id]

    try:
        object_id = ObjectId(course_id.strip())  # 確保 course_id 格式正確
    except Exception:
        raise HTTPException(status_code=400, detail="提供的課程 ID 無效")

    # 刪除相應的課程 ID
    result = favorites_collection.delete_one({"course_id": str(object_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="該課程未在我的最愛中")

    return {"status": "success", "message": "課程已成功從我的最愛中移除"}







#下面都是選課的不用登入的地方================================================================================


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
    """
    獲取指定教育類型下的所有系所。
    """
    # 解析教育類型參數
    education_ids = education_types.split(",") if education_types else []

    # 如果沒有提供教育類型，返回所有科系
    if not education_ids:
        departments = {}
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            department_list = collection.distinct("系所")
            departments[collection_name] = department_list
        return {"departments": departments, "count": sum(len(v) for v in departments.values())}

    # 僅返回指定教育類型的系所
    departments = {}
    for eid in education_ids:
        collection_name = EDUCATION_MAPPING.get(eid)
        if collection_name in db.list_collection_names():
            collection = db[collection_name]
            department_list = collection.distinct("系所")
            departments[collection_name] = department_list

    return {"departments": departments, "count": sum(len(v) for v in departments.values())}


@app.post("/selected-departments")
async def selected_departments(request: DepartmentQuery, education_types: str = Query(None)):
    """
    接收系所數字索引並返回對應名稱。
    """
    # 獲取 departments 列表，需先傳入學制參數
    departments_mapping = await get_departments(education_types)  # 確保正確等待結果
    indexed_departments = departments_mapping["departments"]

    # 將所有系所展平為單一層結構，並生成數字索引
    flat_departments = {}
    index = 0
    for collection, departments in indexed_departments.items():
        for department in departments:
            flat_departments[str(index)] = {"collection": collection, "department": department}
            index += 1

    # 根據索引選擇系所
    selected_indices = request.departments.split(",") if request.departments else []
    selected_departments = [
        flat_departments[index]
        for index in selected_indices
        if index in flat_departments
    ]

    # 如果未提供索引，返回所有系所
    if not selected_departments:
        selected_departments = list(flat_departments.values())  # 預設返回所有系所

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
        # 處理教師姓名，只取第一個 "\n\n" 前的內容(改2)
        if "教師姓名" in record and isinstance(record["教師姓名"], str) and "\n\n" in record["教師姓名"]:
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


           # 包含 _id 並查詢
            cursor = collection.find(query)
            for document in cursor:
                document["_id"] = str(document["_id"])  # 確保 _id 為字串
                results.append(document)

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



