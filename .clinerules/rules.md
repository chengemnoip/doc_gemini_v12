## I. 核心行為準則：
1.  **回應語言：** 所有與使用者的互動及最終輸出，都必須使用「繁體中文」。
2.  **遵守專案描述：** 在處理任何任務時，必須嚴格遵守當前對話或任務上下文中提供的相關專案描述檔案的內容、規範與限制。

## II. 環境管理：
1.  **執行環境：** 你的執行作業系統為 Windows 10 x64，預設 shell 為 PowerShell7(pwsh)。
### A. Python (uv)
1.  **Python 套件管理：**
    *   在 Python 專案中，應優先使用 `uv` 取代 `pip` 進行套件管理。例如，使用 `uv add <package_name>` 取代 `pip install <package_name>`。**請勿使用 `uv pip install` 來增加套件。**
2.  **Python 腳本執行：**
    *   執行 Python 腳本時，應優先使用 `uv run <script_name.py>` 取代 `python <script_name.py>`。

### B. Node.js (pnpm)
1.  **套件管理：**
    *   在 Node.js 專案中，應優先使用 `pnpm` 作為套件管理器。
    *   **安裝所有依賴：** `pnpm install`
    *   **新增正式依賴：** `pnpm add <package_name>`
    *   **新增開發依賴：** `pnpm add -D <package_name>`
    *   **移除依賴：** `pnpm remove <package_name>`
2.  **腳本執行：**
    *   應優先使用 `pnpm <script_name>` 來執行 `package.json` 中定義的腳本。

### C. Git 操作規範
1.  **確認 `.gitignore` 檔案：** 再次確認根目錄的 `.gitignore` 檔案內容是正確的。
2.  **清空 Git 索引：** 執行 `git rm -r --cached .`。
3.  **重新暫存所有檔案：** 執行 `git add .`。此時，Git 會根據 `.gitignore` 重新追蹤檔案。
4.  **提交變更：** 執行 `git commit -m "Rebuild Git index based on .gitignore and remove unwanted folders"`。
5.  **強制推送到遠端儲存庫：** 執行 `git push --force origin `。

## III. MCP (模型/情境協議) 使用策略：
1.  **時間與日期處理：**
    *   當使用者的提示詞明確涉及時間、日期查詢或需要基於特定時間點的上下文時，你必須啟用並使用 `Time` MCP ，時間參考基準必須設定為「Taipei Time」(台北時間，UTC+8)。
2.  **技術資訊獲取：**
    *   **主要來源：** 針對任何技術性問題、程式碼範例、程式碼解釋、架構分析等，應優先使用 `context7 `和 `gitmcp` MCP 作為主要資訊來源。
    *   **次要來源/備援：** 若 `context7 `和 `gitmcp` MCP 無法提供所需技術資訊，或資訊不足，或查詢的是非技術性的一般資訊，則必須使用 `search-scrape-map-google-plan` MCP 進行網絡查找以獲取補充資訊，若擷取失敗則使用 `puppeteer` MCP 。

## IV. 輸出格式規範：
1.  **JSON 檔案內容：**
    *   當被要求生成或修改 JSON 檔案時，輸出的 JSON 內容中絕對不應包含任何形式的註解。
2.  **比較表格呈現：**
    *   不應直接在聊天視窗中以純文字或非結構化方式顯示任何比較表格。
    *   所有比較表格都必須格式化為 Markdown (`.md`) 檔案的內容將其儲存為 `.md` 檔案。
3.  **通用編碼格式：**
    *   所有由你生成的輸出內容，包括但不限於指令文本、文檔內容（如 Markdown）、程式碼片段等，都必須明確指定或確保其編碼格式為 **UTF-8 (無 BOM)**。

## V. 總體要求：
*   嚴格遵循上述所有指令。
*   優先確保任務的準確性和完整性。
