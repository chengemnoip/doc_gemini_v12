import requests
import os
import tempfile # 引入 tempfile 模組
import mimetypes # 用於更準確地推斷 MIME 類型
import json # 引入 json 模組

class DocumentParser:
    def __init__(self):
        pass # 不再需要 mimetypes.add_defaults


    def get_file_info(self, file_path: str):
        """返回本地文件的路徑、原始檔名和 MIME 類型。"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        original_base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        if file_extension == '.ipynb':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    notebook_content = json.load(f)
                
                extracted_text = []
                for cell in notebook_content.get('cells', []):
                    if cell.get('cell_type') == 'code' and 'source' in cell:
                        extracted_text.extend(cell['source']) # 使用 extend 而不是 append
                    elif cell.get('cell_type') == 'markdown' and 'source' in cell:
                        extracted_text.extend(cell['source']) # 使用 extend 而不是 append
                
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8')
                temp_file.write("".join(extracted_text)) # 使用 "".join() 拼接列表中的字串
                temp_file.close()

                return {
                    "file_path": temp_file.name,
                    "original_base_name": original_base_name,
                    "mime_type": "text/plain" # 強制為 text/plain
                }
            except json.JSONDecodeError:
                raise ValueError(f"無法解析 .ipynb 文件: {file_path}，請確保它是有效的 JSON 格式。")
            except Exception as e:
                raise RuntimeError(f"處理 .ipynb 文件時發生錯誤: {e}")
        else:
            return {
                "file_path": file_path,
                "original_base_name": original_base_name,
                "mime_type": self._get_mime_type_from_path(file_path)
            }

    def get_url_info(self, url: str):
        """
        從 URL 獲取文件並將其保存為臨時文件，然後返回臨時文件的路徑、原始檔名和 MIME 類型。
        調用者有責任在處理完成後刪除此臨時文件。
        """
        response = requests.get(url)
        response.raise_for_status() # 檢查請求是否成功

        content_type = response.headers.get('Content-Type', '').lower()
        
        # 嘗試從 URL 推斷文件名和擴展名
        original_file_base_name = url.split('/')[-1].split('?')[0].split('#')[0]
        
        # 提取擴展名以用於臨時文件
        file_extension = os.path.splitext(original_file_base_name)[1]
        if not file_extension and 'content-type' in response.headers:
            # 如果 URL 沒有擴展名，嘗試從 Content-Type 推斷
            ext = mimetypes.guess_extension(content_type)
            if ext:
                file_extension = ext

        # 創建一個臨時文件
        # delete=False 允許我們在關閉後手動刪除文件
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_extension)
        try:
            temp_file.write(response.content)
            temp_file.close() # 寫入後關閉文件，以便其他進程可以讀取

            # 推斷 MIME 類型，優先使用 Content-Type，否則從臨時文件路徑推斷
            final_mime_type = content_type if content_type else self._get_mime_type_from_path(temp_file.name)
            
            return {
                "file_path": temp_file.name, # 返回臨時文件路徑
                "original_base_name": os.path.splitext(original_file_base_name)[0] if '.' in original_file_base_name else original_file_base_name,
                "mime_type": final_mime_type
            }
        except Exception as e:
            # 確保在出現錯誤時也清理臨時文件
            os.remove(temp_file.name)
            raise RuntimeError(f"處理 URL 時創建臨時文件失敗: {e}")

    def _get_mime_type_from_path(self, file_path: str):
        """根據文件路徑推斷 MIME 類型。"""
        # 使用 mimetypes.guess_type 更為健壯
        if file_path.endswith('.ipynb'):
            mime_type = 'application/vnd.jupyter'
        else:
            mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type if mime_type else "application/octet-stream"
