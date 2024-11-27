# model.py
from typing import List, Optional
from spellchecker import SpellChecker
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from display import DisplayStrategy


class TreeNode:
    """
    通用树节点接口，所有节点类型都需要实现。
    """
    def get_name(self) -> str:
        """返回节点名称"""
        raise NotImplementedError()

    def get_children(self) -> list["TreeNode"]:
        """返回子节点列表"""
        raise NotImplementedError()

    def is_leaf(self) -> bool:
        """判断是否是叶子节点"""
        raise NotImplementedError()

class HTMLElement(TreeNode):
    """
    表示 HTML 元素的类，包含标签名、id、文本内容和子元素。
    """
    def __init__(self, tag_name: str, id_value: Optional[str] = None, text_content: str = ""):
        self.tag_name = tag_name
        self.id = id_value if id_value else tag_name  # 默认 id 为标签名
        self.text_content = text_content
        self.children: List['HTMLElement'] = []
        self.parent: Optional['HTMLElement'] = None
        self.has_spelling_error = False

    def add_child(self, child: 'HTMLElement'):
        """
        向当前元素添加子元素。
        """
        self.children.append(child)
        child.parent = self
        self.check_spelling(child)

    def check_spelling(self, element: 'HTMLElement'):
        """
        检查元素及其子元素的拼写错误。
        """
        checker = SpellChecker()
        if element.text_content:
            words = [word.strip('.,!?()[]{}":;') for word in element.text_content.split()]
            words = [word for word in words if word]  # 移除空字符串
            words = [word for word in words if not word.isdigit() and not any(
                c.isalpha() and c > '\u4e00' and c < '\u9fff' for c in word)]  # 排除数字和中文
            misspelled_words = checker.unknown(words)
            for word in words:
                if word in misspelled_words:
                    element.has_spelling_error = True
                    break  # 一旦发现拼写错误，退出循环
        for child in element.children:
            self.check_spelling(child)

    def remove_child(self, child: 'HTMLElement'):
        """
        从当前元素移除子元素。
        """
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    def find_by_id(self, search_id: str) -> Optional['HTMLElement']:
        """
        查找具有指定 id 的元素。
        """
        if self.id == search_id:
            return self
        for child in self.children:
            result = child.find_by_id(search_id)
            if result:
                return result
        return None
    
    # for display
    def get_name(self, show_id: bool, format: str) -> str:
        if format == "tree":
            # 检查是否有拼写错误
            spell_check_mark = "[X] " if self.has_spelling_error else ""

            if self.tag_name not in ["html", "head", "title", "body"] and show_id:
                id_part = f"#{self.id}"
            else:
                id_part = ""
            # Print the tag name with id (if any)

            return f"{spell_check_mark}{self.tag_name}{id_part}"
        elif format == "indent":
            if self.tag_name not in ["html", "head", "title", "body"] and show_id:
                attrs = f' id="{self.id}"'
            else:
                attrs = ""
            return f"<{self.tag_name}{attrs}>"
        else:
            raise ValueError(f"Display Format: {format} is not valid.")

    
    def is_leaf(self) -> bool:
        return len(self.element.children) == 0 and not self.element.text_content

class HTMLDocument:
    """
    表示整个 HTML 文档，包含根元素 <html>。
    """
    def __init__(self):
        self.root = HTMLElement("html", "html")
        self.head = HTMLElement("head", "head")
        self.title = HTMLElement("title", "title")
        self.body = HTMLElement("body", "body")
        self.root.add_child(self.head)
        self.head.add_child(self.title)
        self.root.add_child(self.body)

        self.display_strategy = None # 输出策略

    def find_by_id(self, search_id: str) -> Optional[HTMLElement]:
        """
        在文档中查找具有指定 id 的元素。
        """
        return self.root.find_by_id(search_id)

    def delete_element(self, element: HTMLElement) -> bool:
        """
        删除指定元素。
        """
        if element.parent:
            element.parent.remove_child(element)
            return True
        return False
    
    def set_display_strategy(self, strategy: "DisplayStrategy") -> None:
        """
        设定输出策略
        """
        self.display_strategy = strategy

    def display(self, show_id: bool = True) -> str:
        """
        输出（字符串形式）
        """
        if self.display_strategy is None:
            raise ValueError("Display strategy is not set.")
        return self.display_strategy.display(self, show_id)