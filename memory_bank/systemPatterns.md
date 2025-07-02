# 系統模式 (System Patterns)

## 系統架構
本應用程式將採用一個清晰的分層架構，以確保模塊化、可維護性和可擴展性。

```mermaid
graph TD
    User[使用者] -->|互動| FletUI[Flet 使用者介面]
    FletUI -->|檔案上傳 (本地/URL)| BackendLogic[後端邏輯層 (Python)]
    BackendLogic -->|內容傳遞 & 提示| GoogleGeminiAPI[Google Gemini API]
    GoogleGeminiAPI -->|返回 Markdown| BackendLogic
    BackendLogic -->|顯示/儲存結果| FletUI
```

*   **使用者介面 (UI) 層：**
    *   **技術：** Flet (Python GUI 框架，底層基於 Flutter)。
    *   **職責：** 處理使用者輸入（文件上傳、模型選擇、提示輸入）、顯示應用程式狀態、展示轉換後的 Markdown 內容。
*   **後端邏輯層：**
    *   **技術：** Python。
    *   **職責：**
        *   接收 Flet UI 傳遞的文件數據或 URL。
        *   根據文件類型讀取和預處理文件內容。
        *   安全地將文件內容和使用者選擇的提示傳遞給 Google Gemini API。
        *   處理來自 Gemini API 的響應，進行後處理（如果需要）。
        *   將最終的 Markdown 內容返回給 Flet UI 進行顯示或保存。
        *   管理 API 金鑰的安全存取。
*   **AI 服務層：**
    *   **技術：** Google Gemini API (透過 `google-genai` Python SDK 進行交互)。
    *   **職責：** 提供核心的智能內容理解、轉換和生成能力，將各種輸入內容轉換為結構化的 Markdown 格式。

## 關鍵技術決策
1.  **GUI 框架選擇 Flet：**
    *   **原因：** Flet 允許使用 Python 快速構建美觀且跨平台的桌面和 Web 應用，其基於 Flutter 的渲染能力提供了優秀的使用者體驗。
2.  **AI 整合選擇 Google Gen AI Python SDK (`google-genai`)：**
    *   **原因：** 作為 Google 官方推薦的 SDK，它提供了對 Gemini API 最全面和最新的支持，便於集成高級 AI 功能。避免使用舊版 SDK 以確保兼容性和新特性。
3.  **文件處理策略：**
    *   對於不同文件類型，將採用不同的庫或方法進行初始內容提取（例如，PDF 可能需要 `PyPDF2` 或 `fitz` (PyMuPDF)，程式碼文件和文本文件可直接讀取）。這將是後端邏輯層的重要組成部分。
4.  **API 金鑰管理：**
    *   API 金鑰絕不應硬編碼在客戶端程式碼中。將採用環境變數或安全的配置管理方式，確保金鑰在伺服器端（即應用程式運行環境）被安全地加載和使用。

## 設計模式
*   **模型-視圖-控制器 (MVC) 或 模型-視圖-視圖模型 (MVVM)：** Flet 應用程式的結構可以自然地映射到這些模式，以分離 UI、邏輯和數據。
*   **策略模式 (Strategy Pattern)：** 針對不同的文件類型（PDF, JS, Python, TXT, HTML, CSS, MD, CSV, XML, RTF, ipynb），可以實現不同的文件解析策略，提高代碼的靈活性和可擴展性。
*   **單例模式 (Singleton Pattern)：** 對於 AI 模型的實例化，考慮使用單例模式來管理，以避免重複初始化和優化資源使用。

## 組件關係
*   **Flet UI 與後端邏輯：** Flet 介面將通過事件處理器觸發後端邏輯層的功能（如文件上傳處理函數）。
*   **後端邏輯與 AI 服務：** 後端邏輯層將作為客戶端，調用 `google-genai` SDK 來與 Google Gemini API 進行通信。
*   **文件處理模塊：** 獨立的模塊負責處理特定文件格式的讀取和預處理，並將純文本或結構化內容傳遞給 AI 處理流程。

## 關鍵實現路徑
1.  **文件上傳流程：**
    *   使用者在 UI 選擇本地文件或輸入 URL。
    *   Flet 的 `FilePicker` 或 HTTP 請求處理模塊獲取文件內容。
    *   文件內容被傳遞給後端邏輯層的文件解析器。
2.  **AI 轉換流程：**
    *   解析器提取的內容和使用者選定的提示被組合成請求。
    *   `google-genai` SDK 將請求發送給 Gemini API。
    *   接收 Gemini API 返回的 Markdown 內容。
3.  **結果呈現與保存：**
    *   轉換後的 Markdown 內容在 Flet UI 中顯示。
    *   提供按鈕供使用者將 Markdown 內容保存為 `.md` 文件到本地。