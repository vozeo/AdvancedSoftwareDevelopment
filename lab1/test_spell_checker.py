# test_spell_checker.py
import unittest
from model import HTMLDocument, HTMLElement
from spell_checker import HTMLSpellChecker

class TestHTMLSpellChecker(unittest.TestCase):
    def setUp(self):
        """在每个测试之前设置一个 HTML 文档和拼写检查器。"""
        self.document = HTMLDocument()
        self.spell_checker = HTMLSpellChecker()

    def test_check_spelling_no_errors(self):
        """测试没有拼写错误的情况。"""
        # 添加没有拼写错误的元素
        self.document.body.add_child(HTMLElement("p", "para1", "This is a correct sentence."))
        self.document.body.add_child(HTMLElement("p", "para2", "All words are spelled correctly."))

        errors = self.spell_checker.check_spelling(self.document)
        self.assertEqual(errors, [], "Should be no spelling errors.")

    def test_check_spelling_with_errors(self):
        """测试有拼写错误的情况。"""
        # 添加有拼写错误的元素
        self.document.body.add_child(HTMLElement("p", "para1", "This is a incorrect sentense."))
        self.document.body.add_child(HTMLElement("p", "para2", "Some words are mispeled."))

        errors = self.spell_checker.check_spelling(self.document)
        self.assertGreater(len(errors), 0, "Should be spelling errors.")
        print(errors)
        self.assertIn(("para1", "sentense"), errors, "Should find 'sentense' in para1.")
        self.assertIn(("para2", "mispeled"), errors, "Should find 'mispeled' in para2.")
        for item in errors:
            suggestions = self.spell_checker.get_suggestion(item[1])
            print(f"suggestions for '{item[1]}': {', '.join(suggestions)}")


    def test_check_spelling_empty_document(self):
        """测试空文档的情况。"""
        errors = self.spell_checker.check_spelling(self.document)
        self.assertEqual(errors, [], "Should be no spelling errors in an empty document.")

    def test_check_spelling_mixed_content(self):
        """测试包含英语单词、汉字和数字的混合内容。"""
        # 添加包含英语单词、汉字和数字的元素
        self.document.body.add_child(HTMLElement("p", "para1", "This is a test with 123 and 中文."))
        self.document.body.add_child(HTMLElement("p", "para2", "Some words are incorect, like mispeled and 错误."))
        self.document.body.add_child(HTMLElement("p", "para3", "1234567890 is a number, and so is 0987654321."))

        errors = self.spell_checker.check_spelling(self.document)
        self.assertGreater(len(errors), 0, "Should be spelling errors.")
        print(errors)
        self.assertIn(("para2", "incorect"), errors, "Should find 'incorect' in para2.")
        self.assertIn(("para2", "mispeled"), errors, "Should find 'mispeled' in para2.")
        for item in errors:
            suggestions = self.spell_checker.get_suggestion(item[1])
            print(f"suggestions for '{item[1]}': {', '.join(suggestions)}")


if __name__ == "__main__":
    unittest.main()