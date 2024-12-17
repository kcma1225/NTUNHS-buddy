from pymongo import MongoClient

# 連接到 MongoDB
client = MongoClient("mongodb://localhost:27017/")

# 切換到指定的資料庫
db = client["output_database"]

def list_collection_data(collection_name, query=None):
    """
    列出指定 Collection 中的數據，支持條件篩選
    :param collection_name: Collection 的名稱
    :param query: 查詢條件（默認為空，表示列出所有數據）
    """
    collection = db[collection_name]
    
    # 查詢數據
    if query is None:
        query = {}  # 如果未提供查詢條件，則查詢所有數據

    documents = collection.find(query)
    
    # 列出數據
    print(f"Collection: {collection_name}")
    for doc in documents:
        print(doc)

    # 列出數據總數
    total_count = collection.count_documents(query)
    print(f"總數量: {total_count}")

if __name__ == "__main__":
    # 讓用戶輸入 Collection 名稱
    print("可選 Collection 名稱:")
    all_collections = db.list_collection_names()
    for i, name in enumerate(all_collections, start=1):
        print(f"{i}. {name}")

    collection_index = int(input("請選擇 Collection 的編號 (輸入編號): ").strip())
    collection_name = all_collections[collection_index - 1]

    # 可選的查詢條件
    user_input = input("是否需要添加查詢條件？(y/n): ").strip().lower()
    query = None

    if user_input == "y":
        # 範例：用戶輸入查詢條件，格式如 {"系所": "護理系博士班"}
        raw_query = input("請輸入查詢條件 (JSON 格式): ").strip()
        try:
            query = eval(raw_query)  # 注意，僅在確保輸入為可信時使用 eval
        except Exception as e:
            print(f"查詢條件格式錯誤: {e}")
            query = None

    # 列出 Collection 數據
    list_collection_data(collection_name, query)
