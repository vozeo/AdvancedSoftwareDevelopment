# spell_checker.py
import language_tool_python
from model import HTMLDocument, HTMLElement
from typing import List

class SpellChecker:
    """
    集成 LanguageTool 实现拼写检查。
    """
    def __init__(self):
        self.tool = language_tool_python.LanguageTool('en-US')  # 使用美式英语

    def check_spelling(self, document: HTMLDocument) -> List[str]:
        errors = []
        self.traverse_and_check(document.root, errors)
        return errors

    def traverse_and_check(self, element: HTMLElement, errors: List[str]):
        if element.text_content and element.tag_name != "text":
            matches = self.tool.check(element.text_content)
            for match in matches:
                error = f"[{element.tag_name}#{element.id}] {match.message} at position {match.offset}-{match.offset + match.errorLength}: {match.context}"
                errors.append(error)
        for child in element.children:
            self.traverse_and_check(child, errors)