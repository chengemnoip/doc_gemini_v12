# 文件處理應用程式

## 專案簡介
這是一個功能強大的文件處理應用程式，旨在幫助使用者將多種格式的文件（如 PDF、程式碼文件、Jupyter Notebook 等）智能地轉換為結構良好的 Markdown 格式。本應用程式利用 Google Gemini AI 的強大能力，並透過 Flet 框架提供直觀的使用者介面。

## 功能特色
- 支援多種文件輸入格式：PDF、JavaScript (.js)、Python (.py)、TXT (.txt)、HTML、CSS、Markdown、CSV、XML、RTF。
- **特別支援 Jupyter Notebook (.ipynb) 文件轉換：** 自動提取程式碼和 Markdown 單元格內容並轉換為純文本 Markdown。
- 利用 Google Gemini AI 進行智能內容分析和 Markdown 生成。
- 可選擇不同的 Gemini 模型（例如 `gemini-2.5-flash`, `gemini-2.5-pro`）進行處理。
- 提供自定義提示詞，精確控制 AI 轉換行為。
- 支援從本地文件上傳或通過 URL 獲取文件。
- 轉換結果可直接下載為 `.md` 檔案。
- 跨平台支援 (桌面應用)。

## 技術棧
- **程式語言：** Python
- **GUI 框架：** Flet (基於 Google Flutter)
- **AI 整合：** Google Gen AI Python SDK (`google-genai`)
- **套件管理：** `uv`
- **環境變數管理：** `python-dotenv`
- **打包工具：** PyInstaller (透過 `flet pack`)

## 安裝與設定

### 1. 克隆專案
```bash
git clone [您的專案 Git URL]
cd [您的專案目錄]
```

### 2. 設定 Python 虛擬環境
建議使用 `uv` 創建和管理虛擬環境：
```bash
uv venv
# 激活虛擬環境 (Windows)
# .\.venv\Scripts\activate
# 激活虛擬環境 (macOS/Linux)
# source ./.venv/bin/activate
```

### 3. 安裝依賴
在激活的虛擬環境中，安裝所有必要的 Python 依賴：
```bash
uv sync
```
或手動添加：
```bash
uv add flet google-genai requests python-dotenv
```

### 4. 配置 Gemini API 金鑰
- 複製 `example.env` 檔案並重新命名為 `.env`：
  ```bash
  cp example.env .env  # Linux/macOS
  copy example.env .env # Windows
  ```
- 打開新創建的 `.env` 檔案，並將 `GEMINI_API_KEY` 替換為您的實際 Gemini API 金鑰。
  ```
  GEMINI_API_KEY="您的實際 Gemini API 金鑰"
  ```
  **重要：** 為了安全，請勿將您的 `.env` 檔案提交到版本控制中。`.gitignore` 檔案已配置為自動忽略它。

## 如何運行應用程式

### 1. 啟動應用程式
在激活的虛擬環境中，運行 `main.py`：
```bash
uv run main.py
```
應用程式將在您的預設瀏覽器中打開（通常是 `http://localhost:8550` 或類似位址）。

### 2. 使用應用程式
- **上傳本地文件：** 點擊「上傳本地文件」按鈕，選擇您要處理的文件。
- **從 URL 處理：** 在輸入框中輸入文件的 URL，然後點擊「從 URL 處理」按鈕。
- **選擇 AI 模型：** 從下拉菜單中選擇您希望使用的 Gemini 模型。
- **輸入提示詞：** 在提示詞區域輸入您對文件轉換的具體指令。
- **處理文件：** 點擊「處理文件」按鈕，應用程式將開始處理文件並生成 Markdown。
- **下載結果：** 處理完成後，點擊「下載 Markdown」按鈕保存生成的 Markdown 文件。

## 開發與打包

### 桌面應用打包 (Windows/macOS/Linux)
使用 `flet pack` 命令將應用程式打包為獨立執行檔：
```bash
flet pack main.py
```
打包後的執行檔將位於 `build/` 或 `dist/` 目錄中。

### Web 應用發布 (未來擴展)
使用 `flet publish` 命令將應用程式發布為 Web 應用：
```bash
flet publish main.py
```

## 貢獻
歡迎任何形式的貢獻！如果您有任何功能建議、錯誤報告或改進，請隨時提交 Issue 或 Pull Request。

## 授權
[您的授權資訊，例如 MIT 授權]