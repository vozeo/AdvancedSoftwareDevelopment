# editor.py
from typing import List
from commands import Command

class Editor:
    """
    编辑器类，管理 HTMLDocument，提供编辑操作接口，维护 Undo 和 Redo 栈。
    """
    def __init__(self, document):
        self.document = document
        self.undo_stack: List[Command] = []
        self.redo_stack: List[Command] = []
        self.is_modified = False
        self.show_id = True  # 默认显示 id

    def execute_command(self, command: Command):
        """
        执行命令，并将其推入 Undo 栈，清空 Redo 栈。
        """
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()
        self.is_modified = True

    def undo(self):
        """
        撤销上一个命令。
        """
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()
            self.redo_stack.append(command)
            self.is_modified = True
        else:
            print("Nothing to undo.")

    def redo(self):
        """
        重做上一个撤销的命令。
        """
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()
            self.undo_stack.append(command)
            self.is_modified = True
        else:
            print("Nothing to redo.")

    def clear_history(self):
        """
        清除 Undo 和 Redo 栈。
        """
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.is_modified = False