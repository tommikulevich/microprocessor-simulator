import sys
from PySide2.QtWidgets import QApplication

from main_window import MainWindow
from microprocessor import Microprocessor


if __name__ == "__main__":
    app = QApplication(sys.argv)
    processor = Microprocessor()
    mainWindow = MainWindow(processor)
    mainWindow.show()
    sys.exit(app.exec_())
