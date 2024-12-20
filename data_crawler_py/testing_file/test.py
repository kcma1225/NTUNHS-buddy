import requests

def test_get_student_details():
    base_url = "http://localhost:8000"
    admin_credentials = {"username": "admin", "password": "a22512188"}

    # 登入以獲取 Token
    login_response = requests.post(f"{base_url}/login", json=admin_credentials)
    if login_response.status_code == 200:
        print("Admin login successful.")
        token = login_response.cookies.get("auth_token")
    else:
        print(f"Admin login failed: {login_response.status_code}, {login_response.text}")
        return

    # 測試獲取學生詳細資料
    student_account = "112214"
    response = requests.post(
        f"{base_url}/get-student-details",
        json={"account": student_account},
        cookies={"auth_token": token}
    )

    if response.status_code == 200:
        print("Student details fetched successfully.")
        print(response.json())
    else:
        print(f"Error fetching student details: {response.status_code}, {response.text}")

if __name__ == "__main__":
    test_get_student_details()
