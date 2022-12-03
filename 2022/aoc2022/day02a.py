from io import StringIO
from typing import Tuple, Type

from .inputs import DATA_DIR

INPUT_FILE = DATA_DIR / "input_02.txt"


class Shape:
    """Base class for Rock/Paper/Scissors"""

    def beats(move: "Type[Shape]"):
        raise NotImplementedError


class Rock(Shape):
    shape_score = 1
    opponent_code = "A"
    response_code = "X"

    def beats(move: Type[Shape]):
        return move is Scissors


class Paper(Shape):
    shape_score = 2
    opponent_code = "B"
    response_code = "Y"

    def beats(move: Type[Shape]):
        return move is Rock


class Scissors(Shape):
    shape_score = 3
    opponent_code = "C"
    response_code = "Z"

    def beats(move: Type[Shape]):
        return move is Paper


openings = {shape.opponent_code: shape for shape in (Rock, Paper, Scissors)}
responses = {shape.response_code: shape for shape in (Rock, Paper, Scissors)}


def parse_round(round: str) -> Tuple[Shape, Shape]:
    opening = openings[round[0]]
    response = responses[round[2]]

    return (opening, response)


def score_response(opening: Shape, response: Shape) -> int:
    if response.beats(opening):
        return 6
    elif opening.beats(response):
        return 0
    else:
        # draw
        return 3


def check_strategy(guide: StringIO) -> int:
    total_score = 0
    for line in guide:
        opening, response = parse_round(line)
        shape_score = response.shape_score
        outcome_score = score_response(opening, response)
        total_score += shape_score
        total_score += outcome_score

    return total_score


if __name__ == "__main__":
    print(check_strategy(INPUT_FILE.open("r")))
