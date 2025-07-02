### **# Flet 技術情境**

#### **## 技術棧 (Tech Stack)**
*   **程式語言 (Language):** Python
*   **GUI 框架 (Framework):** Flet
*   **UI 渲染引擎 (UI Engine):** Flutter (此為 Flet 內建，不可替換)
*   **打包與部署工具 (Packaging):** PyInstaller (由 `flet pack` 指令在底層調用)

#### **## 核心依賴項 (Primary Dependencies)**
*   `flet`: 框架本身。
*   `pyinstaller`: `flet pack` 命令的底層依賴，用於生成獨立執行檔。

#### **## 所需依賴庫/套件 (Required Dependency Packages)**
*   **HTTP 請求:** `requests`
*   **數據處理:** `pandas`
*   **Excel 操作:** `openpyxl`
*   **圖表生成:** `matplotlib`
*   **圖像處理:** `Pillow`

#### **## 核心開發與部署模式 (Core Development & Deployment Patterns)**
*   **UI 定義:** 必須在 Python 程式碼中，使用 `ft` (例如 `ft.Text`, `ft.ElevatedButton`) 以宣告式語法構建使用者介面。
*   **核心架構理解:** 必須基於 **`Python (應用邏輯) -> Fletd (橋樑) -> Flutter (UI渲染)`** 的模型來解釋其運作原理。
*   **桌面應用部署:** 為終端使用者創建獨立執行檔的**唯一標準方法**是使用 `flet pack your_app.py` 命令。
*   **Web 應用部署:** 發布為網頁應用的標準方法是使用 `flet publish your_app.py` 命令。