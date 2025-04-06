import ui
import sys
import io
import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextEdit
from PyQt6.QtGui import QFont

from syntax_highlighting import SyntaxHighlighter
from pygments.styles import get_all_styles
import styles

files = []


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def file_changed_explorer(self, e):
        try:
            if not e == None:
                interface.tab_bar.setCurrentIndex(files.index(e.text()))
        except Exception as e:
            print(e)

    def file_changed_tab_bar(self, e):
        interface.explorer.setCurrentRow(e)

    def exit_app(self, e):
        sys.exit(0)
    
    def run_code(self, e):
        current_editor = interface.tab_bar.currentWidget()

        if isinstance(current_editor, QTextEdit):
            code = current_editor.toPlainText()
            try:
                reader = io.StringIO()
                sys.stdout = reader
                exec(code)
                interface.output.append(reader.getvalue())
            except Exception as err:
                interface.output.append(f"Evaluation error: {err}")

            sys.stdout = sys.__stdout__
    
    def clear_output(self, e):
        interface.output.clear()

    def open_file(self, e):
        fname = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "${HOME}",
            "All Files (*);;",
        )
        editor = QTextEdit()
        if not fname[0] == '':
            with open(fname[0], 'r+') as file:
                self.syntax_highlighter = SyntaxHighlighter(editor.document())
                self.current_file_contents = file.read()
                editor.setPlainText(self.current_file_contents)
                editor.setFont(QFont("Iosevka", 16))

            interface.tab_bar.addTab(editor, fname[0])
            interface.explorer.addItem(fname[0])
            files.append(fname[0])

    def close_file(self, e):
        index = interface.tab_bar.currentIndex()
        if index == -1:
            return
        interface.tab_bar.removeTab(index)
        interface.explorer.takeItem(index)
        files.pop(index)

    def save_file(self, e):
        index = interface.tab_bar.currentIndex()
        editor = interface.tab_bar.currentWidget()
        if editor == None:
            return
        with open(files[index], "w") as file:
            if isinstance(editor, QTextEdit):
                code = editor.toPlainText()
                file.write(code)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    interface = ui.Ui_MainWindow()
    interface.setupUi(window)

    interface.explorer.currentItemChanged.connect(window.file_changed_explorer)
    interface.tab_bar.currentChanged.connect(window.file_changed_tab_bar)
    interface.run_code_button.clicked.connect(window.run_code)
    interface.clear_output_button.clicked.connect(window.clear_output)
    interface.actionExit.triggered.connect(window.exit_app)
    interface.actionOpen.triggered.connect(window.open_file)
    interface.actionClose.triggered.connect(window.close_file)
    interface.actionSave.triggered.connect(window.save_file)

    styles.set_styles(interface)
    window.show()
    app.exec()
