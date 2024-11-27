import unittest

import sys
sys.path.append('../../lab1')

from unittest.mock import patch, mock_open
import json
from io import StringIO

class TestHTMLSessionManager(unittest.TestCase):
    def setUp(self):
        self.mock_data = {
            "file_list": ["file1.html", "file2.html", "file3.html"],
            "active_file": "file1.html",
            "showid_list": [True, False, False]
        }
        self.mock_json = json.dumps(self.mock_data)

    @patch("builtins.open", new_callable=mock_open, read_data="")
    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.stdin", new_callable=StringIO)
    @patch("json.load")
    def test_restore_session(self, mock_json_load, mock_stdin, mock_stdout, mock_file):
        # 设置加载时返回的数据
        mock_json_load.return_value = self.mock_data
        mock_stdin.write("editor-list\nexit\n")
        mock_stdin.seek(0)

        # 导入被测试模块的main函数
        from lab1.main import main

        try:
            # 执行main函数
            main()
        except SystemExit:
            pass  # 捕获退出调用

        print(mock_stdout.getvalue().strip())
        self.assertIn("Loaded file: file1.html", mock_stdout.getvalue().strip())
        self.assertIn("Loaded file: file2.html", mock_stdout.getvalue().strip())
        self.assertIn("Loaded file: file3.html", mock_stdout.getvalue().strip())
        self.assertIn("Finished.", mock_stdout.getvalue().strip())

        # 验证文件的打开行为是否正确
        mock_file.assert_called_with("session_data.json", "w", encoding="utf-8")

if __name__ == "__main__":
    unittest.main()
