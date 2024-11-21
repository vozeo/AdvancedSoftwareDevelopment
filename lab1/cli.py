# cli.py
# 这里导入了HTMLElement包，并新增了init命令
from model import HTMLElement
from editor import Editor
from display import TreeDisplayStrategy, IndentDisplayStrategy
from spell_checker import SpellChecker
from commands import (
    InsertCommand,
    AppendCommand,
    EditIdCommand,
    EditTextCommand,
    DeleteCommand
)

class CLI:
    """
    提供命令行交互界面，接收用户输入并显示输出。
    """
    def __init__(self, editor: Editor):
        self.editor = editor
        self.spell_checker = SpellChecker()
        self.display_strategy = TreeDisplayStrategy()  # 默认树形显示

    def start(self):
        print("Entering editor session. Type 'help' for a list of commands.")
        while True:
            try:
                user_input = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting editor.")
                break

            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0].lower()

            if command in ["exit", "quit"]:
                print("Exiting editor.")
                break
            elif command == "help":
                self.print_help()
            elif command == "insert":
                self.handle_insert(parts)
            elif command == "append":
                self.handle_append(parts)
            elif command == "edit-id":
                self.handle_edit_id(parts)
            elif command == "edit-text":
                self.handle_edit_text(parts)
            elif command == "delete":
                self.handle_delete(parts)
            elif command == "print-tree":
                self.handle_print_tree()
            elif command == "print-indent":
                self.handle_print_indent(parts)
            elif command == "spell-check":
                self.handle_spell_check()
            elif command == "init":
                self.handle_init()
            elif command == "undo":
                self.editor.undo()
            elif command == "redo":
                self.editor.redo()
            elif command == "showid":
                self.handle_showid(parts)
            else:
                print("Unknown command. Type 'help' for a list of commands.")

    def print_help(self):
        help_text = """
Available commands:
insert <tagName> <idValue> <insertLocation> [textContent]
append <tagName> <idValue> <parentElement> [textContent]
edit-id <oldId> <newId>
edit-text <elementId> [newTextContent]
delete <elementId>
print-tree
print-indent [indentSize]
spell-check
init
undo
redo
showid <true|false>
help
exit
"""
        print(help_text)

    def handle_insert(self, parts):
        if len(parts) < 4:
            print("Invalid insert command. Usage: insert <tagName> <idValue> <insertLocation> [textContent]")
            return
        tag_name = parts[1]
        id_value = parts[2]
        insert_location = parts[3]
        text_content = ' '.join(parts[4:]) if len(parts) > 4 else ""
        new_element = HTMLElement(tag_name, id_value, text_content)
        command = InsertCommand(self.editor.document, new_element, insert_location)
        self.editor.execute_command(command)

    def handle_append(self, parts):
        if len(parts) < 4:
            print("Invalid append command. Usage: append <tagName> <idValue> <parentElement> [textContent]")
            return
        tag_name = parts[1]
        id_value = parts[2]
        parent_element = parts[3]
        text_content = ' '.join(parts[4:]) if len(parts) > 4 else ""
        new_element = HTMLElement(tag_name, id_value, text_content)
        command = AppendCommand(self.editor.document, new_element, parent_element)
        self.editor.execute_command(command)

    def handle_edit_id(self, parts):
        if len(parts) < 3:
            print("Invalid edit-id command. Usage: edit-id <oldId> <newId>")
            return
        old_id = parts[1]
        new_id = parts[2]
        command = EditIdCommand(self.editor.document, old_id, new_id)
        self.editor.execute_command(command)

    def handle_edit_text(self, parts):
        if len(parts) < 2:
            print("Invalid edit-text command. Usage: edit-text <elementId> [newTextContent]")
            return
        element_id = parts[1]
        new_text = ' '.join(parts[2:]) if len(parts) > 2 else ""
        command = EditTextCommand(self.editor.document, element_id, new_text)
        self.editor.execute_command(command)

    def handle_delete(self, parts):
        if len(parts) < 2:
            print("Invalid delete command. Usage: delete <elementId>")
            return
        element_id = parts[1]
        command = DeleteCommand(self.editor.document, element_id)
        self.editor.execute_command(command)

    def handle_print_tree(self):
        self.display_strategy.display(self.editor.document, self.editor.show_id)

    def handle_print_indent(self, parts):
        indent_size = 2  # 默认缩进
        if len(parts) > 1:
            try:
                indent_size = int(parts[1])
            except ValueError:
                print("Invalid indent value. Using default (2).")
        self.display_strategy = IndentDisplayStrategy(indent_size)
        self.display_strategy.display(self.editor.document, self.editor.show_id)

    def handle_spell_check(self):
        errors = self.spell_checker.check_spelling(self.editor.document)
        if not errors:
            print("No spelling errors found.")
        else:
            print("Spelling Errors:")
            for error in errors:
                print(error)

    def handle_init(self):
        # TODO 需要在commands.py写工具类来完成这个功能
        command = InitCommand(self.editor.document)
        self.editor.execute_command(command)

    def handle_showid(self, parts):
        if len(parts) < 2:
            print("Invalid showid command. Usage: showid <true|false>")
            return
        value = parts[1].lower()
        if value == "true":
            self.editor.show_id = True
            print("showId set to True.")
        elif value == "false":
            self.editor.show_id = False
            print("showId set to False.")
        else:
            print("Invalid value for showid. Use 'true' or 'false'.")