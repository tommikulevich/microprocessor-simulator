from PySide2 import QtGui
from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog, QWidget, \
    QApplication, QStyle, QGridLayout
from PySide2.QtGui import QTextCursor, QTextCharFormat, QIcon, Qt


class MainWindow(QMainWindow):
    def __init__(self, processor):
        super().__init__()
        self.processor = processor

        # Window settings
        self.setWindowTitle("μ-processor Simulator")
        self.setWindowIcon(QIcon(QApplication.instance().style().standardPixmap(QStyle.SP_FileDialogListView)))

        font = QtGui.QFont()
        font.setItalic(True)

        self.regLabels = {}
        self.programInput = QTextEdit()
        self.programInput.setStyleSheet("border: 1px solid black;")
        self.programInput.setFont(QtGui.QFont("Courier", 11))
        self.statusLabel = QLabel()
        self.statusLabel.setFont(font)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.regLayout = QVBoxLayout()
        self.gridLayout = QGridLayout()

        self.initUI()

    def initUI(self):
        for reg in self.processor.registers:
            self.regLabels[reg] = QLabel()
            self.regLabels[reg].setAlignment(Qt.AlignCenter)
            font = QtGui.QFont("Courier", 12)
            font.setBold(True)
            self.regLabels[reg].setFont(font)
            self.regLayout.addWidget(self.regLabels[reg])

        regWidget = QWidget()
        regWidget.setLayout(self.regLayout)

        readButton = QPushButton("Read program")
        readButton.clicked.connect(self.readProgramFile)

        saveButton = QPushButton("Save program")
        saveButton.clicked.connect(self.saveProgramFile)

        stepButton = QPushButton("Step")
        stepButton.clicked.connect(self.stepProgram)

        runButton = QPushButton("Run")
        runButton.clicked.connect(self.runProgram)

        clearButton = QPushButton("Clear")
        clearButton.clicked.connect(self.clearProgram)

        self.gridLayout.addWidget(regWidget, 0, 0, 1, 2)
        self.gridLayout.addWidget(clearButton, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.programInput, 2, 0, 1, 2)
        self.gridLayout.addWidget(readButton, 3, 0, 1, 1)
        self.gridLayout.addWidget(saveButton, 3, 1, 1, 1)
        self.gridLayout.addWidget(runButton, 4, 0, 1, 1)
        self.gridLayout.addWidget(stepButton, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.statusLabel, 5, 0, 1, 2)

        centralWidget = QWidget()
        centralWidget.setLayout(self.gridLayout)
        self.setCentralWidget(centralWidget)
        self.updateRegisters()

    # -------------------------
    # Read/save program support
    # -------------------------

    def readProgramInput(self):
        if self.processor.programCounter == 0:
            program = self.programInput.toPlainText().split("\n")   # Every line is a separate command
            self.processor.readProgram(program)

    def readProgramFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Program")
        if fileName:
            with open(fileName, "r") as file:
                program = file.read().split("\n")

            self.processor.readProgram(program)
            self.programInput.setPlainText("\n".join(program))
            self.clearHighlight()
            self.updateRegisters()

            self.statusLabel.setText("File with program is loaded successfully!")

    def saveProgramFile(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Program")
        if fileName:
            with open(fileName, "w") as file:
                file.write(self.programInput.toPlainText().strip())

            self.statusLabel.setText("File with program is saved successfully!")

    # -----------------------
    # Running program support
    # -----------------------

    def stepProgram(self):
        self.statusLabel.clear()
        self.readProgramInput()

        try:
            line = self.processor.step()
            if line is not None:
                self.highlightLine(line - 1)
                self.updateRegisters()
                self.statusLabel.setText(f"Step: {line}")
            else:
                self.statusLabel.setText(f"Step: Done!")
        except Exception as e:
            self.statusLabel.setText(str(e))

    def runProgram(self):
        self.statusLabel.clear()
        self.readProgramInput()

        try:
            self.processor.run()
            self.clearHighlight()
            self.updateRegisters()
            self.statusLabel.setText(f"Continuous mode: Done!")
        except Exception as e:
            self.statusLabel.setText(str(e))

    # ----------------------------------------
    # Clearing/updating/highlighting functions
    # ----------------------------------------

    def clearProgram(self):
        self.statusLabel.clear()
        self.processor.reset()
        self.clearHighlight()
        self.updateRegisters()

    def clearHighlight(self):
        self.highlightLine(-1)

    def updateRegisters(self):
        for reg in self.processor.registers:
            self.regLabels[reg].setText(self.formatRegLabel(reg))

    def formatRegLabel(self, reg):
        value = self.processor.registers[reg]
        binValue = format(value, '016b')
        hexValue = format(value, '04X')

        return f"{reg}: {' '.join([binValue[:8], binValue[8:]])} (0x{hexValue})"

    def highlightLine(self, lineNumber):
        cursor = self.programInput.textCursor()
        cursor.movePosition(QTextCursor.Start)

        darkFormat = QTextCharFormat()
        cursor.setCharFormat(darkFormat)

        for i in range(lineNumber):
            cursor.movePosition(QTextCursor.Down)

        if lineNumber >= 0:
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)

        self.programInput.setTextCursor(cursor)
