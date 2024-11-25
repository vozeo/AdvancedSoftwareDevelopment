#display.py
from model import HTMLDocument, HTMLElement
import io
from contextlib import redirect_stdout
from typing import Protocol

class DisplayStrategy(Protocol):
    """
    显示策略接口，定义显示方法。
    """
    def display(self, document: "HTMLDocument", show_id: bool):
        raise NotImplementedError("Subclasses must implement this method.")

class TreeDisplayStrategy(DisplayStrategy):
    """
    树形格式显示策略。
    """
    def display(self, document: "HTMLDocument", show_id: bool):
        return self.generate_element_string(document.root, "", True, show_id)

    def generate_element_string(self, element: "HTMLElement", prefix: str, is_last: bool, show_id: bool):
        result = []
        connector = "└── " if is_last else "├── "
        text_connector = "    " if is_last else "│   "

        # 检查是否有拼写错误
        spell_check_mark = "[X] " if element.has_spelling_error else ""

        if element.tag_name not in ["html", "head", "title", "body"] and show_id:
            id_part = f"#{element.id}"
        else:
            id_part = ""
        # Print the tag name with id (if any)
        if not element.parent:
            result.append(f"{spell_check_mark}{element.tag_name}{id_part}")
        else:
            result.append(prefix + connector + f"{spell_check_mark}{element.tag_name}{id_part}")

        child_count = len(element.children)
        # Handle text content
        if element.text_content:
            text_prefix = prefix + text_connector
            if child_count == 0:
                result.append(text_prefix + "└── " + element.text_content)
            else:
                result.append(text_prefix + "├── " + element.text_content)
        else:
            text_prefix = ""  # For subsequent children to use correct indentation

        # Recursively print child elements
        if not element.parent:
            tempprefix = ""
        else:
            tempprefix = "    "
        new_prefix = prefix + text_connector if element.text_content else prefix + (tempprefix if is_last else "│   ")

        for i, child in enumerate(element.children):
            is_last_child = (i == child_count - 1)
            result.append(self.generate_element_string(child, new_prefix, is_last_child, show_id))
        
        return "\n".join(result)

class IndentDisplayStrategy(DisplayStrategy):
    """
    缩进格式显示策略。
    """
    def __init__(self, indent_size: int = 2):
        self.indent_size = indent_size

    def display(self, document: "HTMLDocument", show_id: bool):
        #print("start to show indent form")
        return self.serialize_element(document.root, 0, show_id)
        #print("finish to show indent form")

    def serialize_element(self, element: "HTMLElement", level: int, show_id: bool) -> str:
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