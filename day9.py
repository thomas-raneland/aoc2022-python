from math import copysign

test_input = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

with open("day9.input") as file:
    input = file.read()

# input = test_input

positions = [set(), set(), set(), set(), set(), set(), set(), set(), set(), set()]
rope = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]

for line in input.splitlines():
    direction, steps = line.split(" ")
    dx = 1 if direction == "R" else -1 if direction == "L" else 0
    dy = 1 if direction == "D" else -1 if direction == "U" else 0

    for i in range(0, int(steps)):
        rope[0] = (rope[0][0] + dx, rope[0][1] + dy)

        for k in range(0, len(rope) - 1):
            head_pos = rope[k]
            tail_pos = rope[k + 1]
            diff = (head_pos[0] - tail_pos[0], head_pos[1] - tail_pos[1])
            if diff[0] == 0 and abs(diff[1]) == 2:
                tail_pos = (tail_pos[0], tail_pos[1] + diff[1] / 2)
            elif diff[1] == 0 and abs(diff[0]) == 2:
                tail_pos = (tail_pos[0] + diff[0] / 2, tail_pos[1])
            elif abs(diff[0]) + abs(diff[1]) > 2:
                tail_pos = (tail_pos[0] + copysign(1, diff[0]), tail_pos[1] + copysign(1, diff[1]))
            rope[k + 1] = tail_pos
            positions[k + 1].add(tail_pos)

print("Part I", len(positions[1]))
print("Part II", len(positions[9]))
