import sys

INPUT = open(sys.argv[1]).read().strip()


class Page:
    def __init__(self, value, before_rules, after_rules):
        self.value = value
        self.before_rules = before_rules
        self.after_rules = after_rules

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"Page({self.value}, {self.before_rules}, {self.after_rules})"

    def __lt__(self, other):
        if other.value in self.after_rules:
            return True

        return False

    def __gt__(self, other):
        if other.value in self.before_rules:
            return True

        return False


class Update:
    def __init__(self, pages):
        self.pages = pages

    def __len__(self):
        return len(self.pages)

    def __eq__(self, other):
        return (p.value for p in self.pages) == (p.value for p in other.pages)

    @property
    def middle_page(self):
        return self.pages[len(self.pages) // 2]

    @property
    def is_correct(self):
        update_correct = True
        for idx, page in enumerate(self.pages):
            if idx > 0:
                for prev_val in self.pages[:idx]:
                    if page > prev_val:
                        update_correct = False

                        break
            if idx < len(self.pages) - 1:
                for next_val in self.pages[idx + 1 :]:
                    if page < next_val:
                        update_correct = False
                        break

            if not update_correct:
                break

        return update_correct

    def correct(self):
        return Update(sorted([p for p in self.pages], reverse=True))


def parse_input():
    raw_rules, raw_updates = INPUT.split("\n\n")

    rules_before = {}  # {int: [int]}
    rules_after = {}  # {int: [int]}
    for rule in raw_rules.split("\n"):
        a, b = [int(x) for x in rule.split("|")]
        rules_before.setdefault(a, set())
        rules_before[a].add(b)
        rules_after.setdefault(b, set())
        rules_after[b].add(a)

    updates = []
    for line in raw_updates.split("\n"):
        updates.append(
            Update(
                [
                    Page(
                        int(x),
                        rules_before.get(int(x), set()),
                        rules_after.get(int(x), set()),
                    )
                    for x in line.split(",")
                ]
            )
        )

    return updates


def part1():
    updates = parse_input()

    correct = 0
    correct_midpoints = []
    for update in updates:
        if update.is_correct:
            correct += 1
            correct_midpoints.append(update.middle_page.value)

    return correct_midpoints


def part2():
    updates = parse_input()

    corrected_midpoints = []
    for update in updates:
        if not update.is_correct:
            corrected = update.correct()
            corrected_midpoints.append(corrected.middle_page.value)

    return sum(corrected_midpoints)


print(part1())
print(part2())
