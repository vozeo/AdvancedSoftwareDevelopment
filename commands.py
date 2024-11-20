# commands.py
from abc import ABC, abstractmethod
from typing import Optional

from model import HTMLDocument, HTMLElement

class Command(ABC):
    """
    命令接口，定义执行和撤销的方法。
    """
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class InsertCommand(Command):
    """
    插入元素命令。
    """
    def __init__(self, document: HTMLDocument, new_element: HTMLElement, insert_before_id: str):
        self.document = document
        self.new_element = new_element
        self.insert_before_id = insert_before_id
        self.parent: Optional[HTMLElement] = None
        self.index: Optional[int] = None

    def execute(self):
        target = self.document.find_by_id(self.insert_before_id)
        if target and target.parent:
            self.parent = target.parent
            self.index = self.parent.children.index(target)
            self.parent.children.insert(self.index, self.new_element)
            self.new_element.parent = self.parent
            print(f"Inserted <{self.new_element.tag_name}> with id '{self.new_element.id}' before '{self.insert_before_id}'.")
        else:
            print(f"Insert location '{self.insert_before_id}' not found.")

    def undo(self):
        if self.parent and self.new_element in self.parent.children:
            self.parent.remove_child(self.new_element)
            print(f"Undo Insert: Removed <{self.new_element.tag_name}> with id '{self.new_element.id}'.")

class AppendCommand(Command):
    """
    在某元素内添加子元素命令。
    """
    def __init__(self, document: HTMLDocument, new_element: HTMLElement, parent_id: str):
        self.document = document
        self.new_element = new_element
        self.parent_id = parent_id
        self.parent: Optional[HTMLElement] = None

    def execute(self):
        parent = self.document.find_by_id(self.parent_id)
        if parent:
            parent.add_child(self.new_element)
            self.parent = parent
            print(f"Appended <{self.new_element.tag_name}> with id '{self.new_element.id}' to '{self.parent_id}'.")
        else:
            print(f"Parent element '{self.parent_id}' not found.")

    def undo(self):
        if self.parent and self.new_element in self.parent.children:
            self.parent.remove_child(self.new_element)
            print(f"Undo Append: Removed <{self.new_element.tag_name}> with id '{self.new_element.id}' from '{self.parent_id}'.")

class EditIdCommand(Command):
    """
    编辑元素 id 的命令。
    """
    def __init__(self, document: HTMLDocument, element_id: str, new_id: str):
        self.document = document
        self.element_id = element_id
        self.new_id = new_id
        self.element: Optional[HTMLElement] = None
        self.old_id: Optional[str] = None

    def execute(self):
        self.element = self.document.find_by_id(self.element_id)
        if self.element:
            self.old_id = self.element.id
            self.element.id = self.new_id
            print(f"Changed id of <{self.element.tag_name}> from '{self.old_id}' to '{self.new_id}'.")
        else:
            print(f"Element with id '{self.element_id}' not found.")

    def undo(self):
        if self.element and self.old_id:
            self.element.id = self.old_id
            print(f"Undo Edit ID: Changed id of <{self.element.tag_name}> back to '{self.old_id}'.")

class EditTextCommand(Command):
    """
    编辑元素文本内容的命令。
    """
    def __init__(self, document: HTMLDocument, element_id: str, new_text: str):
        self.document = document
        self.element_id = element_id
        self.new_text = new_text
        self.element: Optional[HTMLElement] = None
        self.old_text: Optional[str] = None

    def execute(self):
        self.element = self.document.find_by_id(self.element_id)
        if self.element:
            self.old_text = self.element.text_content
            self.element.text_content = self.new_text
            print(f"Changed text of <{self.element.tag_name}> with id '{self.element.id}'.")
        else:
            print(f"Element with id '{self.element_id}' not found.")

    def undo(self):
        if self.element and self.old_text is not None:
            self.element.text_content = self.old_text
            print(f"Undo Edit Text: Restored text of <{self.element.tag_name}> with id '{self.element.id}'.")

class DeleteCommand(Command):
    """
    删除元素的命令。
    """
    def __init__(self, document: HTMLDocument, element_id: str):
        self.document = document
        self.element_id = element_id
        self.element: Optional[HTMLElement] = None
        self.parent: Optional[HTMLElement] = None
        self.index: Optional[int] = None

    def execute(self):
        self.element = self.document.find_by_id(self.element_id)
        if self.element and self.element.parent:
            self.parent = self.element.parent
            self.index = self.parent.children.index(self.element)
            self.parent.remove_child(self.element)
            print(f"Deleted <{self.element.tag_name}> with id '{self.element.id}'.")
        else:
            print(f"Element with id '{self.element_id}' not found or has no parent.")

    def undo(self):
        if self.parent and self.element and self.index is not None:
            self.parent.children.insert(self.index, self.element)
            self.element.parent = self.parent
            print(f"Undo Delete: Restored <{self.element.tag_name}> with id '{self.element.id}' to '{self.parent.id}'.")