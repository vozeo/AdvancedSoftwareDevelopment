import json

from session_manager import SessionManager
from io_manager import HTMLParser, HTMLWriter
from spell_checker import HTMLSpellChecker
from cli import CLI


def main():
    parser = HTMLParser()
    writer = HTMLWriter()
    session_manager = SessionManager()

    print("Welcome to the HTML Editor Session Manager.")
    try:
        with open('session_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            file_list = data.get("file_list", [])
            active_file = data.get("active_file", "")
            showid_list = data.get("showid_list", [])
        if len(file_list):
            print("Saved session detected. Importing...")
        for i in range(len(file_list)):
            session_manager.load(file_list[i], parser)
            if not showid_list[i]:
                session_manager.set_showid_false(file_list[i])
        session_manager.set_active_file(active_file)
        print("Finished.")
    except FileNotFoundError:
        pass
    editor = session_manager.get_active_editor()
    checker = HTMLSpellChecker()
    cli = CLI(editor, session_manager, checker, parser, writer)
    print(cli.help_text)

    while True:
        user_input = input("Session> ").strip()
        if user_input:
            cli(user_input)

if __name__ == "__main__":
    main()