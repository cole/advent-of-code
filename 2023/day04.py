import sys

INPUT = open(sys.argv[1]).read().strip()

# INPUT = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def part1():
    score = 0
    for line in INPUT.splitlines():
        winners, numbers = line.split("|")
        _, winners = winners.split(":")

        winners = set([int(n.strip()) for n in winners.split(" ") if n.strip()])
        numbers = list(int(n.strip()) for n in numbers.split(" ") if n.strip())
        winning_numbers = [n for n in numbers if n in winners]

        card_score = 0
        for i, _ in enumerate(winning_numbers):
            if i == 0:
                card_score += 1
            else:
                card_score = card_score * 2

        score += card_score

    return score


def part2():
    copies = {}
    max_cards = len(INPUT.splitlines())
    for line in INPUT.splitlines():
        winners, numbers = line.split("|")
        card_num, winners = winners.split(":")
        _, card_num = card_num.split()
        card_num = int(card_num)

        copies.setdefault(card_num, 0)
        copies[card_num] += 1

        winners = set([int(n.strip()) for n in winners.split(" ") if n.strip()])
        numbers = list(int(n.strip()) for n in numbers.split(" ") if n.strip())
        winning_numbers = [n for n in numbers if n in winners]

        for _ in range(copies[card_num]):
            for x in range(card_num + 1, card_num + len(winning_numbers) + 1):
                if x > max_cards:
                    continue

                copies.setdefault(x, 0)
                copies[x] += 1

    return sum(copies.values())


print(f"part 1: {part1()}")
print(f"part 2: {part2()}")
