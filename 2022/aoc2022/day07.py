from io import StringIO
from timeit import default_timer as timer
from typing import Dict, Optional, NamedTuple

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_07.txt"


class FileEntry(NamedTuple):
    name: str
    size: int


class DirEntry(NamedTuple):
    name: str
    files: Dict[str, FileEntry]
    dirs: Dict[str, "DirEntry"]
    parent: Optional["DirEntry"] = None

    @classmethod
    def build_tree(cls, input: StringIO):
        root = cls(name="/", files={}, dirs={})
        pwd = root
        is_listing = False

        for line in input:
            if line == "$ ls\n":
                is_listing = True
            elif line.startswith("$"):
                is_listing = False

            if line == "$ cd /\n":
                # clear current dir
                pwd = root
            elif line == "$ cd ..\n":
                # move up one dir
                pwd = pwd.parent
            elif line.startswith("$ cd "):
                # add to path
                pwd = pwd.dirs[line[5:].strip()]
            elif line.startswith("dir "):
                # add dir to our 'filesystem'
                pwd.add_subdir(line[4:].rstrip("\n"))
            elif not line.startswith("$"):
                if not is_listing:
                    raise ValueError("Not in ls output")
                # an actual file!
                size, name = line.rstrip("\n").split(" ")
                pwd.add_file(name, int(size))

        return root

    def add_file(self, name: str, size: int):
        self.files[name] = FileEntry(name=name, size=size)

    def add_subdir(self, name: str):
        self.dirs[name] = DirEntry(name=name, files={}, dirs={}, parent=self)

    @property
    def full_path(self):
        path = self.name
        parent = self.parent
        while parent:
            if parent.name == "/":
                path = f"/{path}"
                break
            path = f"{parent.name}/{path}"
            parent = parent.parent

        return path

    @property
    def size(self):
        total_size = 0
        for file in self.files.values():
            total_size += file.size
        for subdir in self.dirs.values():
            total_size += subdir.size

        return total_size

    def walk(self, level=0):
        if level > 100:
            raise ValueError("too deep!")
        yield self, level
        for subdir in self.dirs.values():
            yield from subdir.walk(level=level + 1)

    def pretty_print(self):
        for dir_entry, level in self.walk():
            print(f'{level * "  "} - {dir_entry.name} (dir)')
            for file in dir_entry.files.values():
                print(f'{(level + 1) * "  "} - {file.name} (file, size={file.size})')


def solve_a(input: StringIO) -> int:
    filesystem = DirEntry.build_tree(input)
    dirs_under_10k = [
        entry[0] for entry in filesystem.walk() if entry[0].size <= 100_000
    ]
    return sum([entry.size for entry in dirs_under_10k])


def solve_b(input: StringIO) -> int:
    filesystem = DirEntry.build_tree(input)
    free_space = 70_000_000 - filesystem.size
    required_space = 30_000_000
    needed_space = required_space - free_space

    dir_sizes = [
        entry[0] for entry in filesystem.walk() if entry[0].size >= needed_space
    ]
    dir_sizes.sort(key=lambda d: d.size)

    return dir_sizes[0].size


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
    print(f"Part 2: {solution_b} (time: {(end_b - start_b) * 1000.0:.6f}ms)")
