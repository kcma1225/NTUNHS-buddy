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
    output_dir = "output_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已創建輸出目錄: {output_dir}")

    # 打開目標網站
    url = "https://system10.ntunhs.edu.tw/AcadInfoSystem/Modules/QueryCourse/QueryCourse.aspx"
    driver.get(url)
    print(f"Successfully opened {url}")

    # 學制選項及其對應文件名
    edu_types = {
        "二技": "ContentPlaceHolder1_cblNewEduType_0",
        "二技(三年)": "ContentPlaceHolder1_cblNewEduType_1",
        "四技": "ContentPlaceHolder1_cblNewEduType_2",
        "學士後多元專長": "ContentPlaceHolder1_cblNewEduType_3",
        "碩士班": "ContentPlaceHolder1_cblNewEduType_4",
        "博士班": "ContentPlaceHolder1_cblNewEduType_5",
        "學士後學位學程": "ContentPlaceHolder1_cblNewEduType_6",
        "學士後系": "ContentPlaceHolder1_cblNewEduType_7"
    }

    # 對每個學制進行查詢並保存結果
    for edu_type_name, edu_type_id in edu_types.items():
        print(f"開始處理學制: {edu_type_name}")

        # 每次查詢前重新選擇學期
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "btnMultiSemNo"))
        )
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

        # 找到學制 checkbox 並點擊
        edu_type_checkbox = driver.find_element(By.ID, edu_type_id)
        driver.execute_script("arguments[0].scrollIntoView(true);", edu_type_checkbox)  # 滾動到學制選項
        time.sleep(1)  # 避免滾動完成後立即操作導致問題
        edu_type_checkbox.click()
        print(f"已選擇學制: {edu_type_name}")

        # 等待查詢按鈕可用
        query_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnQuery"))
        )
        print("查詢按鈕已加載！")

        # 點擊查詢按鈕
        query_button.click()
        print("已點擊查詢按鈕！")

        # 等待查詢結果加載
        time.sleep(20)  # 視網頁響應速度調整

        # 爬取查詢結果
        try:
            # 獲取網頁 HTML
            html_source = driver.page_source

            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(html_source, 'html.parser')

            # 查找結果表格
            table = soup.find('table', {'id': 'ContentPlaceHolder1_NewGridView'})
            if not table:
                raise Exception(f"結果表格未找到，學制: {edu_type_name}")

            print(f"查詢結果表格已加載，學制: {edu_type_name}")

            # 提取表格數據
            rows = table.find_all('tr')[1:]  # 跳過表頭
            courses = []
            for row in rows:
                cols = row.find_all('td')
                if len(cols) < 14:  # 確保列數足夠
                    continue
                courses.append({
                    "編號": cols[0].text.strip(),
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
                })

            # 將數據保存到對應的 JSON 文件
            output_file = os.path.join(output_dir, f"{edu_type_name}.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(courses, f, ensure_ascii=False, indent=4)

            print(f"查詢結果已保存到 {output_file}")

        except Exception as e:
            print(f"處理查詢結果時發生錯誤，學制: {edu_type_name}, 錯誤: {e}")

        # 清除選項，準備下一次查詢
        clear_button = driver.find_element(By.ID, "ContentPlaceHolder1_btnClear")
        clear_button.click()
        print(f"已清除選項，準備下一次查詢")

        time.sleep(5)  # 等待清除完成

finally:
    # 關閉瀏覽器
    driver.quit()
