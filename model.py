# model.py
from typing import List, Optional

class HTMLElement:
    """
    表示 HTML 元素的类，包含标签名、id、文本内容和子元素。
    """
    def __init__(self, tag_name: str, id_value: Optional[str] = None, text_content: str = ""):
        self.tag_name = tag_name
        self.id = id_value if id_value else tag_name  # 默认 id 为标签名
        self.text_content = text_content
        self.children: List['HTMLElement'] = []
        self.parent: Optional['HTMLElement'] = None

    def add_child(self, child: 'HTMLElement'):
        """
        向当前元素添加子元素。
        """
        self.children.append(child)
        child.parent = self

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