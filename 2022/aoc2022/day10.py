from queue import Queue
from io import StringIO
from timeit import default_timer as timer

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_10.txt"


class VM:
    def __init__(self):
        self.register = 1
        self.cycle = 0

        self.q1 = Queue()
        self.q2 = Queue()

        self.screen = []

    @property
    def signal_strength(self):
        return self.cycle * self.register

    @property
    def ready(self):
        return self.q1.empty() and self.q2.empty()

    def next_cycle(self):
        self.cycle += 1

    def draw(self):
        row_index = (self.cycle - 1) // 40
        col_index = (self.cycle - 1) % 40

        try:
            row = self.screen[row_index]
        except IndexError:
            self.screen.append([])
            row = self.screen[row_index]

        char = "."
        if self.register - 1 <= col_index <= self.register + 1:
            char = "#"

        row.append(char)

    def finish_cycle(self) -> bool:
        while not self.q1.empty():
            instruction, *args = self.q1.get()
            getattr(self, instruction)(*args)
            self.q1.task_done()

        while not self.q2.empty():
            instruction, value = self.q2.get()
            self.q1.put((instruction, value))
            self.q2.task_done()

    def enqueue(self, cycles, instruction, *args):
        if cycles == 2:
            q = self.q2
        elif cycles == 1:
            q = self.q1

        q.put((instruction, *args))

    def noop(self):
        pass

    def addx(self, value):
        self.register += int(value)


def solve_a(input: StringIO) -> int:
    vm = VM()
    tracked_cycles = 0
    for line in input:
        command = tuple(line.split())
        if command[0] == "noop":
            vm.enqueue(1, *command)
        elif command[0] == "addx":
            vm.enqueue(2, *command)

        while not vm.ready:
            vm.next_cycle()
            if vm.cycle == 20:
                tracked_cycles += vm.signal_strength
            elif (vm.cycle - 20) % 40 == 0:
                tracked_cycles += vm.signal_strength

            vm.finish_cycle()

    return tracked_cycles


def solve_b(input: StringIO) -> int:
    vm = VM()
    for line in input:
        command = tuple(line.split())
        if command[0] == "noop":
            vm.enqueue(1, *command)
        elif command[0] == "addx":
            vm.enqueue(2, *command)

        while not vm.ready:
            vm.next_cycle()
            vm.draw()
            vm.finish_cycle()

    return "\n".join(["".join(row) for row in vm.screen])


if __name__ == "__main__":
    start_a = timer()
    input = INPUT_FILE.open("r")
    solution_a = solve_a(input)
    end_a = timer()
    print(f"Part 1: {solution_a} (time: {(end_a - start_a) * 1000.0:.6f}ms)")

    input.seek(0)
    start_b = timer()
    solution_b = solve_b(input)
    end_b = timer()
    print(f"Part 2:\n{solution_b}\n(time: {(end_b - start_b) * 1000.0:.6f}ms)")
