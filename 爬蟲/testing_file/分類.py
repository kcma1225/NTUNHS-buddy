import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
import time
import json

# 初始化 Edge 瀏覽器
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service)

try:
    # 設定輸出目錄
    output_dir = "課程內容分類"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已創建輸出目錄: {output_dir}")

    # 打開目標網站
    url = "https://system10.ntunhs.edu.tw/AcadInfoSystem/Modules/QueryCourse/QueryCourse.aspx"
    driver.get(url)
    print(f"Successfully opened {url}")

    # 等待頁面完全加載，並找到"學期多選"按鈕
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "btnMultiSemNo"))
    )
    print("學期多選按鈕已加載！")

    # 點擊"學期多選"按鈕
    multi_select_button = driver.find_element(By.ID, "btnMultiSemNo")
    multi_select_button.click()
    print("已點擊學期多選按鈕！")

    # 選擇指定學期 (1132、1131、1122、1121)
    target_terms = ["1132", "1131", "1122", "1121"]
    for term in target_terms:
        checkbox = driver.find_element(By.XPATH, f"//input[@value='{term}']")
        if not checkbox.is_selected():
            checkbox.click()
            print(f"已選擇學期: {term}")
        time.sleep(0.5)  # 等待操作完成

    # 等待新學制選項表格加載
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "divNewEduType"))
    )
    print("學制區塊已加載！")

    # 選擇所有學制
    edu_type_ids = [
        "ContentPlaceHolder1_cblNewEduType_0",  # 二技
        "ContentPlaceHolder1_cblNewEduType_1",  # 二技(三年)
        "ContentPlaceHolder1_cblNewEduType_2",  # 四技
        "ContentPlaceHolder1_cblNewEduType_3",  # 學士後多元專長
        "ContentPlaceHolder1_cblNewEduType_4",  # 碩士班
        "ContentPlaceHolder1_cblNewEduType_5",  # 博士班
        "ContentPlaceHolder1_cblNewEduType_6",  # 學士後學位學程
        "ContentPlaceHolder1_cblNewEduType_7"   # 學士後系
    ]
    for edu_type_id in edu_type_ids:
        edu_type_checkbox = driver.find_element(By.ID, edu_type_id)
        driver.execute_script("arguments[0].scrollIntoView(true);", edu_type_checkbox)
        time.sleep(0.5)
        if not edu_type_checkbox.is_selected():
            edu_type_checkbox.click()
            print(f"已選擇學制: {edu_type_id}")

    # 選擇所有課程內容分類
    category_ids = [
        "ContentPlaceHolder1_cblCategory_0",  # 跨校
        "ContentPlaceHolder1_cblCategory_1",  # 跨域課程
        "ContentPlaceHolder1_cblCategory_2",  # 全英語授課
        "ContentPlaceHolder1_cblCategory_3",  # EMI全英語授課
        "ContentPlaceHolder1_cblCategory_4",  # 同步遠距教學
        "ContentPlaceHolder1_cblCategory_5",  # 非同步遠距教學
        "ContentPlaceHolder1_cblCategory_6",  # 混合式遠距教學
        "ContentPlaceHolder1_cblCategory_7",  # 遠距教學課程
        "ContentPlaceHolder1_cblCategory_8"   # 遠距輔助課程
    ]
    for category_id in category_ids:
        category_checkbox = driver.find_element(By.ID, category_id)
        driver.execute_script("arguments[0].scrollIntoView(true);", category_checkbox)
        time.sleep(0.5)
        if not category_checkbox.is_selected():
            category_checkbox.click()
            print(f"已選擇課程內容分類: {category_id}")

    # 等待查詢按鈕可用
    query_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnQuery"))
    )
    print("查詢按鈕已加載！")

    # 點擊查詢按鈕
    query_button.click()
    print("已點擊查詢按鈕！")

    # 等待查詢結果加載
    time.sleep(20)

    # 爬取查詢結果並比較是否有重複
    try:
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')
        table = soup.find('table', {'id': 'ContentPlaceHolder1_NewGridView'})
        if not table:
            raise Exception(f"結果表格未找到！")
        print(f"查詢結果表格已加載！")

        rows = table.find_all('tr')[1:]
        courses = []
        unique_courses = {}
        for index, row in enumerate(rows):
            cols = row.find_all('td')
            if len(cols) < 14:
                continue
            course_data = {
                "學期": cols[1].text.strip(),
                "系所": cols[2].text.strip(),
                "年級": cols[3].text.strip(),
                "班組": cols[4].text.strip(),
                "科目代號": cols[5].text.strip(),
                "課程名稱": cols[6].text.strip(),
                "教師姓名": cols[7].text.strip(),
                "上課人數": cols[8].text.strip(),
                "學分數": cols[9].text.strip(),
                "課別": cols[10].text.strip(),
                "地點": cols[11].text.strip(),
                "星期": cols[12].text.strip(),
                "節次": cols[13].text.strip(),
            }
            course_tuple = tuple(course_data.values())
            if course_tuple in unique_courses:
                first_index = unique_courses[course_tuple]
                print(f"重複數據發現！\n第一次出現於索引: {first_index}, 數據: {courses[first_index]}\n當前索引: {index}, 數據: {course_data}")
            else:
                unique_courses[course_tuple] = index
                courses.append(course_data)

        output_file = os.path.join(output_dir, "跨校課程.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(courses, f, ensure_ascii=False, indent=4)
        print(f"查詢結果已保存到 {output_file}")

    except Exception as e:
        print(f"處理查詢結果時發生錯誤: {e}")

finally:
    driver.quit()
