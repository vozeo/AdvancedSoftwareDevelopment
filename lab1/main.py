# main.py
# 修订：这里的逻辑命令有些问题，原有init、read <filepath>, save <filepath>, close <filepath>, editor-list, edit <filepath>, exit/quit.
# 其中init逻辑应该移到编辑器内部，完全按照文件要求，应该是指读入文件后再进行的初始化操作
# read应按要求更改为load；
# close逻辑有问题，不需要输入关闭文件名，而是关闭当前文件
# 完成了session退出保存，进入时载入功能
# 修改后的命令有load <filepath>, save <filepath>, close, editor-list, edit <filepath>, exit/quit
import json

# from exceptiongroup import catch

# bug报告：print函数有问题；edit函数切换editor速度太慢
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