import unittest
from io import StringIO
from unittest.mock import patch
from display import TreeDisplay, IndentDisplay
from io_manager import Directory

class TestDisplayStrategies(unittest.TestCase):

    def setUp(self):
        # 创建一个简单的 HTML 文档
        self.file_list = [
            "html/test.html",
            "html/test1.html", 
            "html/aaa/test1.html", 
        ]
        self.active_file = "html/aaa/test1.html"
        self.directory = Directory(file_list=self.file_list, active_file=self.active_file)
        self.tree_display = TreeDisplay()
        self.indent_display = IndentDisplay()

    def test_tree_display_strategy(self):
        expected_output = (
            "root\n"
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

    def test_indent_display_strategy_no_id(self):
        expected_output = (
            "root\n"
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

if __name__ == '__main__':
    unittest.main()
