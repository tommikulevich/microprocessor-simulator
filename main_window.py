from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog, QWidget, \
    QApplication, QStyle, QGridLayout
from PySide2.QtGui import QTextCursor, QTextCharFormat, QColor, QIcon, Qt


class MainWindow(QMainWindow):
    def __init__(self, processor):
        super().__init__()
        self.processor = processor
        self.setWindowTitle("μ-processor Simulator")
        self.setWindowIcon(QIcon(QApplication.instance().style().standardPixmap(QStyle.SP_FileDialogListView)))

        self.regLabels = {}
        self.programInput = QTextEdit()
        self.programInput.setStyleSheet("border: 1px solid black;")
        self.regLayout = QVBoxLayout()
        self.gridLayout = QGridLayout()

        self.initUI()

    def initUI(self):
        for reg in self.processor.registers:
            self.regLabels[reg] = QLabel()
            self.regLabels[reg].setAlignment(Qt.AlignCenter)
            self.regLayout.addWidget(self.regLabels[reg])

        regWidget = QWidget()
        regWidget.setLayout(self.regLayout)

        readButton = QPushButton("Read program")
        readButton.clicked.connect(self.readProgram)

        saveButton = QPushButton("Save program")
        saveButton.clicked.connect(self.saveProgram)

        stepButton = QPushButton("Step")
        stepButton.clicked.connect(self.stepProgram)

        runButton = QPushButton("Run")
        runButton.clicked.connect(self.runProgram)

        clearButton = QPushButton("Clear")
        clearButton.clicked.connect(self.clearProgram)

        self.gridLayout.addWidget(regWidget, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.programInput, 1, 0, 1, 2)
        self.gridLayout.addWidget(readButton, 2, 0, 1, 1)
        self.gridLayout.addWidget(saveButton, 2, 1, 1, 1)
        self.gridLayout.addWidget(runButton, 3, 0, 1, 1)
        self.gridLayout.addWidget(stepButton, 3, 1, 1, 1)
        self.gridLayout.addWidget(clearButton, 4, 0, 1, 2)

        centralWidget = QWidget()
        centralWidget.setLayout(self.gridLayout)
        self.setCentralWidget(centralWidget)
        self.updateRegisters()

    def readProgram(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Program")
        if fileName:
            with open(fileName, "r") as file:
                program = file.read().split("\n")

            self.processor.readProgram(program)
            self.programInput.setPlainText("\n".join(program))
            self.clearHighlight()
            self.updateRegisters()

    def saveProgram(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Program")
        if fileName:
            with open(fileName, "w") as file:
                file.write(self.programInput.toPlainText().strip())

    def stepProgram(self):
        line = self.processor.step()
        if line is not None:
            self.highlightLine(line - 1)
            self.updateRegisters()

    def runProgram(self):
        self.processor.run()
        self.clearHighlight()
        self.updateRegisters()

    def clearProgram(self):
        self.processor.reset()
        self.clearHighlight()
        self.updateRegisters()

    def updateRegisters(self):
        for reg in self.processor.registers:
            self.regLabels[reg].setText(self.formatRegLabel(reg))

    def formatRegLabel(self, reg):
        value = self.processor.registers[reg]
        binValue = format(value, '016b')
        hexValue = format(value, '04X')

        return f"{reg}: {' '.join([binValue[:8], binValue[8:]])} (hex: {hexValue})"

    def clearHighlight(self):
        self.highlightLine(-1)

    def highlightLine(self, lineNumber):
        cursor = self.programInput.textCursor()
        cursor.movePosition(QTextCursor.Start)
        darkFormat = QTextCharFormat()
        cursor.setCharFormat(darkFormat)

        for i in range(lineNumber):
            cursor.movePosition(QTextCursor.Down)

        if lineNumber >= 0:
            lightFormat = QTextCharFormat()
            lightFormat.setBackground(QColor("yellow"))
            cursor.setCharFormat(lightFormat)
            self.programInput.setTextCursor(cursor)
