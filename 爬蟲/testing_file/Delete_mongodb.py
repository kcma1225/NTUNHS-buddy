from pymongo import MongoClient

# 連接到 MongoDB
client = MongoClient("mongodb://localhost:27017/")

# 指定數據庫名稱
db_name = "output_database"

# 刪除數據庫
client.drop_database(db_name)
print(f"數據庫 '{db_name}' 已刪除")
