import functools
import operator
from typing import NamedTuple

test_input = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


class Monkey(NamedTuple):
    name: str
    starting_items: []
    operation: str
    test: int
    if_true: int
    if_false: int


def parse(input):
    monkeys = []
    inspections = []
    items = []

    for s in input.split("\n\n"):
        lines = s.splitlines()
        name = lines[0][:-1]
        starting_items = list(map(int, lines[1][18:].split(", ")))
        operation = lines[2][13:]
        test = int(lines[3].split(" ")[-1])
        if_true = int(lines[4].split(" ")[-1])
        if_false = int(lines[5].split(" ")[-1])
        monkeys.append(Monkey(name, starting_items, operation, test, if_true, if_false))
        inspections.append(0)
        items.append(starting_items)

    return monkeys, inspections, items


def perform_operation(op, x):
    _, expr = op.split("=")
    a, o, b = expr.strip().split(" ")
    av = x if a == "old" else int(a)
    bv = x if b == "old" else int(b)
    return av + bv if o == "+" else av * bv


with open("day11.input") as file:
    input = file.read()

monkeys, inspections, items = parse(input)

for r in range(0, 20):
    for (i, m) in enumerate(monkeys):
        for item in items[i]:
            inspections[i] += 1
            worry_level = perform_operation(m.operation, item) // 3
            if worry_level % m.test == 0:
                items[m.if_true].append(worry_level)
            else:
                items[m.if_false].append(worry_level)
        items[i] = []

print("Part I", functools.reduce(operator.mul, sorted(inspections)[-2:]))
monkeys, inspections, items = parse(input)
divisor = functools.reduce(operator.mul, map(lambda m: m.test, monkeys))

for r in range(0, 10000):
    for (i, m) in enumerate(monkeys):
        for item in items[i]:
            inspections[i] += 1
            worry_level = perform_operation(m.operation, item) % divisor
            if worry_level % m.test == 0:
                items[m.if_true].append(worry_level)
            else:
                items[m.if_false].append(worry_level)
        items[i] = []

print("Part II", functools.reduce(operator.mul, sorted(inspections)[-2:]))
