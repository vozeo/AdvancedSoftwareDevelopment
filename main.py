# main.py
from session_manager import SessionManager
from io_manager import HTMLParser, HTMLWriter
from cli import CLI


def main():
    parser = HTMLParser()
    writer = HTMLWriter()
    session_manager = SessionManager()

    print("Welcome to the HTML Editor Session Manager.")
    print(
        "Type 'init <filename>' to initialize a new HTML document, 'read <filepath>' to read a file, or 'exit' to quit.")

    while True:
        user_input = input("Session> ").strip()
        if not user_input:
            continue
        parts = user_input.split()
        command = parts[0].lower()

        if command in ["exit", "quit"]:
            # TODO: 实现会话状态的保存和恢复
            print("Exiting session manager.")
            break
        elif command == "init":
            if len(parts) < 2:
                filename = "new_document.html"
            else:
                filename = parts[1]
            session_manager.load(filename, parser)
            editor = session_manager.get_active_editor()
            if editor:
                cli = CLI(editor)
                cli.start()
        elif command == "read":
            if len(parts) < 2:
                print("Invalid read command. Usage: read <filepath>")
                continue
            filename = parts[1]
            session_manager.load(filename, parser)
            editor = session_manager.get_active_editor()
            if editor:
                cli = CLI(editor)
                cli.start()
        elif command == "save":
            if len(parts) < 2:
                print("Invalid save command. Usage: save <filepath>")
                continue
            filename = parts[1]
            session_manager.save(filename, writer)
        elif command == "close":
            if len(parts) < 2:
                print("Invalid close command. Usage: close <filepath>")
                continue
            filename = parts[1]
            session_manager.close(filename, writer)
        elif command == "editor-list":
            session_manager.list_editors()
        elif command == "edit":
            if len(parts) < 2:
                print("Invalid edit command. Usage: edit <filepath>")
                continue
            filename = parts[1]
            session_manager.switch_editor(filename)
            editor = session_manager.get_active_editor()
            if editor:
                cli = CLI(editor)
                cli.start()
        else:
            print(
                "Unknown command. Available commands: init, read <filepath>, save <filepath>, close <filepath>, editor-list, edit <filepath>, exit.")


if __name__ == "__main__":
    main()