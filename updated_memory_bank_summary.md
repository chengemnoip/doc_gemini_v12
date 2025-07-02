# 更新後的記憶庫摘要

## 技術情境 (Tech Context)

### 使用的技術
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

### 開發環境設定
建議的開發環境配置：

1.  **Python 環境：** 使用 `uv` 創建和管理 Python 虛擬環境，以隔離專案依賴。
    *   創建虛擬環境：`uv venv`
    *   激活虛擬環境：根據作業系統指示
2.  **依賴安裝：** 在激活的虛擬環境中，使用 `uv add` 安裝所有專案依賴。
    *   `uv add flet google-genai requests PyPDF2` (或 `uv add flet google-genai requests PyMuPDF`)
3.  **整合開發環境 (IDE)：** 推薦使用 Visual Studio Code，並安裝相關的 Python 擴展。

### 技術限制與考量
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

### 依賴項
主要的 Python 依賴庫包括：
*   `flet`
*   `google-genai`
*   `requests`
*   `PyPDF2` (或 `PyMuPDF`)

### 工具使用模式
*   **套件管理：**
    *   安裝所有依賴：`uv sync` (在 `requirements.txt` 存在時) 或 `uv add <package_name>`。
    *   新增依賴：`uv add <package_name>`。
*   **開發與測試：**
    *   運行 Flet 應用程式：`flet run main.py` (假設主應用程式入口為 `main.py`)。
*   **桌面應用打包：**
    *   生成獨立執行檔：`flet pack main.py`。
*   **Web 應用發布：**
    *   發布為網頁應用：`flet publish main.py` (未來擴展時使用)。

---

## 活躍情境 (Active Context)

### 當前工作焦點
本階段的核心工作焦點是更新記憶庫以反映前期研究和規劃的完成，並準備進入應用程式的具體設計與開發階段。

### 近期變更
*   **記憶庫初始化完成：** 已成功在專案根目錄下創建 `memory_bank/` 資料夾，並創建並填充了所有核心記憶庫文件（`projectbrief.md`、`productContext.md`、`systemPatterns.md`、`techContext.md`、`activeContext.md` 和 `progress.md`）。
*   **`docling_docs/` 文件研究完成：** 已詳細閱讀並提取了 `docling_docs/document-processing_python.pdf`、`docling_docs/Files-API@python.pdf` 和 `docling_docs/Google Gen AI Python SDK.pdf` 這三份 PDF 文件的內容，深入理解了 Gemini API 在文件處理和 Files API 方面的能力。
*   **Google Gen AI Python SDK 知識補充完成：** 透過 `python-genai` MCP 查詢，補充了關於 `google-genai` SDK 的安裝與初始化、Files API 文件上傳、`generate_content` 內容生成、API 金鑰安全管理、函式呼叫和錯誤處理等方面的詳細知識和程式碼範例。確認了應使用 `google-genai` 而非舊版 `google-generativeai` SDK。
*   **Flet 框架知識補充完成：** 透過 `flet` MCP 查詢，補充了關於 Flet 框架的安裝與基本使用、常用 UI 組件（例如 `Text`, `ListView`）、事件處理、文件選擇器 (`FilePicker`)、佈局與響應式設計以及應用程式打包 (`flet pack`) 等方面的詳細知識和程式碼範例。理解了 Flet 基於 Flutter 的特性。

### 下一步
1.  **詳細設計：** 基於所有已獲得的知識，設計應用程式的詳細架構和關鍵模塊，特別是文件解析和 AI 交互部分。這將包括決定具體的文件解析庫（例如針對 PDF、RTF、ipynb 等）、API 調用流程和錯誤處理策略。
2.  **核心功能實現 - 文件處理模塊：** 開始編寫能夠讀取和預處理各種文件格式的 Python 模塊。
3.  **核心功能實現 - Flet UI：** 開發 Flet 使用者介面，包括文件上傳按鈕、URL 輸入框、模型選擇下拉菜單、提示輸入區域和結果顯示區域。
4.  **核心功能實現 - AI 交互：** 集成 `google-genai` SDK，實現將預處理過的文件內容和使用者提示傳遞給 Gemini 模型，並接收和處理返回的 Markdown 內容。
5.  **安全實踐：** 實施 API 金鑰的安全加載機制（例如使用環境變數）。

### 活動決策與考量
*   **文件解析庫的選擇：** 需根據研究結果確定最適合處理 PDF、RTF、ipynb 等複雜文件格式的 Python 庫，並考慮其性能和兼容性。初步傾向於 `PyPDF2` 或 `PyMuPDF` 處理 PDF。
*   **UI/UX 流程優化：** 確保使用者上傳文件、選擇模型和獲取結果的流程盡可能流暢和直觀。
*   **異步操作：** 考慮在文件處理和 AI 交互等耗時操作中使用 Flet 的異步功能，以保持 UI 的響應性。
*   **錯誤處理與使用者反饋：** 設計健壯的錯誤處理機制，並在 UI 中向使用者提供清晰的進度指示和錯誤信息。
*   **大型文件處理：** 確認 Files API 是處理大型文件（超過 20MB）的標準方法，這將納入設計考量。

