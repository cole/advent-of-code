from io import StringIO
from aoc2022.day07 import solve_a, solve_b


TEST_DATA = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


def test_solve_a():
    input = StringIO(TEST_DATA)
    assert solve_a(input) == 95437


def test_solve_b():
    input = StringIO(TEST_DATA)
    assert solve_b(input) == 24933642
