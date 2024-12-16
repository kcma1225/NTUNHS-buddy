import requests

# API 基本 URL
BASE_URL = "http://127.0.0.1:8000"

def get_education_types():
    try:
        response = requests.get(f"{BASE_URL}/education-types")
        response.raise_for_status()
        return response.json().get("education_types", [])
    except Exception as e:
        print(f"無法獲取學制清單: {e}")
        return []

def get_departments(education_types):
    try:
        payload = {"education_types": education_types}
        response = requests.post(f"{BASE_URL}/departments", json=payload)
        response.raise_for_status()
        return response.json().get("departments", [])
    except Exception as e:
        print(f"無法獲取系所清單: {e}")
        return []

def search_data(payload):
    try:
        response = requests.post(f"{BASE_URL}/search", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API 請求失敗: {e}")
        return {}

def prompt_choice(options, message, allow_multiple=True, default=None):
    """
    提示用戶選擇選項，支持多選和預設值。
    """
    print(message)
    for i, option in enumerate(options, 1):
        print(f"{i}: {option}")

    default_message = f"（預設: {', '.join(default)})" if default else ""
    choice = input(f"請輸入選項編號 (可多選，以逗號分隔，Enter 預設 {default_message}): ")
    selected = []

    if choice.strip():
        indices = choice.split(",")
        for index in indices:
            if index.strip().isdigit() and 1 <= int(index.strip()) <= len(options):
                selected.append(options[int(index.strip()) - 1])
    else:
        return default or options  # 返回預設值或全選
    return selected




def filter_results_by_keyword(results, keyword):
    """
    根據關鍵字篩選結果。
    - 如果關鍵字為空，直接返回原始結果。
    - 特別處理教師姓名：只匹配 "\n\n" 前的內容。
    """
    if not keyword.strip():
        return results  # 如果沒有輸入關鍵字，返回原始結果

    keyword = keyword.lower()  # 將關鍵字轉為小寫以進行不區分大小寫的匹配
    filtered = []
    for record in results:
        # 處理教師姓名
        teacher_name = record.get("教師姓名", "")
        teacher_name = teacher_name.split("\n\n")[0] if "\n\n" in teacher_name else teacher_name

        # 檢查指定欄位是否包含關鍵字
        if any(
            keyword in str(record.get(field, "")).lower()
            for field in ["系所", "班組", "科目代號", "課程名稱", "地點"]
        ) or keyword in teacher_name.lower():
            record["教師姓名"] = teacher_name  # 更新教師姓名顯示格式
            filtered.append(record)
    return filtered





def test_search_api():
    # 學制選擇
    education_types = get_education_types()
    if not education_types:
        print("未能獲取學制清單，請檢查 API 或網路連線。")
        return
    selected_education = prompt_choice(education_types, "\n=== 學制選擇 ===")
    print(f"已選擇學制: {selected_education}")

    # 系所選擇
    departments = get_departments(selected_education)
    selected_departments = prompt_choice(departments, "\n=== 系所選擇 ===")
    print(f"已選擇系所: {selected_departments}")

    # 學期選擇
    semesters = prompt_choice(["1132", "1131", "1122", "1121"], "\n=== 學期選擇 ===", default=["1132"])
    print(f"已選擇學期: {semesters}")

    # 年級選擇
    grades = prompt_choice(["1", "2", "3", "4"], "\n=== 年級選擇 ===", default=["1", "2", "3", "4"])
    print(f"已選擇年級: {grades}")

    # 課別選擇
    course_types = prompt_choice(
        ["通識必修(通識)", "專業必修(系所)", "通識選修(通識)", "專業選修(系所)"],
        "\n=== 課別選擇 ===",
        default=["通識必修(通識)", "專業必修(系所)", "通識選修(通識)", "專業選修(系所)"]
    )
    print(f"已選擇課別: {course_types}")


    # 課程內容分類選擇
    course_categories = prompt_choice(
        ["跨校", "跨域課程", "全英語授課", "EMI全英語授課",
        "同步遠距教學", "非同步遠距教學", "混合式遠距教學",
        "遠距教學課程", "遠距輔助課程", "無"],
        "\n=== 課程內容分類選擇（Enter 略過） ===",
        allow_multiple=True
    )
    print(f"已選擇課程內容分類: {course_categories if course_categories else '未選擇（略過分類）'}")


 


    # 星期選擇
    weekdays = prompt_choice(["1", "2", "3", "4", "5", "6", "7"], "\n=== 星期選擇 ===", default=["1", "2", "3", "4", "5", "6", "7"])
    print(f"已選擇星期: {weekdays}")

    # 節次選擇
    class_periods = prompt_choice([str(i) for i in range(1, 15)], "\n=== 節次選擇 ===", default=[str(i) for i in range(1, 15)])
    print(f"已選擇節次: {class_periods}")



    
    


    # 執行查詢
    payload = {
        "education_types": selected_education,
        "departments": selected_departments,
        "semesters": semesters,
        "grades": grades,
        "course_types": course_types,
        "course_categories": course_categories,
        "weekdays": weekdays,
        "class_periods": class_periods,
        
    }

    results = search_data(payload)
    
    if results.get("results"):
        # 關鍵字篩選
        keyword = input("\n請輸入關鍵字進行進一步篩選（可跳過按 Enter）: ")
        filtered_results = filter_results_by_keyword(results["results"], keyword)
        for record in filtered_results:
            print(record)
        print(f"\n找到 {len(filtered_results)} 筆匹配的資料")
    else:
        print("未找到匹配的資料。")


if __name__ == "__main__":
    test_search_api()
