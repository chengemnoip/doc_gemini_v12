# 活躍情境 (Active Context)

## 當前工作焦點
本階段的核心工作焦點是更新記憶庫以反映前期研究和規劃的完成，並準備進入應用程式的具體設計與開發階段。

## 近期變更
*   **記憶庫初始化完成：** 已成功在專案根目錄下創建 `memory_bank/` 資料夾，並創建並填充了所有核心記憶庫文件（`projectbrief.md`、`productContext.md`、`systemPatterns.md`、`techContext.md`、`activeContext.md` 和 `progress.md`）。
*   **`docling_docs/` 文件研究完成：** 已詳細閱讀並提取了 `docling_docs/document-processing_python.pdf`、`docling_docs/Files-API@python.pdf` 和 `docling_docs/Google Gen AI Python SDK.pdf` 這三份 PDF 文件的內容，深入理解了 Gemini API 在文件處理和 Files API 方面的能力。
*   **Google Gen AI Python SDK 知識補充完成：** 透過 `python-genai` MCP 查詢，補充了關於 `google-genai` SDK 的安裝與初始化、Files API 文件上傳、`generate_content` 內容生成、API 金鑰安全管理、函式呼叫和錯誤處理等方面的詳細知識和程式碼範例。確認了應使用 `google-genai` 而非舊版 `google-generativeai` SDK。
*   **Flet 框架知識補充完成：** 透過 `flet` MCP 查詢，補充了關於 Flet 框架的安裝與基本使用、常用 UI 組件（例如 `Text`, `ListView`）、事件處理、文件選擇器 (`FilePicker`)、佈局與響應式設計以及應用程式打包 (`flet pack`) 等方面的詳細知識和程式碼範例。理解了 Flet 基於 Flutter 的特性。
*   **環境設置與初步 UI 錯誤修正及功能實作：**
    *   安裝了 `python-dotenv` 庫。
    *   創建了 `example.env` 文件以引導使用者設置 API 金鑰。
    *   修正了 Flet 應用程式中 `ft.icons` 的 `AttributeError`，改為使用 `ft.Icons`。
    *   修正了 `ft.colors` 的 `AttributeError`，改為使用 `ft.Colors`。
    *   實施了更友好的 `GEMINI_API_KEY` 環境變數缺失提示，會在應用程式 UI 中顯示 SnackBar 警告。
    *   修正了 `google-genai` 客戶端獲取模型列表的異步方法問題 (`list_models_async`)。
    *   修正了 `main(page)` 函數的重複定義問題。
    *   解決了 Flet 異步事件處理的 `AssertionError` 和 `RuntimeError: no running event loop`，調整了異步函數調用方式。
    *   解決了 `UnboundLocalError`，調整了 `on_file_picked` 和 `process_document` 函數的定義位置。
    *   修正了 `'Client' object has no attribute 'GenerativeModel'` 錯誤，確保 `genai.GenerativeModel` 的正確使用。
    *   更新了 `prompt_input` 的預設提示詞內容，以包含更詳細的轉換規則。
    *   **UI 顯示邏輯調整：** 在文件處理成功後，不再直接在 UI 上顯示轉換後的 Markdown 內容，僅提供下載按鈕。
    *   **SnackBar 顯示錯誤修正：** 修正了 `page.open_snack_bar()` 錯誤，現在 `SnackBar` 通過 `page.snack_bar.open = True` 和 `page.update()` 正確顯示。
    *   **下載功能改進：** 使用 `ft.FilePicker` 的 `save_file` 模式實現文件保存對話框，解決了先前下載無反應的問題。
    *   **UI 佈局調整：** 將「下載 Markdown」按鈕置中顯示。
    *   **`TypeError: SessionStorage.get() takes 2 positional arguments but 3 were given`**: 透過將 `page.session.get("key", "default")` 修正為 `(page.session.get("key") or "default")` 解決。
    *   **UI 互動邏輯 (自動啟動任務)**: 修改 `on_file_picked_wrapper` 和 `on_process_url_click`，使其僅將選定的文件路徑/URL 儲存在 `page.session` 中並更新 UI，而不立即呼叫 `process_document`。`on_process_file_click` 處理器現在檢索儲存的路徑/URL 並啟動 `process_document`。
    *   **預設提示詞未傳遞給 LLM**: 透過添加列印語句進行調試，然後透過確保 `prompt_input.value` 正確包含在 `full_prompt` 中解決。
    *   **硬編碼的提示詞添加**: 根據使用者要求移除了 `full_prompt += "\n請將上述文件內容轉換為結構良好且易於閱讀的 Markdown 格式。"`。
    *   **過多的終端輸出**: 移除了 `DEBUG` 列印語句。
    *   **文件處理順序 (預提取 vs. 直接 LLM 上傳)**: 使用者要求直接將文件上傳到 LLM。
        *   **`Files.upload() got an unexpected keyword argument 'mime_type'`**: 透過從 `gemini_client.files.upload()` 呼叫中移除 `mime_type` 解決，因為它不是直接參數。
        *   **`AttributeError: module 'mimetypes' has no attribute 'add_defaults'`**: 透過移除 `document_parser.py` 中的 `mimetypes.add_defaults()` 呼叫解決。
        *   **`Files.upload() takes 1 positional argument but 2 were given`**: 透過將 `gemini_client.files.upload(file_path)` 更改為 `gemini_client.files.upload(file=file_path)`，使用關鍵字參數解決。
        *   **`object File can't be used in 'await' expression` (第一次出現)**: 透過將 `gemini_client.files.upload` 更改為 `gemini_client.aio.files.upload` (使用異步客戶端的文件上傳方法) 解決。
        *   **`object File can't be used in 'await' expression` (第二次出現)**: 透過將 `gemini_client.aio.files.upload` 返回的 `File` 物件明確轉換為 `types.Part` 物件，使用 `types.Part.from_uri(file_uri=uploaded_file.uri, mime_type=content_mime_type)` 解決。
        *   **`Part.from_uri() takes 1 positional argument but 2 were given`**: 透過確保 `types.Part.from_uri()` 的 `file_uri` 和 `mime_type` 都作為關鍵字參數傳遞解決。
        *   **URL 處理 for `files.upload`**: 修改 `document_parser.py` 以將 URL 內容保存到臨時文件並返回其路徑，然後 `main.py` 上傳此臨時文件並進行清理。
        *   **`.ipynb` 文件處理與 MIME 類型問題解決：** 由於 Gemini API 不支持 `application/vnd.jupyter` MIME 類型，已修改 `document_parser.py` 以將 `.ipynb` 文件內容解析為純文本，並以 `text/plain` MIME 類型傳遞。同時，將 `main.py` 中的文件上傳方式從 `gemini_client.aio.files.upload` 調整為直接使用 `types.Part.from_bytes`，以確保文件內容和 MIME 類型正確傳遞給模型。
    *   **`main.py` 相關變更：**
        *   `main(page)` 函數、內部 `get_available_models_internal()`、`process_document()`、`on_file_save_result()`、`on_file_picked_wrapper()`、`on_process_url_click()`、`on_process_file_click()` 和 `download_markdown()` 函數經過大量修改，以實作 UI 元素、事件處理器和 LLM 互動邏輯。
        *   修正 Flet 圖示/顏色屬性名稱 (`ft.Icons`, `ft.Colors`)、`page.snack_bar` 用法、正確的 `google.genai` 模型調用 (`gemini_client.aio.models.generate_content`)、適當的異步任務管理、動態下載檔案命名，以及詳細的進度/文件路徑顯示。移除了硬編碼的提示詞添加和調試列印語句。
        *   將 `genai.upload_file` 更改為 `gemini_client.aio.files.upload(file=...)`，並將 `contents_for_llm.append(uploaded_file)` 更改為 `contents_for_llm.append(types.Part.from_uri(file_uri=uploaded_file.uri, mime_type=content_mime_type))`。
        *   在 `process_document` 中添加了 `from google.genai import types` 以及 `temp_file_path` 和 `content_mime_type` 變數，並在 `finally` 區塊中添加了 `os.remove(temp_file_path)` 以進行清理。
    *   **`document_parser.py` 相關變更：**
        *   移除了所有文字解析邏輯 (`_parse_pdf`, `_parse_text_file`, `_parse_ipynb` 等)。
        *   `get_file_info` 現在返回 `file_path`、`original_base_name`、`mime_type`。
        *   `get_url_info` 現在將 URL 內容下載到臨時文件，返回其路徑、原始基本名稱和 MIME 類型。
        *   引入了 `tempfile` 和 `mimetypes` 模組。
        *   由於 `AttributeError` 移除了 `mimetypes.add_defaults()`。

