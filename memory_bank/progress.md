# 進度 (Progress)

## 已完成的工作
*   **記憶庫初始化：**
    *   已成功在專案根目錄下創建了 `memory_bank/` 資料夾。
    *   已在 `memory_bank/` 資料夾中成功創建並填充了所有核心文件：`projectbrief.md`、`productContext.md`、`systemPatterns.md`、`techContext.md`、`activeContext.md` 和 `progress.md`。
*   **知識獲取與研究：**
    *   詳細閱讀並研究了 `docling_docs/` 資料夾中的現有文件（`document-processing_python.pdf`、`Files-API@python.pdf`、`Google Gen AI Python SDK.pdf`），對 Gemini API 的文件處理和 Files API 有了深入理解。
    *   使用 `python-genai` MCP 查詢並補充了關於 'Google Gen AI Python SDK' 的相關知識文件和程式碼範例，確認使用新版 SDK。
    *   使用 `flet` MCP 查詢並補充了關於 'Flet 框架' 的相關知識文件和程式碼範例，了解其基於 Flutter 的特性和 UI 概念。
*   **環境設置與依賴安裝：** 已確保基本的 Python 環境和依賴（包括 `flet`, `google-genai`, `requests`, `python-dotenv`）已設置，並創建了 `example.env`。
*   **Flet UI 初步功能實現與錯誤修正及功能實作：**
    *   修正了 `ft.icons` 的使用錯誤，應用程式現在可以正常啟動。
    *   增強了 `GEMINI_API_KEY` 未設置時的錯誤處理，會在 Flet 介面顯示友好的提示。
    *   修正了 `ft.colors` 的使用錯誤。
    *   修正了 `google-genai` 客戶端獲取模型列表的異步方法問題 (`list_models_async`)。
    *   修正了 `main(page)` 函數的重複定義問題。
    *   解決了 `UnboundLocalError`，調整了 `on_file_picked` 和 `process_document` 函數的定義位置和調用方式。
    *   修正了 `'Client' object has no attribute 'GenerativeModel'` 錯誤，現在 `GenerativeModel` 被正確調用。
    *   解決了 `RuntimeWarning: coroutine ... was never awaited` 警告，確保 Flet 異步事件處理的正確性。
    *   更新了 `prompt_input` 的預設提示詞內容。
    *   調整 UI 顯示邏輯，不再直接顯示轉換後的 Markdown 內容，僅提供下載選項。
    *   修正了 `AttributeError: 'Page' object has no attribute 'open_snack_bar'` 錯誤，現在 `SnackBar` 被正確顯示。
    *   修正了下載功能，現在使用 `FilePicker.save_file` 來觸發另存檔案對話框，並解決了 `RuntimeWarning`。
    *   將「下載 Markdown」按鈕在 UI 中置中顯示。
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
        *   **`.ipynb` 文件處理：** 成功實現了將 `.ipynb` 文件內容解析為純文本的功能，並將其 MIME 類型設置為 `text/plain`，解決了 Gemini API 不支持 `application/vnd.jupyter` MIME 類型的問題。
        *   **文件上傳方式優化：** 將 `main.py` 中的文件上傳方式從 `gemini_client.aio.files.upload` 調整為直接使用 `types.Part.from_bytes`，提高了文件上傳的兼容性和可靠性。

## 待辦事項 (Remaining Tasks)
*   **功能測試與驗證：** 運行應用程式並使用不同類型文件（本地文件、URL 文件）進行測試，確保所有功能按預期工作，特別是文件上傳、AI 處理和結果下載。
*   **性能優化：** 對於大型文件或高頻次請求，考慮進一步的性能優化（例如，對 `document_parser` 進行異步化處理，或者對 API 調用進行重試機制）。
*   **錯誤處理增強：** 細化錯誤處理邏輯，為使用者提供更具體和可操作的錯誤信息。
*   **打包與部署：** 準備使用 `flet pack` 將應用程式打包成獨立執行檔。
*   **文檔更新：** 根據最終的程式碼和最佳實踐，全面更新記憶庫文件。

