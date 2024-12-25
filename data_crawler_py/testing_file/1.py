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




# 處理教師姓名，只取第一個 "\n\n" 前的內容(改2)
    if "教師姓名" in record and "\n\n" in record["教師姓名"]:
        record["教師姓名"] = record["教師姓名"].split("\n\n")[0]