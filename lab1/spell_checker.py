# spell_checker.py
import string
from typing import List, Tuple
from model import HTMLDocument, HTMLElement
from spellchecker import SpellChecker  # 确保安装了pyspellchecker库

class HTMLSpellChecker:
    """
    用于检查 HTML 文档中元素文本的拼写错误。
    """
    def __init__(self):
        self.spell_checker = SpellChecker()

    def check_spelling(self, document: HTMLDocument) -> List[Tuple[str, str]]:
        """
        检查给定 HTML 文档中的拼写错误。

        :param document: HTMLDocument 实例
        :return: 拼写错误的列表，每个错误为 (元素 id, 错误单词)
        """
        errors = []
        if document and document.root:
            self._check_element_spelling(document.root, errors)
            print("the len of errors: ", len(errors))
        else:
            raise ValueError("文档或根元素不存在")
        return errors

    def _check_element_spelling(self, element: HTMLElement, errors: List[Tuple[str, str]]):
        """
        #递归检查元素及其子元素的拼写
        #:param element: 当前检查的 HTMLElement
        #:param errors: 存储拼写错误的列表
        """
        if element.text_content:
            words = [word.strip('.,!?()[]{}":;') for word in element.text_content.split()]
            words = [word for word in words if word]  # 移除空字符串
            words = [word for word in words if not word.isdigit() and not any(
                c.isalpha() and c > '\u4e00' and c < '\u9fff' for c in word)]  # 排除数字和中文
            misspelled_words = self.spell_checker.unknown(words)
            for word in words:
                if word in misspelled_words:
                    errors.append((element.id, word))
        for child in element.children:
            self._check_element_spelling(child, errors)

    def get_suggestion(self, word:str) -> List[str]:
        return list(self.spell_checker.candidates(word))