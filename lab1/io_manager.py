# io_manager.py
from bs4 import BeautifulSoup, NavigableString
from model import HTMLDocument, HTMLElement
from model import TreeNode
from typing import Dict, List, Optional, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from display import DisplayStrategy
import os

class HTMLParser:
    """
    负责读取和解析 HTML 文件，将其转化为 HTMLDocument 对象。
    """
    
    # 直接获取当前节点下的文本，而非get_text的所有文本
    def get_direct_text(self, tag) -> str:
        return "".join(child.strip() for child in tag.contents if isinstance(child, NavigableString))

    def parse(self, filepath: str) -> HTMLDocument:
        if not os.path.exists(filepath):
            print(f"File '{filepath}' does not exist.")
            return None
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        document = HTMLDocument()

        # 解析 <head>
        head = soup.find('head')
        if head:
            for child in head.children:
                if child.name:
                    tag = child.name
                    id_attr = child.get('id', tag)
                    text = self.get_direct_text(child)
                    element = HTMLElement(tag, id_attr, text)
                    # 对title进行特殊处理 原来存在的init模板中的删了重新加
                    if tag == 'title': 
                        title_element = document.head.find_by_id("title")
                        document.head.remove_child(title_element)
                    document.head.add_child(element)

        # 解析 <body>
        body = soup.find('body')
        if body:
            for child in body.children:
                if isinstance(child, str):
                    # 文本节点
                    text = child.strip()
                    if text:
                        text_element = HTMLElement("text", "text", text)   # TODO Text ID 的唯一性
                        document.body.add_child(text_element)
                elif child.name:
                    element = self.parse_element(child)
                    document.body.add_child(element)

        return document

    def parse_element(self, bs_element) -> HTMLElement:
        tag = bs_element.name
        id_attr = bs_element.get('id', tag)
        text = self.get_direct_text(bs_element)
        element = HTMLElement(tag, id_attr, text)
        for child in bs_element.children:
            if child.name:
                child_element = self.parse_element(child)
                element.add_child(child_element)
        return element

class HTMLWriter:
    """
    负责将 HTMLDocument 对象序列化为 HTML 字符串并写入文件。
    """
    def write(self, document: HTMLDocument, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as file:
            from display import IndentDisplayStrategy
            disp = IndentDisplayStrategy(indent_size=2)
            document.set_display_strategy(disp)
            html_str = document.display(show_id=True)
            file.write(html_str)
        print(f"File written to: {filepath}")



class FNode(TreeNode):
    def __init__(self, file_name) -> None:
        super(FNode, self).__init__()
        self.file_name = file_name
        # self.children: List['FNode'] = []
        # self.parent: Optional['FNode'] = None
        self.is_active: bool = False

    def add_child(self, child: 'FNode') -> None:
        self.children.append(child)
        child.parent=self

    def set_active(self) -> None:
        self.is_active = True
    
    def get_display_name(self) -> str:
        return self.file_name if not self.is_active else self.file_name + "*"

class Directory:
    def __init__(self, file_list: List[str], active_file: str) -> None:
        tree = {}
        for file in file_list:
            parts = file.split("/")
            current = tree
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
        self.root = FNode('.')
        for subtree in tree.items():
            child_node = self.build_tree(subtree)
            self.root.add_child(child_node)
        # set active file
        if active_file:
            parts = active_file.split('/')
            current = self.root
            for part in parts:
                for subtree in current.children:
                    if subtree.file_name == part:
                        current=subtree
                        break
            current.set_active()

    def build_tree(self, file_tree: Tuple[str, dict]) -> FNode:
        file_name, subtree = file_tree
        file = FNode(file_name)
        for child in subtree.items():
            child_node = self.build_tree(child)
            file.add_child(child_node)
        return file
    
    def set_display_strategy(self, strategy: "DisplayStrategy") -> None:
        """
        设定输出策略
        """
        self.display_strategy = strategy

    def display(self) -> str:
        """
        输出（字符串形式）
        """
        if self.display_strategy is None:
            raise ValueError("Display strategy is not set.")
        return self.display_strategy.display(self)