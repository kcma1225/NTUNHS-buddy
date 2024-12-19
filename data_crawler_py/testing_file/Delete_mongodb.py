from pymongo import MongoClient

# 連接到 MongoDB
client = MongoClient("mongodb://localhost:27017/")

# 要刪除的數據庫名稱列表
databases_to_delete = ["output_database", "account_database", "course_favorites_database"]

# 遍歷刪除數據庫
for db_name in databases_to_delete:
    client.drop_database(db_name)
    print(f"數據庫 '{db_name}' 已刪除")

print("所有指定數據庫已成功刪除！")