### 學習與專案洞察
*   Google Gemini API 的 Files API 是處理大型文件的關鍵，它允許上傳文件並通過文件 ID 引用，而無需在每次請求中發送整個文件內容。這對於優化性能和降低延遲至關重要。
*   Flet 框架的宣告式 UI 設計和與 Python 的無縫集成使其成為快速開發桌面和 Web 應用程式的理想選擇。其 `FilePicker` 組件將是實現文件上傳功能的關鍵。Flet 基於 Flutter，其 UI 概念與 Flutter 相似。
*   API 金鑰的安全性不容忽視，必須透過環境變數等方式進行管理，以防止敏感信息洩露。
*   多模態輸入 (文件 + 文本提示) 是 Gemini 模型的一個強大特性，將被充分利用來實現智能化的文件轉換。
*   需要注意 `google-genai` 是新版 SDK，避免混淆和使用舊版 `google-generativeai`。

---

## 進度 (Progress)

### 已完成的工作
*   **記憶庫初始化：**
    *   已成功在專案根目錄下創建了 `memory_bank/` 資料夾。
    *   已在 `memory_bank/` 資料夾中成功創建並填充了所有核心文件：`projectbrief.md`、`productContext.md`、`systemPatterns.md`、`techContext.md`、`activeContext.md` 和 `progress.md`。
*   **知識獲取與研究：**
    *   詳細閱讀並研究了 `docling_docs/` 資料夾中的現有文件（`document-processing_python.pdf`、`Files-API@python.pdf`、`Google Gen AI Python SDK.pdf`），對 Gemini API 的文件處理和 Files API 有了深入理解。
    *   使用 `python-genai` MCP 查詢並補充了關於 'Google Gen AI Python SDK' 的相關知識文件和程式碼範例，確認使用新版 SDK。
    *   使用 `flet` MCP 查詢並補充了關於 'Flet 框架' 的相關知識文件和程式碼範例，了解其基於 Flutter 的特性和 UI 概念。

### 待辦事項 (Remaining Tasks)
*   **詳細設計：** 基於所有已獲得的知識，設計應用程式的詳細架構和關鍵模塊，特別是文件解析和 AI 交互部分。這將包括決定具體的文件解析庫（例如針對 PDF、RTF、ipynb 等）、API 調用流程和錯誤處理策略。
*   **核心功能實現 - 文件處理模塊：** 開始編寫能夠讀取和預處理各種文件格式的 Python 模塊。
*   **核心功能實現 - Flet UI：** 開發 Flet 使用者介面，包括文件上傳按鈕、URL 輸入框、模型選擇下拉菜單、提示輸入區域和結果顯示區域。
*   **核心功能實現 - AI 交互：** 集成 `google-genai` SDK，實現將預處理過的文件內容和使用者提示傳遞給 Gemini 模型，並接收和處理返回的 Markdown 內容。
*   **安全實踐：** 實施 API 金鑰的安全加載機制（例如使用環境變數）。
*   **打包與部署：** 使用 `flet pack` 將應用程式打包成獨立執行檔。
*   **測試與優化：** 進行功能測試、性能測試和安全測試。
*   **文檔更新：** 根據開發進度持續更新記憶庫文件。

### 當前狀態
專案目前已完成 **記憶庫初始化** 和 **前期知識研究** 階段。所有必要的背景信息、產品願景、技術細節和工具使用模式都已記錄在記憶庫中。現在準備進入 **應用程式的詳細設計與核心功能實現** 階段。

### 已知問題
*   文件解析的複雜性（特別是對於非純文本格式如 PDF、RTF、ipynb）仍是潛在的挑戰，需要仔細評估和選擇合適的庫。
*   Google Gemini API 的速率限制和成本管理需要在開發過程中持續關注。
*   API 金鑰的安全處理需要嚴謹的設計和實現。

### 專案決策演進
*   **確認核心技術棧：** Flet 作為 GUI 框架，Google Gen AI Python SDK (`google-genai`) 作為 AI 交互核心，PyInstaller 透過 `flet pack` 進行打包。
*   **文件上傳策略：** 將主要使用 Files API 處理文件上傳，以支持大型文件和各種文件類型。
*   **API 金鑰安全：** 確定使用環境變數作為 API 金鑰的主要管理方式。
*   **AI 模型選擇：** 應用程式將提供 `gemini-2.5-flash` 和 `gemini-2.5-pro` 作為模型選項。
*   **SDK 版本確認：** 明確使用 `google-genai` 作為 Gemini API 的 Python SDK。