## 當前狀態
專案目前已完成 **記憶庫初始化**、**前期知識研究** 和 **環境設置與初步 UI 錯誤修正** 階段。核心技術棧已確認，應用程式骨架已能啟動。現在準備進入 **應用程式的詳細設計與核心功能實現** 階段。

## 已知問題
*   文件解析的複雜性（特別是對於非純文本格式如 PDF、RTF、ipynb）仍是潛在的挑戰，需要仔細評估和選擇合適的庫。
*   Google Gemini API 的速率限制和成本管理需要在開發過程中持續關注。
*   API 金鑰的安全處理需要嚴謹的設計和實現。

## 專案決策演進
*   **確認核心技術棧：** Flet 作為 GUI 框架，Google Gen AI Python SDK (`google-genai`) 作為 AI 交互核心，PyInstaller 透過 `flet pack` 進行打包。
*   **文件上傳策略：** 將主要使用 Files API 處理文件上傳，以支持大型文件和各種文件類型。
*   **API 金鑰安全：** 確定使用環境變數作為 API 金鑰的主要管理方式，並導入 `python-dotenv` 協助加載。
*   **AI 模型選擇：** 應用程式將提供 `gemini-2.5-flash` 和 `gemini-2.5-pro` 作為模型選項。
*   **SDK 版本確認：** 明確使用 `google-genai` 作為 Gemini API 的 Python SDK。
*   **UI 圖示修正：** `ft.icons` 已修正為 `ft.Icons`。
*   **UI 顏色修正：** `ft.colors` 已修正為 `ft.Colors`。
*   **Gemini 客戶端初始化：** 修正 `gemini_client.GenerativeModel` 為 `genai.GenerativeModel`。
*   **Flet 異步事件處理：** 採用直接將異步函數賦值給事件處理器（例如 `on_result=on_file_picked`），並在異步函數內部使用 `await` 調用其他協程，而非在 `lambda` 中包裝 `page.run_task`。解決了 `RuntimeError` 和 `AssertionError`。
*   **函數定義順序：** 調整了 `on_file_picked` 和 `process_document` 函數的定義位置，以解決 `UnboundLocalError`。
*   **預設提示詞：** 更新了 `prompt_input` 的預設提示詞內容，以包含更詳細的轉換規則。
*   **會話管理：** 修正 `page.session.get("key", "default")` 為 `(page.session.get("key") or "default")`。
*   **UI 互動邏輯：** 調整文件選擇和 URL 輸入後不立即處理，而是等待明確的處理按鈕點擊。
*   **LLM 提示詞管理：** 移除了硬編碼的提示詞添加，並確保 `prompt_input.value` 正確傳遞。
*   **終端輸出：** 移除了調試用的 `DEBUG` 列印語句。
*   **文件上傳至 LLM：** 確定直接將文件上傳到 LLM，並解決了相關的 `Files.upload()` 參數、`mimetypes.add_defaults()`、異步調用 (`gemini_client.aio.files.upload`) 和 `types.Part.from_uri()` 轉換問題。
*   **URL 文件處理：** `document_parser.py` 修改為將 URL 內容下載到臨時文件，然後由 `main.py` 上傳並清理。
*   **`main.py` 程式碼結構：** 函數 (`get_available_models_internal`, `process_document`, `on_file_save_result`, `on_file_picked_wrapper`, `on_process_url_click`, `on_process_file_click`, `download_markdown`) 經過大量修改以實現 UI 和 LLM 互動邏輯。
*   **`document_parser.py` 程式碼結構：** 移除了文字解析邏輯，專注於獲取文件資訊和 URL 臨時文件處理。
*   **`.ipynb` 文件處理策略：** 決定將 `.ipynb` 文件轉換為純文本（提取程式碼和 Markdown 內容）並以 `text/plain` MIME 類型上傳，以解決 Gemini API 不支持其原生 MIME 類型問題。
*   **文件上傳機制調整：** 優先使用 `types.Part.from_bytes` 將本地文件內容作為 bytes 直接傳遞給 `generate_content`，而非透過 `files.upload` 預先上傳。