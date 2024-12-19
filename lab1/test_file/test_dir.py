import unittest
from io import StringIO
from unittest.mock import patch
from display import TreeDisplayStrategy, IndentDisplayStrategy
from io_manager import Directory


class TestDisplayStrategies(unittest.TestCase):

    def setUp(self):
        # 基本的文件列表
        self.file_list = [
            "html/test.html",
            "html/test1.html",
            "html/aaa/test1.html",
        ]
        self.active_file = "html/aaa/test1.html"
        self.directory = Directory(file_list=self.file_list, active_file=self.active_file)
        self.tree_display = TreeDisplayStrategy()
        self.indent_display = IndentDisplayStrategy()

    def test_tree_display_strategy(self):
        """测试树形展示策略"""
        expected_output = (
            ".\n"
            "└── html\n"
            "    ├── test.html\n"
            "    ├── test1.html\n"
            "    └── aaa\n"
            "        └── test1.html*"
        )
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.directory.set_display_strategy(self.tree_display)
            print(self.directory.display())
            self.assertEqual(fake_out.getvalue().strip(), expected_output.strip())

    def test_indent_display_strategy(self):
        """测试缩进展示策略"""
        expected_output = (
            ".\n"
            "  html\n"
            "    test.html\n"
            "    test1.html\n"
            "    aaa\n"
            "      test1.html*\n"
        )
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.directory.set_display_strategy(self.indent_display)
            print(self.directory.display())
            self.assertEqual(fake_out.getvalue().strip(), expected_output.strip())

    def test_empty_directory(self):
        """测试空目录的展示"""
        self.directory = Directory(file_list=[], active_file=None)
        expected_output = ".\n"  # 空目录仅显示 root
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.directory.set_display_strategy(self.tree_display)
            print(self.directory.display())
            self.assertEqual(fake_out.getvalue().strip(), expected_output.strip())

    def test_nested_directories(self):
        """测试深层嵌套的文件目录"""
        self.file_list = [
            "a/b/c/d/e/file.txt",
            "a/b/x/y/z/file2.txt",
        ]
        self.directory = Directory(file_list=self.file_list, active_file="a/b/c/d/e/file.txt")
        expected_output_tree = (
            ".\n"
            "└── a\n"
            "    └── b\n"
            "        ├── c\n"
            "        │   └── d\n"
            "        │       └── e\n"
            "        │           └── file.txt*\n"
            "        └── x\n"
            "            └── y\n"
            "                └── z\n"
            "                    └── file2.txt"
        )
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.directory.set_display_strategy(self.tree_display)
            print(self.directory.display())
            self.assertEqual(fake_out.getvalue().strip(), expected_output_tree.strip())


    def test_file_name_collision(self):
        """测试相同文件名在不同目录中的情况"""
        self.file_list = [
            "folder1/file.txt",
            "folder2/file.txt",
        ]
        self.directory = Directory(file_list=self.file_list, active_file="folder2/file.txt")
        expected_output_tree = (
            ".\n"
            "├── folder1\n"
            "│   └── file.txt\n"
            "└── folder2\n"
            "    └── file.txt*"
        )
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.directory.set_display_strategy(self.tree_display)
            print(self.directory.display())
            self.assertEqual(fake_out.getvalue().strip(), expected_output_tree.strip())


if __name__ == '__main__':
    unittest.main()
