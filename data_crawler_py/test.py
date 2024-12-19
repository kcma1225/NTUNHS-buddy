import requests

BASE_URL = "http://127.0.0.1:8000"  # 根據您的 API 位址更新
STUDENT_ACCOUNT = {
    "username": "112214129",  # 測試帳號
    "password": "Ntunhs129"   # 測試密碼
}

def student_login():
    """
    登入學生帳號，並返回 Token。
    """
    response = requests.post(f"{BASE_URL}/login", json=STUDENT_ACCOUNT)
    if response.status_code == 200:
        print("學生登入成功，Token 已獲取")
        return response.cookies.get("auth_token")
    else:
        print(f"學生登入失敗: {response.status_code}, {response.json()}")
        return None

def get_favorites_details(token):
    """
    測試獲取我的最愛詳細資料。
    """
    response = requests.get(
        f"{BASE_URL}/get-favorites-details",
        cookies={"auth_token": token}
    )
    if response.status_code == 200:
        print("我的最愛詳細資料取得成功:")
        print(response.json())
    else:
        print(f"獲取我的最愛詳細資料失敗: {response.status_code}, {response.text}")

def main():
    # 登入學生並獲取 Token
    token = student_login()
    if not token:
        return

    # 測試獲取我的最愛詳細資料
    get_favorites_details(token)

if __name__ == "__main__":
    main()
