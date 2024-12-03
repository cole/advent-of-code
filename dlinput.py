# Source: https://github.com/jonathanpaulson/AdventOfCode/blob/master/get_input.py

import argparse
import os
import subprocess
import sys

# Usage: AOC_SESSION=... python dlinput.py 1 > 2023/day01.in

SESSION = os.environ["AOC_SESSION"]

parser = argparse.ArgumentParser(description="Read input")
parser.add_argument("year", type=int)
parser.add_argument("day", type=int)
args = parser.parse_args()

cmd = f'curl -s https://adventofcode.com/{args.year}/day/{args.day}/input --cookie "session={SESSION}"'
output = subprocess.check_output(cmd, shell=True)
output = output.decode("utf-8")
print(output, end="")
print("\n".join(output.split("\n")[:10]), file=sys.stderr)
