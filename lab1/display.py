# display.py
from model import HTMLDocument, HTMLElement

class DisplayStrategy:
    """
    显示策略接口，定义显示方法。
    """
    def display(self, document: HTMLDocument, show_id: bool):
        pass

class TreeDisplayStrategy(DisplayStrategy):
    """
    树形格式显示策略。
    """
    def display(self, document: HTMLDocument, show_id: bool):
        self.print_element(document.root, "", True, show_id)

    def print_element(self, element: HTMLElement, prefix: str, is_last: bool, show_id: bool):
        connector = "└── " if is_last else "├── "
        print(prefix + connector, end='')

        id_part = f"#{element.id}" if show_id else ""
        print(f"{element.tag_name}{id_part}")

        new_prefix = prefix + ("    " if is_last else "│   ")
        child_count = len(element.children)
        for i, child in enumerate(element.children):
            is_last_child = (i == child_count - 1)
            self.print_element(child, new_prefix, is_last_child, show_id)

class IndentDisplayStrategy(DisplayStrategy):
    """
    缩进格式显示策略。
    """
    def __init__(self, indent_size: int = 2):
        self.indent_size = indent_size

    def display(self, document: HTMLDocument, show_id: bool):
        self.serialize_element(document.root, 0, show_id)

    def serialize_element(self, element: HTMLElement, level: int, show_id: bool) -> str:
        indent = ' ' * (self.indent_size * level)
        tag = element.tag_name
        attrs = ""
        # 仅添加 id 属性，且排除特定标签的 id
        if tag not in ["html", "head", "title", "body"]:
            if show_id:
                attrs = f' id="{element.id}"'
        opening_tag = f"{indent}<{tag}{attrs}>"

        if not element.children and not element.text_content:
            return f"{opening_tag}</{tag}>\n"

        result = f"{opening_tag}"
        if element.text_content:
            result += f"{element.text_content}"
        if element.children:
            result += "\n"
            for child in element.children:
                result += self.serialize_element(child, level + 1, show_id)
            result += f"{indent}</{tag}>\n"
        else:
            result += f"</{tag}>\n"
        return result