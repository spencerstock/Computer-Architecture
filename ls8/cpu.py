"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.registers[7] = 0xF4
        pass

    def load(self, path):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        program = []
        try:
            with open(path) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num != "":
                        program.append(int(num, 2))
                        

        except FileNotFoundError:
            print(f"{path} not found")
            sys.exit(2)


        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, position):
        return self.ram[position]

    def ram_write(self, position, value):
        self.ram[position] = value

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
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        pc = 0
        running = True

        while running:
            command = self.ram_read(pc)

            if command == 0b00000001:
                running = False
                pc += 1
                print("Halted")
                sys.exit(1)
            
            elif command == 0b10000010:
                reg = self.ram_read(pc + 1)
                num = self.ram_read(pc + 2)
                self.registers[reg] = num
                pc += 3

            elif command == 0b01000111:
                reg = self.ram_read(pc + 1)
                num = self.registers[reg]
                print(num)
                pc += 2

            elif command == 0b10100010:
                reg_a = self.registers[self.ram_read(pc + 1)]
                reg_b = self.registers[self.ram_read(pc + 2)]
                self.registers[self.ram_read(pc + 1)] = reg_a * reg_b
                pc += 3

            else:
                print(f"Unkown command {command}")
                pc += 1
                print(pc)
        