## 下一步
*   **功能測試與驗證：** 運行應用程式並使用不同類型文件（本地文件、URL 文件）進行測試，確保所有功能按預期工作，特別是文件上傳、AI 處理和結果下載。
*   **性能優化：** 對於大型文件或高頻次請求，考慮進一步的性能優化（例如，對 `document_parser` 進行異步化處理，或者對 API 調用進行重試機制）。
*   **錯誤處理增強：** 細化錯誤處理邏輯，為使用者提供更具體和可操作的錯誤信息。
*   **打包與部署：** 準備使用 `flet pack` 將應用程式打包成獨立執行檔。
*   **文檔更新：** 根據最終的程式碼和最佳實踐，全面更新記憶庫文件。

## 活動決策與考量
*   **文件解析庫的選擇：** 需根據研究結果確定最適合處理 PDF、RTF 等複雜文件格式的 Python 庫，並考慮其性能和兼容性。對於 `.ipynb` 文件，已決定將其內容提取為純文本並以 `text/plain` 類型傳遞給 Gemini API，以規避 API 不支持 `application/vnd.jupyter` MIME 類型的限制。
*   **UI/UX 流程優化：** 確保使用者上傳文件、選擇模型和獲取結果的流程盡可能流暢和直觀。
*   **異步操作：** 考慮在文件處理和 AI 交互等耗時操作中使用 Flet 的異步功能，以保持 UI 的響應性。
*   **錯誤處理與使用者反饋：** 設計健壯的錯誤處理機制，並在 UI 中向使用者提供清晰的進度指示和錯誤信息。
*   **大型文件處理：** 確認 Files API 是處理大型文件（超過 20MB）的標準方法，這將納入設計考量。
*   **文件處理策略：** 決定直接將文件上傳到 LLM，而非預先提取文本內容。

