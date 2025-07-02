import flet as ft
import os
import json
import requests
import asyncio
import sys # 導入 sys 模組
from google import genai
from google.genai import types # 導入 types 模組
from document_parser import DocumentParser
from dotenv import load_dotenv

# 加載 .env 檔案中的環境變數
load_dotenv()

# 初始化 DocumentParser
parser = DocumentParser()

# 全局變數，用於儲存 Gemini 客戶端實例
# 必須是全局的，以便 get_available_models_internal 和 process_document 可以訪問
gemini_client = None 

async def main(page: ft.Page):
    page.title = "文件處理應用程式"
    page.vertical_alignment = ft.CrossAxisAlignment.START
    # Flet 目前無法跨平台預設最大化，請手動最大化
    # page.window_maximized = True
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.update()

    # 配置 Gemini API 金鑰
    API_KEY = os.getenv("GEMINI_API_KEY")
    global gemini_client # 聲明使用全局變數

    if not API_KEY:
        page.snack_bar = ft.SnackBar(
            ft.Text("錯誤：GEMINI_API_KEY 環境變數未設置。請設置您的 Gemini API 金鑰以使用完整功能。", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED_700,
            open=True
        )
        page.snack_bar.open = True
        page.update()
        gemini_client = None # 確保未設置時為 None
    else:
        try:
            gemini_client = genai.Client(api_key=API_KEY)
        except Exception as e:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"初始化 Gemini 客戶端失敗: {e}", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
                open=True
            )
            page.snack_bar.open = True
            page.update()
            gemini_client = None # 初始化失敗時也設為 None
    
    # 獲取可用的 Gemini 模型 (作為 main 函數的內部函數)
    async def get_available_models_internal():
        if not gemini_client:
            # 如果 gemini_client 未初始化，則無法獲取模型列表
            return []
        
        models = []
        try:
            # 使用 gemini_client.aio.models.list() 獲取異步模型列表
            async for m in await gemini_client.aio.models.list():
                # 使用 getattr 健壯地檢查屬性
                if "generateContent" in getattr(m, 'supported_generation_methods', []):
                    models.append(m.name)
        except Exception as e:
            print(f"獲取可用模型失敗: {e}")
        return sorted(models)

    # UI 顯示元素
    file_path_display = ft.Text("未選擇文件或 URL", size=14, color=ft.Colors.GREY_600)
    status_message_display = ft.Text("", size=14, weight=ft.FontWeight.BOLD)
    
    # 必須在 UI 控制項使用這些函數之前定義
    # process_document 函數定義
    async def process_document(page_ref: ft.Page, file_path: str = None, url: str = None):
        result_display.value = "" # 清空之前的結果
        result_display.update()
        progress_bar.visible = True
        progress_bar.update()
        download_button.visible = False
        download_button.update()
        status_message_display.value = "準備處理文件..."
        status_message_display.update()
 
        contents_for_llm = []
        original_file_base_name = "output" # 預設值
        temp_file_path = None # 用於儲存臨時文件路徑，以便在 finally 中清理
        content_mime_type = None # 用於儲存 MIME 類型

        try:
            if file_path:
                status_message_display.value = "正在準備本地文件進行上傳..."
                status_message_display.update()

                file_info = parser.get_file_info(file_path)
                original_file_base_name = file_info["original_base_name"]
                content_mime_type = file_info["mime_type"] # 儲存 MIME 類型
                
                # 創建 genai.upload_file 物件
                with open(file_info["file_path"], 'rb') as f:
                    file_bytes = f.read()
                contents_for_llm.append(types.Part.from_bytes(data=file_bytes, mime_type=content_mime_type))
                file_path_display.value = f"選擇的文件：{os.path.basename(file_path)}"
                file_path_display.update()
                status_message_display.value = "本地文件準備完成，等待處理。"
                status_message_display.update()

            elif url:
                status_message_display.value = "正在下載 URL 內容並保存為臨時文件..."
                status_message_display.update()

                url_info = parser.get_url_info(url)
                original_file_base_name = url_info["original_base_name"]
                temp_file_path = url_info["file_path"] # 儲存臨時文件路徑
                content_mime_type = url_info["mime_type"] # 儲存 MIME 類型

                # 上傳臨時文件
                with open(temp_file_path, 'rb') as f:
                    file_bytes = f.read()
                contents_for_llm.append(types.Part.from_bytes(data=file_bytes, mime_type=content_mime_type))
                file_path_display.value = f"選擇的 URL：{url}"
                file_path_display.update()
                status_message_display.value = "URL 內容已保存為臨時文件並準備上傳。"
                status_message_display.update()
            else:
                result_display.value = "請選擇一個文件或輸入一個 URL。"
                result_display.update()
                status_message_display.value = "錯誤：未選擇文件。"
                status_message_display.update()
                progress_bar.visible = False
                progress_bar.update()
                return
            
            # 將原始文件基本名稱儲存到 session
            page.session.set("original_base_name", original_file_base_name)

            status_message_display.value = "文件內容準備完成，正在檢查 Gemini 客戶端..."
            status_message_display.update()
 
            if not gemini_client:
                result_display.value = "Gemini API 客戶端未初始化。請設置 GEMINI_API_KEY 環境變數。"
                result_display.update()
                status_message_display.value = "錯誤：API 客戶端未初始化。"
                status_message_display.update()
                progress_bar.visible = False
                progress_bar.update()
                return
            
            status_message_display.value = "正在調用 Gemini AI 模型生成 Markdown..."
            status_message_display.update()
 
            model_name = model_dropdown.value
             
            # 將提示詞作為第一個 'text' 部分添加到 contents_for_llm
            full_prompt_text = f"使用者指令：{prompt_input.value}"
            contents_for_llm.insert(0, full_prompt_text) # 將提示詞放在最前面
 
            # 直接使用 gemini_client.aio.models.generate_content() 調用
            # 如果模型不支持文件輸入，這裡可能會報錯
            response = await gemini_client.aio.models.generate_content(
                model=model_name, contents=contents_for_llm
            )
             
            markdown_output = response.text
            status_message_display.value = "Markdown 內容已成功生成！"
            status_message_display.update()
            download_button.visible = True
            download_button.update()
            # 將生成內容暫存，以便下載時使用
            page.session.set("markdown_output", markdown_output)
 
        except Exception as ex:
            result_display.value = f"處理文件時發生錯誤: {ex}"
            download_button.visible = False
            status_message_display.value = f"處理失敗: {ex}"
            status_message_display.update()
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path) # 清理臨時文件
            result_display.update()
            progress_bar.visible = False
            progress_bar.update()
            download_button.update()
 
    # 文件保存的回調函數
    def on_file_save_result(e: ft.FilePickerResultEvent):
        if e.path:
            try:
                content_to_save = page.session.get("markdown_output")
                if content_to_save:
                    with open(e.path, "w", encoding="utf-8") as f:
                        f.write(content_to_save)
                    page.snack_bar = ft.SnackBar(ft.Text(f"Markdown 已保存到: {e.path}"), open=True)
                    page.snack_bar.open = True
                    page.update()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("沒有內容可以保存！"), open=True)
                    page.snack_bar.open = True
                    page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"保存失敗: {ex}"), open=True)
                page.snack_bar.open = True
                page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("文件保存已取消。"), open=True)
            page.snack_bar.open = True
            page.update()

    # 文件選擇器用於保存文件
    file_saver = ft.FilePicker(on_result=on_file_save_result)
    page.overlay.append(file_saver)

    # 文件選擇器用於選擇本地文件
    async def on_file_picked_wrapper(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            page.session.set("selected_file_path", file_path) # 儲存文件路徑
            page.session.set("selected_url", None) # 清除 URL 選擇
            file_path_display.value = f"已選擇文件：{os.path.basename(file_path)}"
            file_path_display.update()
            status_message_display.value = "文件已選擇，等待處理。"
            status_message_display.update()
            # 不再自動調用 process_document

    file_picker = ft.FilePicker(on_result=on_file_picked_wrapper)
    page.overlay.append(file_picker)

    # UI 控制項
    local_file_button = ft.ElevatedButton(
        "上傳本地文件",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(allow_multiple=False)
    )

    async def on_process_url_click(e):
        input_url = url_input.value
        if input_url:
            page.session.set("selected_url", input_url) # 儲存 URL
            page.session.set("selected_file_path", None) # 清除文件路徑選擇
            file_path_display.value = f"已輸入 URL：{input_url}"
            file_path_display.update()
            status_message_display.value = "URL 已輸入，等待處理。"
            status_message_display.update()
        else:
            file_path_display.value = "請輸入有效的 URL。"
            file_path_display.update()
            status_message_display.value = "錯誤：未輸入 URL。"
            status_message_display.update()
        # 不再自動調用 process_document

    url_input = ft.TextField(
        label="或輸入文件 URL",
        hint_text="例如: https://example.com/document.pdf",
        width=500
    )
    process_url_button = ft.ElevatedButton(
        "從 URL 處理",
        icon=ft.Icons.LINK,
        on_click=on_process_url_click # 直接調用異步函數
    )
  
    # 模型選擇下拉菜單
    available_models = await get_available_models_internal()
    model_dropdown_options = [
        ft.dropdown.Option("gemini-2.5-flash"),
        ft.dropdown.Option("gemini-2.5-pro")
    ]
    for model_name in available_models:
        if model_name not in ["gemini-2.5-flash", "gemini-2.5-pro"]: # 避免重複添加預設模型
            model_dropdown_options.append(ft.dropdown.Option(model_name))
 
    model_dropdown = ft.Dropdown(
        label="選擇 Gemini 模型",
        options=model_dropdown_options,
        value="gemini-2.5-flash", # 預設值
        width=250
    )
 
    # 提示詞輸入區域
    prompt_input = ft.TextField(
        label="輸入提示詞 (選填)",
        value="將此文件的內容轉換為 Markdown 格式。 在轉換時遵循以下規則：\n1. 忽略文件背景樣式( eg. 顏色、浮水印等)。\n2. 優先將該文件中的表格轉換為 HTML語法來嵌入到 Markdown 中， 確保最終的輸出結果在視覺上盡可能接近原始文件的排版。\n3. 優先將該文件中的目錄文字，用 Markdown 的程式碼區塊（```）完整包裝起來，以保留其原始的排版、點和空白，不要對內容做任何修改，直接輸出結果。\n4. 請嚴格且僅輸出原始的 .md 文件內容。輸出開頭嚴禁包含任何說明文字、註解、引言、前言或寒暄語。唯一允許的內容是1. 2. 3. 的要求 & Markdown 文本。",
        multiline=True,
        min_lines=3,
        max_lines=10,
        width=700
    )
 
    # 結果顯示區域 (保持存在但通常為空，除非顯示錯誤)
    result_display = ft.Markdown(
        "",
        selectable=True,
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        on_tap_link=lambda e: page.launch_url(e.data)
    )
 
    # 進度指示器
    progress_bar = ft.ProgressBar(width=400, visible=False)
 
    # 下載按鈕
    download_button = ft.ElevatedButton(
        "下載 Markdown",
        icon=ft.Icons.DOWNLOAD,
        on_click=lambda _: file_saver.save_file(
            file_name=(page.session.get("original_base_name") or "output") + ".md" # 使用原始檔名
        ), # 觸發保存對話框，帶預設文件名
        visible=False
    )

    async def on_process_file_click(e):
        selected_file_path = page.session.get("selected_file_path")
        selected_url = page.session.get("selected_url")

        if selected_file_path:
            await process_document(page, file_path=selected_file_path)
        elif selected_url:
            await process_document(page, url=selected_url)
        else:
            result_display.value = "請先選擇一個文件或輸入一個 URL。"
            result_display.update()
            status_message_display.value = "錯誤：未選擇文件進行處理。"
            status_message_display.update()
 
    page.add(
        ft.Column(
            [
                # 新增顯示文件路徑/URL的Text
                ft.Row([file_path_display], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(
                    [
                        local_file_button,
                        ft.VerticalDivider(),
                        url_input,
                        process_url_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(),
                ft.Row(
                    [
                        model_dropdown,
                        ft.Container(width=20), # 間隔
                        prompt_input,
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Row(
                    [
                        ft.ElevatedButton("處理文件", icon=ft.Icons.PLAY_ARROW, on_click=on_process_file_click), # 直接調用異步函數
                        progress_bar,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                # 新增顯示處理狀態的Text
                ft.Row([status_message_display], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(),
                ft.Text("轉換結果:", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=result_display,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=5,
                    padding=10,
                    expand=True # 讓結果顯示區域擴展
                ),
                ft.Row(
                    [
                        download_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER # 下載按鈕置中
                )
            ],
            expand=True, # 讓主列擴展以填充頁面
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()
 
if __name__ == "__main__":
    ft.app(target=main)