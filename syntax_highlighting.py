from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont

from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document, style="one-dark"):
        super().__init__(document)
        self.lexer = PythonLexer()
        self.set_style(style)

    def set_style(self, style):
        self.style = get_style_by_name(style)
        self.formats = {}
        for token, pygments_style in self.style:
            fmt = QTextCharFormat()
            if pygments_style.get("color"):
                fmt.setForeground(QColor(f"#{pygments_style['color']}"))
            if pygments_style.get("bold"):
                fmt.setFontWeight(QFont.Weight.Bold)
            self.formats[token] = fmt

    def highlightBlock(self, text):
        offset = 0
        for token, content in lex(text, self.lexer):
            length = len(content)
            if content == "":
                continue
            fmt = self.formats.get(token)
            if fmt:
                self.setFormat(offset, length, fmt)
            offset += length
