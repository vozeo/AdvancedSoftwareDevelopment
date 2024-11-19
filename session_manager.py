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

    def save(self, filename: str, writer: HTMLWriter):
        """
        保存指定文件。
        """
        if filename not in self.editors:
            print(f"File '{filename}' is not loaded.")
            return
        editor = self.editors[filename]
        writer.write(editor.document, filename)
        editor.is_modified = False

    def close(self, filename: str, writer: HTMLWriter):
        """
        关闭指定文件，如果修改过则保存。
        """
        if filename not in self.editors:
            print(f"File '{filename}' is not loaded.")
            return
        editor = self.editors[filename]
        if editor.is_modified:
            choice = input(f"File '{filename}' has unsaved changes. Save before closing? (y/n): ").lower()
            if choice == 'y':
                self.save(filename, writer)
        del self.editors[filename]
        print(f"Closed file: {filename}")
        if self.active_filename == filename:
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