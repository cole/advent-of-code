import concurrent.futures
import sys

INPUT = open(sys.argv[1]).read().strip()


class Computer:
    def __init__(self, definition, force_register_a=None):
        self.registers = {"A": None, "B": None, "C": None}
        self.pointer = 0
        self.outputs = []
        self.program = []

        self.opcodes = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

        for register in ("A", "B", "C"):
            for line in definition.split("\n"):
                if line.startswith(f"Register {register}"):
                    self.registers[register] = int(line.split()[-1])

        if force_register_a is not None:
            self.registers["A"] = force_register_a

        self.program = [
            int(val)
            for val in definition.split("\n")[-1].replace("Program: ", "").split(",")
        ]

    @classmethod
    def check_register_a_value(cls, register_value):
        computer = cls(INPUT, force_register_a=register_value)
        computer.run(return_early=True)

        if computer.outputs == computer.program:
            return register_value

    def combo_operand(self, operand):
        match operand:
            case 4:
                return self.registers["A"]
            case 5:
                return self.registers["B"]
            case 4:
                return self.registers["C"]
            case _:
                return operand

    def adv(self, operand):
        val = self.registers["A"] // (2 ** self.combo_operand(operand))
        truncated = int(str(f"{val}").split(".")[0])
        self.registers["A"] = truncated

    def bxl(self, operand):
        val = self.registers["B"] ^ operand
        self.registers["B"] = val

    def bst(self, operand):
        val = self.combo_operand(operand) % 8
        self.registers["B"] = val

    def jnz(self, operand):
        if self.registers["A"] == 0:
            return None

        self.pointer = operand
        return operand

    def bxc(self, _operand):
        self.registers["B"] = self.registers["B"] ^ self.registers["C"]

    def out(self, operand):
        val = self.combo_operand(operand) % 8
        self.outputs.append(val)

    def bdv(self, operand):
        val = self.registers["A"] // (2 ** self.combo_operand(operand))
        truncated = int(str(f"{val}").split(".")[0])
        self.registers["B"] = truncated

    def cdv(self, operand):
        val = self.registers["A"] // (2 ** self.combo_operand(operand))
        truncated = int(str(f"{val}").split(".")[0])
        self.registers["C"] = truncated

    def run(self, return_early=False, debug=False):
        while self.pointer <= len(self.program):
            try:
                opcode = self.program[self.pointer]
                operand = self.program[self.pointer + 1]
            except IndexError:
                break

            instruction = self.opcodes[opcode]

            if debug:
                print(f"{opcode=} {operand=} {str(instruction.__name__)}")

            jump = instruction(operand)
            if jump is not None:
                self.pointer = jump
            else:
                self.pointer += 2

            if (
                return_early
                and self.outputs
                and not (self.outputs == self.program[: len(self.outputs)])
            ):
                break


def part1():
    computer = Computer(INPUT)
    computer.run()
    return ",".join([str(x) for x in computer.outputs])


def part2():
    value_checks = range(130_000_000, 170_000_000)

    with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
        for result in executor.map(
            Computer.check_register_a_value, value_checks, chunksize=1_000_000
        ):
            if result is not None:
                return result


if __name__ == "__main__":
    print(part1())
    print(part2())
