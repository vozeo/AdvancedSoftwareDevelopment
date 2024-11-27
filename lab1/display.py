#display.py
from model import HTMLDocument, HTMLElement, TreeNode
import io
from io_manager import FNode
from contextlib import redirect_stdout
from typing import Protocol

class DisplayStrategy(Protocol):
    """
    显示策略接口，定义显示方法。
    """
    def display(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method.")

class TreeDisplayStrategy(DisplayStrategy):
    """
    树形展示逻辑，适用于任意实现 TreeNode 接口的对象。
    """
    def display(self, tree: TreeNode, show_id: bool=True) -> str:
        res = self._generate_node(tree.root, "", is_last=True,show_id=show_id)
        return res

    def _generate_node(self, node: TreeNode, prefix: str, is_last: bool, show_id: bool) -> str:
        result = []
        connector = "└── " if is_last else "├── "
        text_connector = "    " if is_last else "│   "
        display_name = ''
        if isinstance(node, HTMLElement):
            display_name = node.get_display_name(format="tree", show_id=show_id)
        elif isinstance(node, FNode):
            display_name = node.get_display_name()
        result.append(prefix + connector + display_name if node.parent else display_name)
        child_count = len(node.children)
        if isinstance(node, HTMLElement) and node.text_content:
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
        if isinstance(node, HTMLElement) and node.text_content:
            new_prefix = prefix + text_connector
        else:
            new_prefix = prefix + (tempprefix if is_last else "│   ")

        for i, child in enumerate(node.children):
            is_last_child = (i == child_count - 1)
            result.append(self._generate_node(child, new_prefix, is_last_child, show_id=show_id))
        
        return "\n".join(result)
    

class IndentDisplayStrategy(DisplayStrategy):
    """
    缩进展示逻辑，适用于任意实现 TreeNode 接口的对象。
    """
    def __init__(self, indent_size: int = 2):
        self.indent_size = indent_size

    def display(self, tree, show_id: bool=True):
        #print("start to show indent form")
        res =  self.serialize_element(tree.root, 0, show_id)
        return res
        #print("finish to show indent form")

    def serialize_element(self, node, level: int, show_id: bool) -> str:
        indent = ' ' * (self.indent_size * level)

        display_name = ''
        if isinstance(node, HTMLElement):
            display_name = node.get_display_name(show_id=show_id, format="indent")
        elif isinstance(node, FNode):
            display_name = node.get_display_name()
        opening_tag = f"{indent}{display_name}"

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