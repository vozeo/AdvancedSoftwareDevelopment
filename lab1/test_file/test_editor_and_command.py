import unittest
import sys
sys.path.append("..")
from model import HTMLDocument, HTMLElement
from editor import Editor
from commands import (
    InitCommand,
    InsertCommand,
    AppendCommand,
    EditIdCommand,
    EditTextCommand,
    DeleteCommand,
)


class TestEditorWithCommands(unittest.TestCase):

    def setUp(self):
        # 创建一个 HTMLDocument 和 Editor 实例
        self.document = HTMLDocument()
        self.editor = Editor(self.document)

    def test_init_command(self):
        command = InitCommand(self.document)
        self.editor.execute_command(command)

        self.assertEqual(self.document.root.tag_name, "html")
        self.assertEqual(len(self.document.root.children), 2)  # head and body

    def test_insert_command(self):
        # 初始化文档
        self.editor.execute_command(InitCommand(self.document))

        # 插入一个元素到 body 的开头c
        new_element = HTMLElement(tag_name="div", id_value="div0")
        command = AppendCommand(self.document, new_element, "body")
        self.editor.execute_command(command)
        new_element = HTMLElement(tag_name="div", id_value="div1")
        command = InsertCommand(self.document, new_element, "div0")
        self.editor.execute_command(command)

        body = self.document.find_by_id("body")
        self.assertEqual(body.children[0].id, "div1")

        # 撤销插入
        self.editor.undo()
        self.editor.undo()
        self.assertNotIn(new_element, body.children)

    def test_append_command(self):
        # 初始化文档
        self.editor.execute_command(InitCommand(self.document))

        # 在 body 内追加一个元素
        new_element = HTMLElement(tag_name="p", id_value="p1")
        command = AppendCommand(self.document, new_element, "body")
        self.editor.execute_command(command)

        body = self.document.find_by_id("body")
        self.assertIn(new_element, body.children)

        # 撤销追加
        self.editor.undo()
        self.assertNotIn(new_element, body.children)

    def test_edit_id_command(self):
        # 初始化文档并添加一个元素
        self.editor.execute_command(InitCommand(self.document))
        body = self.document.find_by_id("body")
        element = HTMLElement(tag_name="div", id_value="div1")
        body.add_child(element)

        # 修改元素的 ID
        command = EditIdCommand(self.document, "div1", "new_div1")
        self.editor.execute_command(command)
        self.assertEqual(element.id, "new_div1")

        # 撤销 ID 修改
        self.editor.undo()
        self.assertEqual(element.id, "div1")

    def test_edit_text_command(self):
        # 初始化文档并添加一个元素
        self.editor.execute_command(InitCommand(self.document))
        body = self.document.find_by_id("body")
        element = HTMLElement(tag_name="p", id_value="p1", text_content="Old text")
        body.add_child(element)

        # 修改元素的文本内容
        command = EditTextCommand(self.document, "p1", "New text")
        self.editor.execute_command(command)
        self.assertEqual(element.text_content, "New text")

        # 撤销文本修改
        self.editor.undo()
        self.assertEqual(element.text_content, "Old text")

    def test_delete_command(self):
        # 初始化文档并添加一个元素
        self.editor.execute_command(InitCommand(self.document))
        body = self.document.find_by_id("body")
        element = HTMLElement(tag_name="div", id_value="div1")
        body.add_child(element)

        # 删除元素
        command = DeleteCommand(self.document, "div1")
        self.editor.execute_command(command)
        self.assertNotIn(element, body.children)

        # 撤销删除
        self.editor.undo()
        self.assertIn(element, body.children)

    def test_redo_functionality(self):
        # 测试 undo 和 redo 的完整功能
        self.editor.execute_command(InitCommand(self.document))
        element = HTMLElement(tag_name="div", id_value="div1")
        self.editor.execute_command(AppendCommand(self.document, element, "body"))

        # Undo
        self.editor.undo()
        body = self.document.find_by_id("body")
        self.assertNotIn(element, body.children)

        # Redo
        self.editor.redo()
        self.assertIn(element, body.children)


if __name__ == "__main__":
    unittest.main()
