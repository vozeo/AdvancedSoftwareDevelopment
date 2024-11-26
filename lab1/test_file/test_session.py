import sys

sys.path.append('../../lab1')

from lab1.session_manager import SessionManager
from lab1.io_manager import HTMLParser, HTMLWriter
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
        pass

    def test_04_get_active_editor(self):
        # 测试返回活动文件功能
        pass

    def test_05_switch_editor(self):
        # 测试更换活动文件功能
        pass

    def test_06_close(self):
        # 测试关闭session功能
        pass



if __name__ == '__main__':
    unittest.main()