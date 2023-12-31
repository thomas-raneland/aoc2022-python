from enum import Enum

test_input = """A Y
B X
C Z"""


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    A = 1
    B = 2
    C = 3
    X = 1
    Y = 2
    Z = 3


def beats(me, opp):
    return me.value == opp.value % 3 + 1


with open("day2.input") as file:
    lines = file.read().splitlines()

# lines = test_input.splitlines()

# part I
total = 0

for line in lines:
    opp, me = map(lambda x: Shape[x], line.split(" "))
    total += me.value + (6 if beats(me, opp) else 3 if me.value == opp.value else 0)

print("Part I:", total)


# part II
def win(opp):
    return Shape.ROCK if opp == Shape.SCISSORS \
        else Shape.PAPER if opp == Shape.ROCK \
        else Shape.SCISSORS


def lose(opp):
    return Shape.ROCK if opp == Shape.PAPER \
        else Shape.PAPER if opp == Shape.SCISSORS \
        else Shape.SCISSORS


total = 0

for line in lines:
    opp_str, outcome_str = line.split(" ")
    opp = Shape[opp_str]
    me = opp if outcome_str == 'Y' else win(opp) if outcome_str == 'Z' else lose(opp)
    total += me.value + (6 if beats(me, opp) else 3 if me.value == opp.value else 0)

print("Part II:", total)
