class Microprocessor:
    def __init__(self):
        self.registers = {"AX": 0, "BX": 0, "CX": 0, "DX": 0}
        self.program = []
        self.programCounter = 0

    def readProgram(self, program):
        self.program = [line.split(";")[0].strip() for line in program]  # Ignore comments
        self.programCounter = 0

    def step(self):
        if self.programCounter < len(self.program):
            command = self.program[self.programCounter]
            self.executeCommand(command)
            self.programCounter += 1
            return self.programCounter
        else:
            return None

    def run(self):
        self.programCounter = 0
        while self.programCounter < len(self.program):
            self.step()

    def reset(self):
        self.programCounter = 0
        for key in self.registers.keys():
            self.registers[key] = 0

    def executeCommand(self, command):
        operation, operands = command.split(None, 1)  # Separate operation from operands
        operands = [operand.strip().upper() for operand in operands.split(",")]

        try:
            if operation.upper() == "MOV":
                self.mov(*operands)
            elif operation.upper() == "ADD":
                self.add(*operands)
            elif operation.upper() == "SUB":
                self.sub(*operands)
            else:
                print(f"Unknown command: {operation}")
        except IndexError:
            print(f"Invalid command: {command}")
        except ValueError:
            print(f"Invalid value in command: {command}")

    @staticmethod
    def parseValue(value):
        if value.lower().endswith("h"):
            return int(value[:-1], 16)
        elif value.lower().endswith("b"):
            return int(value[:-1], 2)
        else:
            return int(value)

    def getRegValue(self, reg):
        if reg.upper().endswith("H") or reg.upper().endswith("L"):
            reg, part = reg[:-1], reg[-1]
            value = self.registers[reg]

            if part == "H":
                return value >> 8
            else:
                return value & 0xFF
        else:
            return self.registers[reg]

    def setRegValue(self, reg, value):
        if reg.upper().endswith("H") or reg.upper().endswith("L"):
            reg, part = reg[:-1], reg[-1]

            if part == "H":
                self.registers[reg] = (self.registers[reg] & 0xFF) | (value << 8)
            else:
                self.registers[reg] = (self.registers[reg] & 0xFF00) | value
        else:
            self.registers[reg] = value

    def mov(self, dest, src):
        if src in self.registers:
            value = self.getRegValue(src)
        else:
            value = self.parseValue(src)

        self.setRegValue(dest, value)

    def add(self, dest, src):
        if src in self.registers:
            value = self.getRegValue(src)
        else:
            value = self.parseValue(src)

        self.setRegValue(dest, self.getRegValue(dest) + value)

    def sub(self, dest, src):
        if src in self.registers:
            value = self.getRegValue(src)
        else:
            value = self.parseValue(src)

        self.setRegValue(dest, self.getRegValue(dest) - value)
