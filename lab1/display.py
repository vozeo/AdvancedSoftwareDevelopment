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
    


class TreeDisplay:
    """
    树形展示逻辑，适用于任意实现 TreeNode 接口的对象。
    """
    def display(self, tree) -> str:
        res = self._generate_node(tree.root, "", is_last=True)
        return res

    def _generate_node(self, node, prefix: str, is_last: bool) -> str:
        result = []
        connector = "└── " if is_last else "├── "
        text_connector = "    " if is_last else "│   "
        result.append(prefix + connector + node.get_name(format="tree", show_id=True) if node.parent else node.get_name(format="tree", show_id=True))
        child_count = len(node.children)
        if node.text_content:
            text_prefix = prefix + text_connector
            if child_count == 0:
                result.append(text_prefix + "└── " + node.text_content)
            else:
                result.append(text_prefix + "├── " + node.text_content)
        else:
            text_prefix = ""  # For subsequent children to use correct indentation

        # Recursively print child elements
        if not node.parent:
            tempprefix = ""
        else:
            tempprefix = "    "
        new_prefix = prefix + text_connector if node.text_content else prefix + (tempprefix if is_last else "│   ")

        for i, child in enumerate(node.children):
            is_last_child = (i == child_count - 1)
            result.append(self._generate_node(child, new_prefix, is_last_child))
        
        return "\n".join(result)
    

class IndentDisplay:
    """
    缩进展示逻辑，适用于任意实现 TreeNode 接口的对象。
    """
    def __init__(self, indent_size: int = 2):
        self.indent_size = indent_size

    def display(self, tree, show_id: bool):
        #print("start to show indent form")
        res =  self.serialize_element(tree.root, 0, show_id)
        return res
        #print("finish to show indent form")

    def serialize_element(self, node, level: int, show_id: bool) -> str:
        indent = ' ' * (self.indent_size * level)
        opening_tag = f"{indent}{node.get_name(show_id=show_id, format="indent")}"

        if not node.children:
            if isinstance(node, HTMLElement):
                if not node.text_content:
                    return f"{opening_tag}</{node.tag_name}>\n"
            else:
                return f"{opening_tag}\n"

        result = f"{opening_tag}"
        if isinstance(node, HTMLElement) and node.text_content:
            result += f"{node.text_content}"
        if node.children:
            result += "\n"
            for child in node.children:
                result += self.serialize_element(child, level + 1, show_id)
            if isinstance(node, HTMLElement):
                result += f"{indent}</{node.tag_name}>\n"
        else:
            if isinstance(node, HTMLElement):
                result += f"</{node.tag_name}>\n"

        return result