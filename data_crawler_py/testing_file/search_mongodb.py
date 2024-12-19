from pymongo import MongoClient

# 連接到 MongoDB
client = MongoClient("mongodb://localhost:27017/")

def check_database_and_collections():
    """
    檢查特定資料庫和 Collection 是否存在，並檢查帳號資料庫內容
    """
    # 定義目標資料庫
    target_databases = ["account_database", "course_favorites_database"]
    all_databases = client.list_database_names()

    # 遍歷目標資料庫，檢查是否存在
    for db_name in target_databases:
        if db_name in all_databases:
            print(f"資料庫 '{db_name}' 已存在")

            # 檢查帳號資料庫是否有管理者帳號
            if db_name == "account_database":
                db = client[db_name]
                if "admin" in db.list_collection_names():
                    print("帳號資料庫的 'admin' Collection 已存在")
                    encrypted_password = db["admin"].find_one().get("password")
                    print(f"加密密碼: {encrypted_password}")
                else:
                    print("帳號資料庫中尚無 'admin' Collection")
        else:
            print(f"資料庫 '{db_name}' 尚未創建")

if __name__ == "__main__":
    check_database_and_collections()
