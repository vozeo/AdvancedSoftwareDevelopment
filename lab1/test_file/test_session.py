import os
import sys

sys.path.append('../../lab1')

from lab1.session_manager import SessionManager
from lab1.io_manager import HTMLParser, HTMLWriter
from lab1.editor import Editor
from io import StringIO
from unittest.mock import patch

# 初始化
session_manager = SessionManager()
parser = HTMLParser()
writer = HTMLWriter()

import unittest
class TestSession(unittest.TestCase):
    def test_01_load(self):
        # 测试load功能
        filename = session_manager.load('test1.html',parser)
        self.assertIsNotNone(session_manager.editors[filename],'file should be loaded')
        filename = session_manager.load('test2.html',parser)
        self.assertIsNotNone(session_manager.editors[filename], 'file should be loaded')

    def test_02_save(self):
        # 测试save功能
        judge = session_manager.save('test1.html',writer)
        self.assertEqual(judge,True)
        judge = session_manager.save('test2.html', writer)
        self.assertEqual(judge, True)
        judge = session_manager.save('test3.html', writer)
        self.assertEqual(judge, False,'test3 is not exist')
        pass

    def test_03_list_editors(self):
        # 测试列出各session功能
        with patch('sys.stdout', new=StringIO()) as fake_out:
            session_manager.list_editors()
            self.assertEqual(fake_out.getvalue().strip(), 'test1.html\n> test2.html')
        pass

    def test_04_get_active_editor(self):
        # 测试返回活动文件功能
        self.assertIsInstance(session_manager.get_active_editor(),type(session_manager.editors['test1.html']))
        pass

    def test_05_switch_editor(self):
        # 测试更换活动文件功能
        judge = session_manager.switch_editor('test3.html')
        self.assertEqual(judge, False)
        judge = session_manager.switch_editor('test2.html')
        self.assertEqual(judge, True)
        self.assertIsInstance(session_manager.get_active_editor(), type(session_manager.editors['test2.html']))
        pass

    def test_06_close(self):
        # 测试关闭session功能
        judge = session_manager.close(writer)
        self.assertEqual(judge, True)
        judge = session_manager.close(writer)
        self.assertEqual(judge, True)
        judge = session_manager.close(writer)
        self.assertEqual(judge, False)
        # 删除测试文件
        os.remove('test1.html')
        os.remove('test2.html')
        pass



if __name__ == '__main__':
    unittest.main()