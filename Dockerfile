# 第一階段：Node 環境進行前端編譯
FROM node:18-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm install

# 複製專案所有檔案 (包含 src, vite.config.js, 等等)
COPY . .

# 進行前端打包，通常會產生 dist/ 資料夾
RUN npm run build


# 第二階段：使用 Nginx 來提供靜態檔 + Reverse Proxy
FROM nginx:stable-alpine

# 刪除預設靜態檔案
RUN rm -rf /usr/share/nginx/html/*

# 將 dist 資料夾中的檔案複製到 Nginx 預設靜態目錄
COPY --from=build /app/dist /usr/share/nginx/html

# 複製自訂的 default.conf (其中已經設定好 Reverse Proxy + CORS)
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]