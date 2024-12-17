import requests

BASE_URL = "http://127.0.0.1:8000"

def test_selected_departments_clean():
    print("\n=== 測試: 學制 -> 系所 -> 最終課程篩選 (簡化版) ===")

    # Step 1: 選擇學制
    print("\n1. 測試 POST /available-education-types 選擇學制")
    payload = {"education_types": "1"}  # 1: 二技
    response = requests.post(f"{BASE_URL}/available-education-types", json=payload)
    if response.status_code == 200:
        selected_education = response.json()
        print(f"已選學制: {selected_education['selected_education_types']}")
    else:
        print("選擇學制失敗:", response.json())
        return

    # Step 2: 獲取系所列表
    print("\n2. 測試 GET /departments 獲取系所列表")
    params = {"education_types": "1"}  # 根據學制篩選
    response = requests.get(f"{BASE_URL}/departments", params=params)
    if response.status_code == 200:
        departments = response.json()
        print(f"系所總數量: {departments['count']}")
        print("可選擇的系所 (前 5 個):")
        for idx, dept in list(departments['departments'].items())[:5]:
            print(f"{idx}: {dept}")
        # 選擇一個系所的索引
        selected_index = list(departments['departments'].keys())[0]  # 選擇第一個索引
        print(f"選擇的系所索引: {selected_index}")
    else:
        print("獲取系所失敗:", response.json())
        return

    # Step 3: 選擇系所 (無多餘邏輯)
    print("\n3. 測試 POST /selected-departments 選擇單一系所")
    payload = {"departments": selected_index}
    response = requests.post(f"{BASE_URL}/selected-departments", json=payload)
    if response.status_code == 200:
        selected_departments = response.json()
        print(f"已選系所: {selected_departments['selected_departments']}")
    else:
        print("選擇系所失敗:", response.json())
        return

    # Step 4: 最終課程篩選
    print("\n4. 測試 GET /final-course-selection 獲取課程")
    params = {
        "education_types": "1",
        "departments": selected_departments['selected_departments'][0],
        "semesters": "1131"
    }
    response = requests.get(f"{BASE_URL}/final-course-selection", params=params)
    if response.status_code == 200:
        final_results = response.json()
        print(f"篩選後的課程總筆數: {final_results['count']}")
        print("\n前 5 筆課程資料:")
        for i, record in enumerate(final_results["results"][:5], start=1):
            print(f"\n【第 {i} 筆】")
            for key, value in record.items():
                print(f"{key}: {value}")
    else:
        print("獲取課程失敗:", response.json())

if __name__ == "__main__":
    test_selected_departments_clean()
