# 技術情境 (Tech Context)

## 使用的技術
本專案將主要基於以下技術棧進行開發：

*   **核心程式語言：** Python 3.9 或更高版本。
*   **GUI 框架：** Flet (建議使用最新穩定版本)。
    *   **核心概念：** Flet 是一個基於 Google Flutter 的開源框架，允許開發者使用 Python 等語言構建實時、多平台應用程式（Web, Desktop, Mobile）。它透過一個 DOM 伺服器 (Fletd) 將 Python 端的 UI 變化轉換為 Flutter 小部件，實現跨平台渲染。
    *   **UI 定義：** 必須在 Python 程式碼中，使用 `ft` (例如 `ft.Text`, `ft.ElevatedButton`) 以宣告式語法構建使用者介面。
    *   **關鍵控制項：** 包括 `Container`, `Row`, `Column`, `Stack`, `Text`, `Icon`, `Image`, `ListView`, `GridView`, `Card`, `Divider`, `Slider` 等。
*   **AI SDK：** Google Gen AI Python SDK (`google-genai`) (建議使用最新穩定版本)。
    *   **重要提示：** 這是 `google-generativeai` 的新版本，應優先使用 `google-genai`。
    *   **核心功能：**
        *   **內容生成 (`generate_content`)：** 支援多模態輸入，可處理文字、圖片、音訊、影片和 PDF 文件（最多 1000 頁）。
        *   **Files API：** 用於上傳和管理大型媒體檔案（音訊、圖片、影片、文件等，最大 50MB/檔案，總計 20GB/專案），檔案可儲存 48 小時。對於超過 20MB 的請求，必須使用 Files API。
        *   **安全設定：** 可配置安全設定 (`safety_settings`) 來控制模型的回應。
        *   **函式呼叫 (`Function Calling`)：** 允許模型呼叫 Python 函式，實現與外部工具的互動。
        *   **快取 (`Caches`)：** 支援快取內容以優化重複請求的性能。
        *   **模型微調 (`Tunings`)：** 支援對模型進行微調以適應特定任務。
    *   **客戶端創建：**
        ```python
        from google import genai
        # For Gemini Developer API
        client = genai.Client(api_key='YOUR_GEMINI_API_KEY')
        # For Vertex AI API
        # client = genai.Client(vertexai=True, project='your-project-id', location='us-central1')
        ```
*   **HTTP 請求庫：** `requests` (用於處理 URL 文件上傳)。
*   **PDF 處理庫：** `PyPDF2` 或 `fitz` (PyMuPDF) (用於從 PDF 文件中提取文本內容)。
*   **打包工具：** PyInstaller (底層由 `flet pack` 命令調用)。
*   **套件管理：** `uv` (優先於 `pip` 使用)。

## 開發環境設定
建議的開發環境配置：

1.  **Python 環境：** 使用 `uv` 創建和管理 Python 虛擬環境，以隔離專案依賴。
    *   創建虛擬環境：`uv venv`
    *   激活虛擬環境：根據作業系統指示
2.  **依賴安裝：** 在激活的虛擬環境中，使用 `uv add` 安裝所有專案依賴。
    *   `uv add flet google-genai requests PyPDF2` (或 `uv add flet google-genai requests PyMuPDF`)
3.  **整合開發環境 (IDE)：** 推薦使用 Visual Studio Code，並安裝相關的 Python 擴展。

## 技術限制與考量
1.  **Flet 跨平台兼容性：** 雖然 Flet 支援多平台，但在不同作業系統上可能會遇到特定的 UI 或打包問題，需要進行測試和調適。
2.  **Google Gemini API 速率限制與成本：**
    *   需要了解 Gemini API 的使用限制（如每分鐘請求數、每分鐘令牌數）和計費模式，以避免超額使用和產生不必要的費用。
    *   對於大量文件轉換，可能需要考慮異步處理或批次處理機制。
3.  **大文件處理性能：**
    *   對於非常大的文件（如大型 PDF 或日誌文件），文件讀取、傳輸到 AI 服務以及 AI 處理的延遲可能會增加。需要優化文件分塊處理或流式處理。Files API 將是處理大文件的關鍵。
4.  **複雜文件格式解析挑戰：**
    *   PDF、RTF、ipynb 等格式的結構複雜，精確地提取所有內容（包括圖片、表格、特定格式）並轉換為語義豐富的 Markdown 可能會是挑戰。AI 模型在理解這些複雜結構方面將扮演關鍵角色。
5.  **API 金鑰安全：**
    *   API 金鑰應透過環境變數安全加載，而不是硬編碼在程式碼中。在打包應用程式時，也需要確保金鑰管理的安全機制。

## 依賴項
主要的 Python 依賴庫包括：
*   `flet`
*   `google-genai`
*   `requests`
*   `PyPDF2` (或 `PyMuPDF`)

## 工具使用模式
*   **套件管理：**
    *   安裝所有依賴：`uv sync` (在 `requirements.txt` 存在時) 或 `uv add <package_name>`。
    *   新增依賴：`uv add <package_name>`。
*   **開發與測試：**
    *   運行 Flet 應用程式：`flet run main.py` (假設主應用程式入口為 `main.py`)。
*   **桌面應用打包：**
    *   生成獨立執行檔：`flet pack main.py`。
*   **Web 應用發布：**
    *   發布為網頁應用：`flet publish main.py` (未來擴展時使用)。