## 學習與專案洞察
*   Google Gemini API 的 Files API 是處理大型文件的關鍵，它允許上傳文件並通過文件 ID 引用，而無需在每次請求中發送整個文件內容。這對於優化性能和降低延遲至關重要。
*   Flet 框架的宣告式 UI 設計和與 Python 的無縫集成使其成為快速開發桌面和 Web 應用程式的理想選擇。其 `FilePicker` 組件將是實現文件上傳功能的關鍵。Flet 基於 Flutter，其 UI 概念與 Flutter 相似。
*   API 金鑰的安全性不容忽視，必須透過環境變數等方式進行管理，並導入 `python-dotenv` 以便從 `.env` 檔案加載。
*   多模態輸入 (文件 + 文本提示) 是 Gemini 模型的一個強大特性，將被充分利用來實現智能化的文件轉換。
*   需要注意 `google-genai` 是新版 SDK，避免混淆和使用舊版 `google-generativeai`。
*   Flet 的圖示 (`ft.icons`) 屬性實際上是 `ft.Icons`。
*   Flet 的顏色 (`ft.colors`) 屬性實際上是 `ft.Colors`。
*   `google-genai` 中 `GenerativeModel` 應直接從 `genai` 模組導入，而非 `gemini_client` 實例。**已修正為正確調用 `gemini_client.aio.models.generate_content()`。**
*   在 Flet 中處理異步事件時，對於 `on_click` 和 `on_result` 等，如果處理函數是 `async def`，應直接將其賦值給事件處理器（例如 `on_result=my_async_function`），Flet 會自動在底層安排其運行。避免在 `lambda` 中對異步函數的結果再次使用 `page.run_task`，這會導致 `AssertionError` 和 `RuntimeError: no running event loop`。
*   Python 中函數的定義順序很重要，尤其是在引用它們之前，以避免 `UnboundLocalError`。
*   應用程式 UI 的設計應考慮使用者體驗，例如在處理完成後隱藏結果顯示區域，僅提供下載選項。
*   Flet 中 `SnackBar` 的顯示應通過設置 `page.snack_bar.open = True` 並隨後調用 `page.update()` 來實現，而不是使用不存在的 `page.open_snack_bar()` 方法。
*   Flet 的 `FilePicker` 的 `save_file` 模式是觸發原生文件保存對話框的正確方式。
*   在 Flet 中處理異步任務時，確保異步函數被正確地提交給 `page.run_task`，這有助於避免 `RuntimeWarning`。
*   **Flet UI/UX 模式：** 顯示文件路徑/URL、為長時間運行的過程提供分階段的文字描述、以及動態 UI 元素可見性 (例如，下載按鈕)。
*   **提示工程：** 結構化 LLM 提示，包含特定規則 (忽略背景樣式、將表格轉換為 HTML、將 TOC 包裹在程式碼區塊中、直接文字輸出不帶前言)。
*   **文件處理模組 (`document_parser.py`)：** 移除了所有文字解析邏輯，`get_file_info` 和 `get_url_info` 現在主要負責獲取文件路徑、原始基本名稱和 MIME 類型，並處理 URL 內容到臨時文件的下載。
*   **異步程式設計：** Python 的 `asyncio` 和 Flet 的 `page.run_task` 用於管理異步操作以保持 UI 響應性，並傾向於在 `async def` 事件處理器中直接 `await`。
*   **環境管理：** `python-dotenv` 用於從 `.env` 文件載入 API 金鑰，`uv` 用於套件管理。
*   **安全性：** 透過環境變數管理 API 金鑰是最佳實踐。
*   **臨時文件管理：** 使用 `tempfile` 建立和管理 URL 內容的臨時文件，並確保在處理完成後進行清理。
*   **Gemini API 對於 MIME 類型的支持限制：** 發現 Gemini API 不支持 `application/vnd.jupyter` MIME 類型，對於此類文件需要進行預處理（如轉換為純文本）並使用 API 支持的通用 MIME 類型（如 `text/plain`）。
*   **`types.Part.from_bytes` 的重要性：** 對於本地文件，直接讀取文件內容為 bytes 並使用 `types.Part.from_bytes` 配合明確的 MIME 類型是將文件內容傳遞給 Gemini API 的最佳實踐，這比依賴 `files.upload` 更為可靠，尤其是在處理不常見或 API 不直接支持的 MIME 類型時。