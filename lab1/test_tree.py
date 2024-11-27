import unittest
from io import StringIO
from unittest.mock import patch
from display import TreeDisplay, IndentDisplay
from model import HTMLDocument, HTMLElement

class TestDisplayStrategies(unittest.TestCase):

    def setUp(self):
        # 创建一个简单的 HTML 文档
        self.document = HTMLDocument()
        body = self.document.body
        h1 = HTMLElement("h1", "header", "Hello World")
        p = HTMLElement("p", "paragraph", "This is a test paragraph.")
        span = HTMLElement("span", "highlight", "highlighted text")
        p.add_child(span)
        body.add_child(h1)
        body.add_child(p)

    def test_tree_display_strategy(self):
        strategy = TreeDisplay()
        expected_output = (
            "html\n"
             "├── head\n"
             "│   └── title\n"
             "└── body\n"
             "    ├── h1#header\n"
             "    │   └── Hello World\n"
             "    └── p#paragraph\n"
             "        ├── This is a test paragraph.\n"
             "        └── span#highlight\n"
             "            └── highlighted text")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            print(strategy.display(self.document))
            self.assertEqual(fake_out.getvalue().strip(), expected_output.strip())

    def test_indent_display_strategy_no_id(self):
        strategy = IndentDisplay()
        expected_output = (
            "<html>\n"
            "  <head>\n"
            "    <title></title>\n"
            "  </head>\n"
            "  <body>\n"
            "    <h1>Hello World</h1>\n"
            "    <p>This is a test paragraph.\n"
            "      <span>highlighted text</span>\n"
            "    </p>\n"
            "  </body>\n"
            "</html>\n"
        )
        with patch('sys.stdout', new=StringIO()) as fake_out:
            print(strategy.display(self.document, show_id=False))
            self.assertEqual(fake_out.getvalue().strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()
