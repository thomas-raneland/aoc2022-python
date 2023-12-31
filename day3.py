test_input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

with open("day3.input") as file:
    lines = file.read().splitlines()

# lines = test_input.splitlines()
total = 0


def value(c):
    return 1 + ord(c) - ord('a') if ord(c) > ord('Z') else 27 + ord(c) - ord('A')


for line in lines:
    mid = len(line) // 2
    first = line[:mid]
    second = line[mid:]
    in_both = set(first).intersection(set(second))
    total += sum(map(value, in_both))

print("Part I", total)

chunks = [lines[x:x+3] for x in range(0, len(lines), 3)]

total = 0

for chunk in chunks:
    in_all = set(chunk[0]).intersection(set(chunk[1])).intersection(set(chunk[2]))
    total += sum(map(value, in_all))

print("Part II", total)