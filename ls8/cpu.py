"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        # registers R0 thru R7
        # R5 is reserved as the interrupt mask (IM)
        # R6 is reserved as the interrupt status (IS)
        # R7 is reserved as the stack pointer (SP)
        self.registers = [0b0] * 8

        # internal registers
        self.pc = 0 # PC: Program Counter, address of the currently executing instruction
        self.ir = 0 # IR: Instruction Register, contains a copy of the currently executing instruction
        self.mar = 0 # MAR: Memory Address Register, holds the memory address we're reading or writing
        self.mdr = 0 # MDR: Memory Data Register, holds the value to write or the value just read
        self.fl = 0 # FL: Flags, see below

        self.ram = [0b0] * 255

        # opcodes
        self.OPCODES = {0b10000010: 'LDI', 0b01000111: 'PRN', 0b00000001: 'HLT', 0b10100010: 'MUL'}

    def load(self, filename: str):
        """Load a program into memory."""

        try:
            with open(filename, 'r') as f:
                lines = (line for line in f.readlines() if not (line[0]=='#' or line[0]=='\n'))
                program = [int(line.split('#')[0].strip(), 2) for line in lines]

            address = 0

            for instruction in program:
                self.ram[address] = instruction
                address += 1
        except FileNotFoundError as e:
            print(e)
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # addition
        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]

        # multiplication
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
           
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            command = self.ram[self.pc]
            try:
                op = self.OPCODES[command]
                # do LDI
                if op == 'LDI':
                    reg = self.ram[self.pc+1]
                    val = self.ram[self.pc+2]
                    self.registers[reg] = val
                    self.pc += 3

                # do Print
                elif op == 'PRN':
                    reg = self.ram[self.pc+1]
                    val = self.registers[reg]
                    print(val)
                    self.pc += 2

                # pass to alu
                elif op == 'ADD' or op == 'MUL':
                    reg_a = self.ram[self.pc+1]
                    reg_b = self.ram[self.pc+2]
                    self.alu(op, reg_a, reg_b)
                    self.pc += 3
                # exit
                elif op == 'HLT':
                    running = False
                    # self.pc += 1 # i don't know if it makes sense to do this.

            except KeyError as e:
                print(f"unknown command {command}")
                self.pc += 1
        pass

    def ram_read(self, location):
        """ read from ram

            accept the address to read and return the value stored there
        """
        return self.ram[location]

    def ram_write(self, location, value):
        """ write to ram

        accept a value to write, and the address to write it to.
        """
        self.ram[location] = value
        pass
