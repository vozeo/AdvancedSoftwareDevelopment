# cli.py
# 这里导入了HTMLElement包，并新增了init命令
from model import HTMLElement
from editor import Editor
from display import TreeDisplayStrategy, IndentDisplayStrategy
from spell_checker import HTMLSpellChecker
from session_manager import SessionManager
from commands import *
from io_manager import HTMLParser, HTMLWriter, Directory
from typing import Callable, List
import json
import sys
import shlex


class CLI:
    """
    提供命令行交互界面，接收用户输入并显示输出。
    """

    def __init__(
        self,
        editor: Editor,
        session_manager: SessionManager,
        spell_checker: HTMLSpellChecker,
        parser: HTMLParser,
        writer: HTMLWriter,
    ):
        self.editor = editor
        self.session_manager = session_manager
        self.spell_checker = spell_checker
        self.parser = parser
        self.writer = writer
        self.tree_display = TreeDisplayStrategy()

        # Use 2 as the default indent_size.
        self.indent_display = IndentDisplayStrategy(indent_size=2)

        self.help_text = help_text

    def command_func(self, command: str) -> Callable[..., None]:
        command_mapping = {
            "exit": self.handle_exit,
            "quit": self.handle_exit,
            "help": self.handle_help,
            "load": self.handle_load,
            "save": self.handle_save,
            "close": self.handle_close,
            "editor-list": self.handle_editor_list,
            "edit": self.handle_edit,
            "insert": self.handle_insert,
            "append": self.handle_append,
            "edit-id": self.handle_edit_id,
            "edit-text": self.handle_edit_text,
            "delete": self.handle_delete,
            "print-tree": self.handle_print_tree,
            "print-indent": self.handle_print_indent,
            "spell-check": self.handle_spell_check,
            "init": self.handle_init,
            "undo": self.handle_undo,
            "redo": self.handle_redo,
            "showid": self.handle_showid,
            "dir-tree": self.handle_dir_tree,
            "dir-indent": self.handle_dir_indent
        }

        return command_mapping.get(command, self.handle_unknown_command)

    def __call__(self, user_input: str) -> None:
        parsed_input = shlex.split(user_input)
        command, *args = parsed_input
        command_func = self.command_func(command)

        # Pass only arguments to command functions.
        co_argcount = command_func.__code__.co_argcount
        command_func(args) if co_argcount > 1 else command_func()

    def handle_exit(self):

        opened_files = self.session_manager.get_opened_files()
        active_files = self.session_manager.get_active_file()
        showids = self.session_manager.get_showids()
        save_data = {
            "file_list": opened_files,
            "active_file": active_files,
            "showid_list": showids
        }
        with open("session_data.json", "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=4)
        print("Session data saved to session_data.json.")
        for file in opened_files:
            self.session_manager.close(self.writer)
        print("Existing session manager.")
        sys.exit(0)

    def handle_help(self):
        print(self.help_text)

    def handle_load(self, args: List[str]):
        if len(args) != 1:
            print("Invalid load command. Usage: load <filepath>")
            return
        filename =args[0]

        self.session_manager.load(filename, self.parser)
        self.editor = self.session_manager.get_active_editor()

    def handle_save(self, args: List[str]):
        if len(args) != 1:
            print("Invalid save command. Usage: save <filepath>")
            return
        filename = args[0]

        self.session_manager.save(filename, self.writer)

    def handle_close(self):

        self.session_manager.close(self.writer)

    def handle_editor_list(self):
        self.session_manager.list_editors()

    def handle_edit(self, args: List[str]):
        if len(args) != 1:
            print("Invalid edit command. Usage: edit <filepath>")

        filename = args[0]
        self.session_manager.switch_editor(filename)
        self.editor = self.session_manager.get_active_editor()

    def handle_insert(self, args: List[str]):
        if len(args) < 3:
            print(
                "Invalid insert command. Usage: insert <tagName> <idValue> <insertLocation> [textContent]"
            )
            return
        tag_name, id_value, insert_location, *text_content = args
        text_content = " ".join(text_content) if text_content else ""
        new_element = HTMLElement(tag_name, id_value, text_content)
        command = InsertCommand(self.editor.document, new_element, insert_location)
        self.editor.execute_command(command)

    def handle_append(self, args: List[str]):
        if len(args) < 3:
            print(
                "Invalid append command. Usage: append <tagName> <idValue> <parentElement> [textContent]"
            )
            return
        tag_name, id_value, parent_element, *text_content = args
        text_content = " ".join(text_content) if text_content else ""
        new_element = HTMLElement(tag_name, id_value, text_content)
        command = AppendCommand(self.editor.document, new_element, parent_element)
        self.editor.execute_command(command)

    def handle_edit_id(self, args: List[str]):
        if len(args) != 2:
            print("Invalid edit-id command. Usage: edit-id <oldId> <newId>")
            return
        old_id, new_id = args
        command = EditIdCommand(self.editor.document, old_id, new_id)
        self.editor.execute_command(command)

    def handle_edit_text(self, args: List[str]):
        if len(args) < 1:
            print(
                "Invalid edit-text command. Usage: edit-text <elementId> [newTextContent]"
            )
            return
        element_id, new_text = args
        new_text = " ".join(new_text) if new_text else ""
        command = EditTextCommand(self.editor.document, element_id, new_text)
        self.editor.execute_command(command)

    def handle_delete(self, args: List[str]):
        if len(args) != 1:
            print("Invalid delete command. Usage: delete <elementId>")
            return
        element_id = args[0]
        command = DeleteCommand(self.editor.document, element_id)
        self.editor.execute_command(command)

    def handle_print_tree(self):
        # set tree
        self.editor.document.set_display_strategy(self.tree_display)
        print(self.editor.document.display(self.editor.show_id))

    def handle_print_indent(self, args: List[str]):
        if args:
            try:
                self.indent_display.indent_size = int(args[0])
            except ValueError:
                print("Invalid indent value. Using default (2).")

        # set indent
        self.editor.document.set_display_strategy(self.indent_display)
        print(self.editor.document.display(self.editor.show_id))

    def handle_spell_check(self):
        errors = self.spell_checker.check_spelling(self.editor.document)
        if not errors:
            print("No spelling errors found.")
        else:
            print("Spelling Errors:")
            for error in errors:
                print(error)

    def handle_init(self):
        command = InitCommand(self.editor.document)
        self.editor.execute_command(command)

    def handle_undo(self):
        self.editor.undo()

    def handle_redo(self):
        self.editor.redo()

    def handle_showid(self, args: List[str]):
        if len(args) != 2:
            print("Invalid showid command. Usage: showid <true|false>")
            return
        value = args[0].lower()
        if value == "true":
            self.editor.show_id = True
            print("showId set to True.")
        elif value == "false":
            self.editor.show_id = False
            print("showId set to False.")
        else:
            print("Invalid value for showid. Use 'true' or 'false'.")

    def handle_dir_tree(self):
        file_list = self.session_manager.get_opened_files()
        active_file = self.session_manager.get_active_file()
        directory = Directory(file_list=file_list, active_file=active_file)
        directory.set_display_strategy(self.tree_display)
        print(directory.display())

    def handle_dir_indent(self, args: List[str]):
        if args:
            try:
                self.indent_display.indent_size = int(args[1])
            except ValueError:
                print("Invalid indent value. Using default (2).")

        file_list = self.session_manager.get_opened_files()
        active_file = self.session_manager.get_active_file()
        directory = Directory(file_list=file_list, active_file=active_file)
        directory.set_display_strategy(self.indent_display)
        print(directory.display())

    def handle_unknown_command(self, args: List[str]):
        print("Unknown command. Type 'help' for a list of commands.")


help_text = """
Type `help` to view this list anytime.
Command-line Help:

Available Commands:
1. load <filename>
   - Load an HTML file into the editor. If the file does not exist, a new file will be created.
   - <filename>: Path to the HTML file to load.

2. save <filename>
   - Save the current active file to the specified filename.
   - <filename>: Path where the active file will be saved.

3. close
   - Close the currently active editor. If there are unsaved changes, you will be prompted to save them.
   - After closing, the next open file (if any) becomes the active file.

4. editor-list
   - Display all open files in the session.
   - `*` indicates modified files, and `>` marks the active file.

5. edit <filename>
   - Switch the active editor to the specified file.
   - <filename>: The name of an already open file.

6. insert <tag> <id> <pos> [text]
   - Insert a new HTML element into the document at the specified position.
   - <tag>: The HTML tag (e.g., div, span).
   - <id>: A unique ID for the new element.
   - <pos>: Where to insert (e.g., after an existing element ID).
   - [text]: Optional content for the new element.

7. append <tag> <id> <parent> [text]
   - Append a new HTML element as a child of a parent element.
   - <tag>: The HTML tag (e.g., div, p).
   - <id>: A unique ID for the new element.
   - <parent>: ID of the parent element.
   - [text]: Optional content for the new element.

8. edit-id <oldId> <newId>
   - Change the ID of an existing HTML element.
   - <oldId>: The current ID of the element.
   - <newId>: The new ID to assign.

9. edit-text <id> [text]
   - Edit the text content of an HTML element.
   - <id>: The ID of the element to edit.
   - [text]: The new text content. If omitted, the text will be cleared.

10. delete <id>
    - Delete an HTML element by its ID.
    - <id>: The ID of the element to delete.

11. print-tree
    - Print the document in a hierarchical tree structure.

12. print-indent [size]
    - Print the document with indentation for better readability.
    - [size]: Optional indentation size (default is 2).

13. spell-check
    - Check for spelling errors in the current document and display a list of errors, if any.

14. init
    - Initialize a new, empty HTML document in the editor.

15. undo
    - Undo the last action performed in the editor.

16. redo
    - Redo the last undone action in the editor.

17. showid <true|false>
    - Toggle whether element IDs are displayed in output.
    - <true|false>: Set to `true` to show IDs or `false` to hide them.

18. dir-tree
    - Display a tree structure of all open files in the session, highlighting the active file.

19. dir-indent [size]
    - Display open files with indentation for better visualization.
    - [size]: Optional indentation size (default is 2).

20. exit / quit
    - Save the current session state and exit the program.
    - Session data will be saved to `session_data.json`.

Type `help` to view this list at any time.
"""
