# 使用官方 Python 基礎映像
FROM python:3.9-slim
# 設定工作目錄
WORKDIR /app
# 複製所有本地文件到容器內
COPY . /app
# 安裝所需的 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt
# 設定環境變數，避免生成 .pyc 文件
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# 開放 API 的埠
EXPOSE 8000
# 預設執行命令，啟動 API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]