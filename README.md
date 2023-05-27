# 📟 μ-processor Simulator

> ☣ **Warning:** This project was created during my studies for educational purposes only. It may contain non-optimal solutions.

### 📑 About

Simple application that **implements a model of a microprocessor** has been created. The processor has **four 16-bit general purpose registers** named **AX**, **BX**, **CX** and **DX**, each treated as a pair of 8-bit registers (e.g. AH | AL). The list of commands includes three commands: **MOV**, **ADD** and **SUB**. The processor allows the implementation of two addressing modes: register and instant, as well as the implementation of written programs in the **full execution mode** and in the **step mode**. In step mode, the sequence of instructions is tracked. In addition, it is possible to **save** to a file and then **reload** a previously written program for further editing and restarting.

> The application is written in **Python 3.10.9**, using the Qt Framework (PySide2), in PyCharm 2023.1.2 Professional Edition.

### 🌟 Functionality

In addition to the functions listed in the description, the application allows you to **add comments** using a semicolon (everything after the semicolon is ignored by the program) and **enter in the register** not only a decimal value, but also a **binary value**, ending the string of bits with the letter b (for example, `0001b`). In addition, in case of overfilling or exceeding the range, the user is informed of this.

The **instruction syntax** is following:

`MNEMONIC ARG1, ARG2  ; COMMENT`

where the mnemonic code should be separated from the arguments by **at least one space**, and the arguments should be separated by **a comma**. Everything after **semicolons** is comments and is ignored by the program.

<p align="center">
  <img src="/_readme-img/1-main.png?raw=true" width="300" alt="Main window">
</p>

The interface includes:
- Contents of **registers** in bin and hex representation.
- `Clear` button to **clear the contents of the registers** and **reset the program counter**.
- **A text box** where you can edit the program.
- `Read program` and `Save program` buttons to **load / write a program from / to a file**.
- `Run` and `Step` buttons to **execute the program** in full execution mode and in step mode.
- **A labe**l where **errors, informational messages, etc.** are written.
