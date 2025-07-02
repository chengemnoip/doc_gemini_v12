# 專案簡報 (Project Brief)

## 專案名稱
文件處理應用程式 (Document Processing Application)

## 核心目標
本專案旨在開發一個功能全面的文件處理應用程式，其主要目標包括：
1.  **文件格式轉換：** 能夠將多種輸入文件格式（如 PDF, JavaScript, Python, TXT, HTML, CSS, Markdown, CSV, XML, RTF, ipynb）轉換為統一的 Markdown 格式。
2.  **使用者介面 (UI)：** 提供一個基於 Flet 框架的直觀使用者介面，使用戶能夠輕鬆操作。
3.  **文件上傳機制：** 支援從本地檔案系統上傳文件，以及透過 URL 方式獲取文件。文件上傳不論內容大小皆以 File API 的方式處理。
4.  **AI 模型整合：** 利用 Google Gen AI Python SDK (`google-genai`) 進行文件內容的分析、處理和生成。
5.  **模型選擇：** 允許使用者選擇預設的 `gemini-2.5-flash` 模型，並可選 `gemini-2.5-pro` 或自訂輸入。
6.  **安全規範：** 嚴格遵守安全最佳實踐，確保 API 金鑰等敏感資訊不會在客戶端程式碼中暴露。
7.  **獨立執行檔打包：** 能夠將應用程式打包成獨立的執行檔，使用戶無需安裝 Python 環境或額外依賴即可運行。

## 關鍵技術
*   **GUI 框架：** Flet (基於 Flutter)
*   **AI/ML 整合：** Google Gen AI Python SDK (`google-genai`)
*   **打包工具：** PyInstaller (透過 `flet pack` 調用)

## 輸入/輸出格式
*   **輸入文件格式：** PDF, JavaScript (.js), Python (.py), TXT (.txt), HTML, CSS, Markdown, CSV, XML, RTF, Jupyter Notebook (.ipynb)
*   **輸出文件格式：** Markdown (.md)

## 部署與發布
*   **桌面應用：** 使用 `flet pack` 命令打包為獨立執行檔。
*   **Web 應用：：** 使用 `flet publish` 命令發布為網頁應用 (未來可能擴展)。

## 安全考量
*   API 金鑰及其他敏感配置應安全地管理，避免硬編碼或在客戶端直接暴露。考慮使用環境變數、安全配置檔案或其他安全機制。