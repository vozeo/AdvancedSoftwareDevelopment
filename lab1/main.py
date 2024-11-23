# main.py
# 修订：这里的逻辑命令有些问题，原有init、read <filepath>, save <filepath>, close <filepath>, editor-list, edit <filepath>, exit/quit.
# 其中init逻辑应该移到编辑器内部，完全按照文件要求，应该是指读入文件后再进行的初始化操作
# read应按要求更改为load；
# close逻辑有问题，不需要输入关闭文件名，而是关闭当前文件
# 完成了session退出保存，进入时载入功能
# 修改后的命令有load <filepath>, save <filepath>, close, editor-list, edit <filepath>, exit/quit
import json

from exceptiongroup import catch

# bug报告：print函数有问题；edit函数切换editor速度太慢
from session_manager import SessionManager
from io_manager import HTMLParser, HTMLWriter
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
    print("""
Command-line Help:
1. load filename.html  
   - Load an HTML file into the editor.  
   - If the file does not exist, a new file will be created.  
   - The newly loaded file becomes the active file.  

2. save filename.html  
   - Save the current active file with the specified name.  
   - If the file already exists, it will be overwritten.  

3. close  
   - Close the current active editor.  
   - If there are unsaved changes, you will be prompted to save the file.  
   - After closing, the first file in the open editor list becomes the active editor.  
   - If no files are open, there will be no active editor.  

4. editor-list  
   - Display a list of all files currently open in the session.  
   - The list shows:  
     - `*` for modified files.  
     - `>` to indicate the active file.  

5. edit filename.html  
   - Switch the active editor to the specified file.  
   - The file must already be open in the session.  

Type any command above to perform the specified action.
    """)

    while True:
        user_input = input("Session> ").strip()
        if not user_input:
            continue
        parts = user_input.split()
        command = parts[0].lower()

        if command in ["exit", "quit"]:
            # 保存当前编辑的文件
            file_list = session_manager.get_opened_files()
            active_file = session_manager.get_active_file()
            showid_list = session_manager.get_showids()
            save_data = {
                "file_list": file_list,
                "active_file": active_file,
                "showid_list": showid_list
            }
            with open('session_data.json', 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=4)
            print("Session data saved to session_data.json.")
            for file in file_list:
                # 这个函数不需要传入文件，只要关闭次数够就能关闭所有编辑器
                session_manager.close(writer)
            print("Exiting session manager.")
            break
        # elif command == "init":
        #     if len(parts) < 2:
        #         filename = "new_document.html"
        #     else:
        #         filename = parts[1]
        #     session_manager.load(filename, parser)
        #     editor = session_manager.get_active_editor()
        #     if editor:
        #         cli = CLI(editor)
        #         cli.start()
        elif command == "load":
            if len(parts) < 2:
                print("Invalid load command. Usage: load <filepath>")
                continue
            filename = parts[1]
            session_manager.load(filename, parser)
            editor = session_manager.get_active_editor()
            if editor:
                cli = CLI(editor, session_manager)
                cli.start()
        elif command == "save":
            if len(parts) < 2:
                print("Invalid save command. Usage: save <filepath>")
                continue
            filename = parts[1]
            session_manager.save(filename, writer)
        elif command == "close":
            if len(parts) >= 2:
                print("Invalid close command. Usage: close")
                continue
            session_manager.close(writer)
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
                cli = CLI(editor, session_manager)
                cli.start()
        else:
            print(
                "Unknown command. Available commands: init, load <filepath>, save <filepath>, close, editor-list, edit <filepath>, exit.")


if __name__ == "__main__":
    main()