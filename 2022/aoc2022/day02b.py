from io import StringIO
from typing import Tuple

from .inputs import DATA_DIR
from .day02a import Paper, Rock, Scissors, Shape, score_response

INPUT_FILE = DATA_DIR / "input_02.txt"

openings = {shape.opponent_code: shape for shape in (Rock, Paper, Scissors)}
winning_responses = {
    opening: response
    for opening in (Rock, Paper, Scissors)
    for response in (Rock, Paper, Scissors)
    if response.beats(opening)
}
loss_responses = {
    opening: response
    for opening in (Rock, Paper, Scissors)
    for response in (Rock, Paper, Scissors)
    if opening.beats(response)
}
draw_responses = {
    opening: response
    for opening in (Rock, Paper, Scissors)
    for response in (Rock, Paper, Scissors)
    if not (opening.beats(response) or response.beats(opening))
}


def parse_round(round: str) -> Tuple[Shape, Shape]:
    opening = openings[round[0]]
    response_code = round[2]
    if response_code == "X":
        response = loss_responses[opening]
    elif response_code == "Y":
        response = draw_responses[opening]
    elif response_code == "Z":
        response = winning_responses[opening]
    else:
        raise ValueError("Invalid response code")

    return (opening, response)


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
