# session_manager.py
from typing import Dict
from editor import Editor
from model import HTMLDocument
from io_manager import HTMLParser, HTMLWriter

class SessionManager:
    """
    管理多个 Editor 会话，处理文件的加载、保存、切换等。
    """
    def __init__(self):
        self.editors: Dict[str, Editor] = {}  # key: filename, value: Editor
        self.active_filename: str = ""

    def load(self, filename: str, parser: HTMLParser):
        """
        加载文件，如果文件不存在则初始化一个新文档。新加载的文件成为活动文件。
        """
        if filename in self.editors:
            print(f"File '{filename}' is already loaded.")
            self.active_filename = filename
            return
        document = parser.parse(filename)
        if not document:
            # 文件不存在或解析失败，初始化新文档
            document = HTMLDocument()
            print(f"Initialized new HTML document for '{filename}'.")
        editor = Editor(document)
        self.editors[filename] = editor
        self.active_filename = filename
        print(f"Loaded file: {filename}")
        return filename

    def save(self, filename: str, writer: HTMLWriter):
        """
        保存指定文件。
        """
        if filename not in self.editors:
            print(f"File '{filename}' is not loaded.")
            return False
        editor = self.editors[filename]
        writer.write(editor.document, filename)
        editor.is_modified = False
        return True

    def close(self, writer: HTMLWriter):
        """
        关闭指定文件，如果修改过则保存。
        """
        target_name = self.active_filename
        if target_name =="":
            print("Editor is empty.")
            return
        editor = self.editors[target_name]
        if editor.is_modified:
            choice = input(f"File '{target_name}' has unsaved changes. Save before closing? (y/n): ").lower()
            if choice == 'y':
                self.save(target_name, writer)
        del self.editors[target_name]
        print(f"Closed file: {target_name}")
        self.active_filename = next(iter(self.editors), "")

    def list_editors(self):
        """
        显示当前会话中打开的编辑文件的列表。
        """
        if not self.editors:
            print("No open editors.")
            return
        for filename, editor in self.editors.items():
            indicator = ">" if filename == self.active_filename else " "
            modified = "*" if editor.is_modified else ""
            print(f"{indicator} {filename}{modified}")

    def switch_editor(self, filename: str):
        """
        切换到指定文件的编辑器。
        """
        if filename in self.editors:
            self.active_filename = filename
            print(f"Switched to editor: {filename}")
        else:
            print(f"Editor for file '{filename}' not found.")

    def get_active_editor(self) -> Editor:
        """
        获取当前活动编辑器。
        """
        if self.active_filename:
            return self.editors[self.active_filename]
        else:
            return None
        
    def get_opened_files(self):
        """
        获取当前打开的文件列表。
        """
        return list(self.editors.keys())

    def get_showids(self):
        """
            获取当前打开的文件列表对应的所有showid。
        """
        editors = list(self.editors.values())
        return [editor.show_id for editor in editors]

    def get_active_file(self):
        """
            获取当前活动文件名
        """
        return self.active_filename

    def set_showid_false(self, file_name):
        """
            设置file_name文件的showid为false
        """
        editor = self.editors[file_name]
        editor.show_id = False

    def set_active_file(self, file_name):
        self.active_filename = file_name