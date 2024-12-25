import os
import json
from pymongo import MongoClient
from bcrypt import hashpw, gensalt, checkpw



# 加密密碼
def hash_password(plain_password):
    return hashpw(plain_password.encode(), gensalt()).decode()

# 連接 MongoDB
def connect_to_mongodb():
    client = MongoClient("mongodb://mongo:27017/")
    print("成功連接到 MongoDB")
    return client

# 創建管理帳號資料庫
def create_account_database():
    client = connect_to_mongodb()
    db_name = "account_database"
    db = client[db_name]

    # 預設管理帳號與密碼
    admin_username = "admin"
    admin_password = "0000" #a22512188
    admin_position = 1  # 職位代碼：1 代表管理員
    hashed_password = hash_password(admin_password)

    # 插入管理者帳號
    if admin_username not in db.list_collection_names():
        db[admin_username].insert_one({
            "password": hashed_password,
            "position": admin_position  # 新增職位欄位
        })
        print(f"已創建管理者帳號: {admin_username}，並加密密碼和設置職位")
    else:
        print(f"管理者帳號 {admin_username} 已存在")

    return db_name, hashed_password

# 創建選課系統資料庫
def create_course_favorites_database():
    client = connect_to_mongodb()
    db_name = "course_favorites_database"
    db = client[db_name]

    # 確保資料庫創建至少有一個初始 Collection
    init_collection_name = "init_collection"
    if init_collection_name not in db.list_collection_names():
        db[init_collection_name].insert_one({"message": "Initialization document"})
        print(f"已創建初始 Collection '{init_collection_name}'")

    print(f"選課系統資料庫 {db_name} 已創建（包含初始 Collection）")
    return db_name






# 檢查 Collection 是否已存在
def is_collection_existing(db, collection_name):
    return collection_name in db.list_collection_names()

# 檢查數據是否已存在
def is_already_imported(collection, data):
    if isinstance(data, list) and data:
        first_item = data[0]
        return collection.find_one(first_item) is not None
    elif isinstance(data, dict):
        return collection.find_one(data) is not None
    return False

# 修改部分代碼，在插入數據時排序
def import_json_to_mongodb(output_data_dir, db_name):
    client = connect_to_mongodb()
    db = client[db_name]

    # 確保學制按名稱排序
    for file_name in sorted(os.listdir(output_data_dir)):  # 按字母順序排序文件名稱
        if file_name.endswith(".json"):
            file_path = os.path.join(output_data_dir, file_name)
            collection_name = os.path.splitext(file_name)[0]  # 以文件名作為 Collection 名稱（學制）

            # 檢查 Collection 是否存在
            if is_collection_existing(db, collection_name):
                print(f"Collection '{collection_name}' 已存在，跳過該學制")
                continue

            # 讀取 JSON 數據
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 將數據分類並插入到學制 Collection
            collection = db[collection_name]
            classified_data = {}

            for record in data:
                department = record.get("系所", "未分類")
                if department not in classified_data:
                    classified_data[department] = []
                classified_data[department].append(record)

            # 插入所有系所數據到該 Collection
            for department, records in classified_data.items():
                if not is_already_imported(collection, records):
                    collection.insert_many(records)
                    print(f"已將 '{department}' 的 {len(records)} 筆資料插入到 Collection: {collection_name}")

    print("所有學制數據已處理並導入 MongoDB！")


# 主程序
if __name__ == "__main__":
    # 設置參數
    output_data_dir = "output_data"   # 學制 JSON 檔案所在資料夾
    database_name = "output_database"  # MongoDB 資料庫名稱

    # 確保資料夾存在
    if not os.path.exists(output_data_dir):
        print(f"資料夾 '{output_data_dir}' 不存在，請檢查路徑！")
        exit()

    account_db_name, hashed_admin_password = create_account_database()
    course_db_name = create_course_favorites_database()



    # 執行數據導入程序
    import_json_to_mongodb(output_data_dir, database_name)






