import subprocess
import time
from select import select
import traceback


# 定义命令行程序的路径
CLI_PROGRAM_PATH = 'main.py'

# 测试文件名
HTML_FILE_1 = 'test_file_1.html'
HTML_FILE_2 = 'test_file_2.html'


def run_commands_with_timeout(commands, timeout=5):
    print("Starting CLI program...")

    process = subprocess.Popen(
        ['python3.11', CLI_PROGRAM_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1  # 行缓冲
    )

    try:
        for command in commands:
            print(f"Input: {command}")
            process.stdin.write(command + '\n')
            process.stdin.flush()

            start_time = time.time()
            while time.time() - start_time < timeout:
                ready_to_read, _, _ = select([process.stdout], [], [], 0.1)
                if ready_to_read:
                    output = process.stdout.readline().strip()
                    if output:
                        print(f"Output: {output}")
                elif process.poll() is not None:  # 子进程已退出
                    break

    except BrokenPipeError as e:
        print(f"BrokenPipeError: {e}. The subprocess might have exited prematurely.")
        print("Attempting to capture subprocess error output...")
        
        # 捕获子进程的标准错误（调用栈等）
        process.terminate()
        stderr = process.stderr.read()
        if stderr:
            print("Subprocess error output (stderr):")
            print(stderr.strip())
        else:
            print("No error output detected from the subprocess.")
        
        print("Main process traceback:")
        traceback.print_exc()  # 打印主进程的调用栈

    finally:
        process.stdin.close()
        process.wait()

        # 确认子进程已完全终止
        if process.poll() is not None:
            print(f"Subprocess exited with code {process.poll()}.")


def test_comprehensive_workflow():
    print("Running comprehensive workflow test...")

    commands = [
        # 初始化测试环境
        f"load {HTML_FILE_1}",
        "init",  # 初始化HTML文档

        # 插入多个元素
        "append div div1 body 'Hello World!'",
        "insert p p1 div1 'This is a paragraph.'",
        "insert span span1 p1 'Span inside paragraph.'",
        "print-tree",  # 打印树形结构，验证插入

        # 编辑元素
        "edit-id div1 new_div1",
        "edit-text p1 'Updated paragraph content'",
        "print-indent",  # 打印缩进结构，验证编辑

        # 删除元素并撤销
        "delete span1",
        "print-tree",  # 验证删除后树形结构
        "undo",  # 撤销删除
        "print-tree",  # 验证撤销后的树形结构
        "redo",  # 重做删除
        "print-tree",  # 验证重做后的树形结构

        # 保存文件并加载另一个文件
        f"save {HTML_FILE_1}",
        f"load {HTML_FILE_2}",
        "init",
        "insert h1 h1_1 0 'Title in file 2'",
        "print-tree",

        # 编辑多个文件
        f"edit {HTML_FILE_1}",
        "print-tree",  # 验证切换回文件1
        f"save {HTML_FILE_1}",

        # 关闭文件并退出
        "close",
        "exit"
    ]

    stdout, stderr = run_commands_with_timeout(commands)

    print("STDOUT:")
    print(stdout)
    print("STDERR:")
    print(stderr)

    # 验证输出内容包含关键点
    assert "Loading" in stdout
    assert "Saving" in stdout
    assert "Undo" in stdout
    assert "Redo" in stdout
    assert "Session data saved" in stdout
    print("Comprehensive workflow test passed!")


def test_heavy_insertions_and_deletions():
    print("Running heavy insertions and deletions test...")

    commands = [
        # 初始化并插入多个元素
        f"load {HTML_FILE_1}",
        "init",
    ] + [
        f"insert div div_{i} 0 'Content for div {i}'" for i in range(20)
    ] + [
        "print-tree",  # 打印树形结构，验证插入

        # 删除一些元素
        "delete div_0",
        "delete div_1",
        "print-tree",  # 验证删除后的树形结构

        # 撤销和重做
        "undo",
        "undo",
        "redo",
        "print-tree",

        # 保存文件并退出
        f"save {HTML_FILE_1}",
        "exit"
    ]

    stdout, stderr = run_commands_with_timeout(commands)

    print("STDOUT:")
    print(stdout)
    print("STDERR:")
    print(stderr)

    # 验证输出内容包含关键点
    assert "Loading" in stdout
    assert "Undo" in stdout
    assert "Redo" in stdout
    assert "Saving" in stdout
    assert "Session data saved" in stdout
    print("Heavy insertions and deletions test passed!")


def test_spelling_and_id_handling():
    print("Running spelling and ID handling test...")

    commands = [
        # 初始化并插入元素
        f"load {HTML_FILE_1}",
        "init",
        "insert div div1 0 'Hello Wrld!'",
        "insert p p1 div1 'This is a paragrap.'",
        "spell-check",  # 拼写检查，应该有错误
        "edit-text p1 'This is a paragraph.'",  # 修正拼写
        "spell-check",  # 再次检查，无错误

        # 测试showid功能
        "showid true",
        "print-tree",
        "showid false",
        "print-tree",

        # 保存文件并退出
        f"save {HTML_FILE_1}",
        "exit"
    ]

    stdout, stderr = run_commands_with_timeout(commands)

    print("STDOUT:")
    print(stdout)
    print("STDERR:")
    print(stderr)

    # 验证拼写检查和showid输出
    assert "Spelling Errors:" in stdout
    assert "No spelling errors found" in stdout
    assert "showId set to True" in stdout
    assert "showId set to False" in stdout
    assert "Saving" in stdout
    print("Spelling and ID handling test passed!")


def run_all_tests():
    """ 运行所有测试用例 """
    test_comprehensive_workflow()
    test_heavy_insertions_and_deletions()
    test_spelling_and_id_handling()


if __name__ == "__main__":
    run_all_tests()
