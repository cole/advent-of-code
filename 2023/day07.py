import enum
import functools
import sys
from collections import Counter

INPUT = open(sys.argv[1]).read().strip()


class HandType(enum.IntEnum):
    HIGH_CARD = enum.auto()
    ONE_PAIR = enum.auto()
    TWO_PAIR = enum.auto()
    THREE_OF_A_KIND = enum.auto()
    FULL_HOUSE = enum.auto()
    FOUR_OF_A_KIND = enum.auto()
    FIVE_OF_A_KIND = enum.auto()


@functools.total_ordering
class Hand:
    CARD_ORDER = ("A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2")
    JOKER_CHAR = None

    def __init__(self, cards):
        self.cards = cards

    @property
    def type(self):
        chars = Counter(self.cards)
        if self.JOKER_CHAR:
            jokers = chars.pop(self.JOKER_CHAR, 0)
        else:
            jokers = 0
        counts = tuple(sorted(chars.values(), reverse=True)) or (0,)

        match (counts[0] + jokers, *counts[1:]):
            case (5, *_):
                return HandType.FIVE_OF_A_KIND
            case (4, *_):
                return HandType.FOUR_OF_A_KIND
            case (3, 2, *_):
                return HandType.FULL_HOUSE
            case (3, *_):
                return HandType.THREE_OF_A_KIND
            case (2, 2, *_):
                return HandType.TWO_PAIR
            case (2, *_):
                return HandType.ONE_PAIR
            case _:
                return HandType.HIGH_CARD

    def __str__(self):
        return self.cards

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        if self.type.value == other.type.value:
            for char_a, char_b in zip(self.cards, other.cards):
                if char_a != char_b:
                    return self.CARD_ORDER.index(char_a) > self.CARD_ORDER.index(char_b)

            return False

        return self.type.value < other.type.value


class HandWithJokers(Hand):
    CARD_ORDER = ("A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J")
    JOKER_CHAR = "J"


def part1():
    hand_bids = []
    for line in INPUT.splitlines():
        hand_cards, bid = line.split()
        hand_bids.append((Hand(hand_cards), int(bid)))

    hand_bids.sort(key=lambda i: i[0])

    total = 0
    for i, (hand, bid) in enumerate(hand_bids, start=1):
        total += i * bid

    return total


def part2():
    hand_bids = []
    for line in INPUT.splitlines():
        hand_cards, bid = line.split()
        hand_bids.append((HandWithJokers(hand_cards), int(bid)))

    hand_bids.sort(key=lambda i: i[0])

    total = 0
    for i, (hand, bid) in enumerate(hand_bids, start=1):
        total += i * bid

    return total


print(f"part 1: {part1()}")
print(f"part 2: {part2()}")
