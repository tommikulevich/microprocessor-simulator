class Microprocessor:
    def __init__(self):
        self.registers = {"AX": 0, "BX": 0, "CX": 0, "DX": 0}
        self.programCounter = 0
        self.program = []

    # ---------------------------
    # Reading and running program
    # ---------------------------

    def readProgram(self, program):
        self.program = [line.split(";")[0].strip() for line in program]  # Ignore comments
        self.programCounter = 0

    def run(self):
        self.programCounter = 0
        while self.programCounter < len(self.program):
            self.step()
        self.programCounter = 0

    def step(self):
        if self.programCounter < len(self.program):
            command = self.program[self.programCounter]
            self.executeCommand(command)
            self.programCounter += 1
            return self.programCounter
        else:
            return None

    def reset(self):
        self.programCounter = 0
        for key in self.registers.keys():
            self.registers[key] = 0

    def executeCommand(self, command):
        try:
            operation, operands = command.split(None, 1)  # Separate operation from operands
        except ValueError:
            raise Exception(f"Invalid command or line is empty")

        operands = [operand.strip().upper() for operand in operands.split(",")]  # Separate operands

        try:
            if operation.upper() == "MOV":
                self.mov(*operands)
            elif operation.upper() == "ADD":
                self.add(*operands)
            elif operation.upper() == "SUB":
                self.sub(*operands)
            else:
                raise Exception(f"Unknown command: {operation}")
        except IndexError:
            raise Exception(f"Invalid command: {command}")
        except ValueError as e:
            raise Exception(f"Invalid value in command: {command}. Error: {str(e)}")

    # -----------------
    # Editing registers
    # -----------------

    @staticmethod
    def parseValue(value):
        if value.lower().endswith("b"):
            return int(value[:-1], 2)   # Binary representation
        else:
            return int(value)

    def getValue(self, reg):
        if reg.upper().endswith("H") or reg.upper().endswith("L"):
            reg, part = reg[0] + 'X', reg[1]
            value = self.registers[reg]

            if part == "H":
                return (value & 0xFF00) >> 8
            else:
                return value & 0xFF
        else:
            return self.registers[reg]

    def setValue(self, reg, value):
        if reg.upper().endswith("H") or reg.upper().endswith("L"):
            reg, part = reg[0] + 'X', reg[1]

            if part == "H":
                self.registers[reg] = (self.registers[reg] & 0x00FF) | (value << 8)
            else:
                self.registers[reg] = (self.registers[reg] & 0xFF00) | value
        else:
            self.registers[reg] = value

    @staticmethod
    def getRegSize(reg):
        if reg.upper().endswith("H") or reg.upper().endswith("L"):
            return 8
        else:
            return 16

    # ------------------------
    # Microprocessors commands
    # ------------------------

    def mov(self, dest, src):
        if (src[0].upper() + 'X') in self.registers:
            value = self.getValue(src)
        else:
            value = self.parseValue(src)

        regSize = self.getRegSize(dest)
        maxValue = 2 ** regSize - 1

        if not (0 <= value <= maxValue):
            raise ValueError(f"Value out of range: {value}")

        self.setValue(dest, value)

    def add(self, dest, src):
        if (src[0].upper() + 'X') in self.registers:
            value = self.getValue(src)
        else:
            value = self.parseValue(src)

        regSize = self.getRegSize(dest)
        maxValue = 2 ** regSize - 1

        if not (0 <= value <= maxValue):
            raise ValueError(f"Value out of range: {value}")

        result = self.getValue(dest) + value
        if result < 0 or result >= 2 ** 16:
            raise ValueError("Overflow error occurred")

        self.setValue(dest, self.getValue(dest) + value)

    def sub(self, dest, src):
        if (src[0].upper() + 'X') in self.registers:
            value = self.getValue(src)
        else:
            value = self.parseValue(src)

        regSize = self.getRegSize(dest)
        maxValue = 2 ** regSize - 1

        if not (0 <= value < maxValue):
            raise ValueError(f"Value out of range: {value}")

        result = self.getValue(dest) - value
        if result < 0:
            raise ValueError("Underflow error occurred")

        self.setValue(dest, self.getValue(dest) - value)
