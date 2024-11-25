# io_manager.py
from bs4 import BeautifulSoup, NavigableString
from model import HTMLDocument, HTMLElement
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
            html_str = self.serialize_element(document.root, 0)
            file.write(html_str)
        print(f"File written to: {filepath}")

    def serialize_element(self, element: HTMLElement, indent: int) -> str:
        indent_str = '  ' * indent
        tag = element.tag_name
        attrs = ""
        # 仅添加 id 属性，且排除特定标签的 id
        if tag not in ["html", "head", "title", "body"]:
            attrs = f' id="{element.id}"'
        opening_tag = f"{indent_str}<{tag}{attrs}>"
        closing_tag = f"</{tag}>"

        if not element.children and not element.text_content:
            return f"{opening_tag}{closing_tag}\n"

        result = f"{opening_tag}"
        if element.text_content:
            result += f"{element.text_content}"
        if element.children:
            result += "\n"
            for child in element.children:
                result += self.serialize_element(child, indent + 1)
            result += f"{indent_str}"
        result += f"{closing_tag}\n"
        return result