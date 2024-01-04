from typing import NamedTuple


class RockPos(NamedTuple):
    rock_index: int
    location: tuple

    def fall(self):
        return RockPos(self.rock_index, (self.location[0], self.location[1] + 1))

    def push(self, dx):
        return RockPos(self.rock_index, (self.location[0] + dx, self.location[1]))

    def min_y(self):
        return min(map(lambda pos: pos[1] + self.location[1], rocks[self.rock_index]))

    def positions(self):
        return set(map(lambda pos: (pos[0] + self.location[0], pos[1] + self.location[1]), rocks[self.rock_index]))


def find_cycle():
    for length in range(1, len(heights) // 5):
        height = heights[-1] - heights[-1 - length]

        if height == heights[-1 - length] - heights[-1 - length * 2] \
                and height == heights[-1 - length] - heights[-1 - length * 2] \
                and height == heights[-1 - length * 2] - heights[-1 - length * 3] \
                and height == heights[-1 - length * 3] - heights[-1 - length * 4] \
                and height == heights[-1 - length * 4] - heights[-1 - length * 5]:
            return length, height

    return -1, -1


rocks = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, -1), (1, -1), (2, -1), (1, -2)],
    [(0, 0), (1, 0), (2, 0), (2, -1), (2, -2)],
    [(0, 0), (0, -1), (0, -2), (0, -3)],
    [(0, 0), (1, 0), (0, -1), (1, -1)]
]
rock_index = 0

test_input = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

with open("day17.input") as file:
    file_input = file.read()

jet_pattern = file_input
jet_index = 0

heights = []
stopped_positions = set()
min_y = 0
answers = {}

while len(answers) < 2:
    falling = RockPos(rock_index, (2, min_y - 4))
    rock_index = (rock_index + 1) % len(rocks)

    while True:
        pushed = falling.push(1 if jet_pattern[jet_index] == ">" else -1)
        jet_index = (jet_index + 1) % len(jet_pattern)

        if all(0 <= crds[0] < 7 for crds in pushed.positions()) and pushed.positions().isdisjoint(stopped_positions):
            falling = pushed

        fell = falling.fall()

        if fell.location[1] < 0 and fell.positions().isdisjoint(stopped_positions):
            falling = fell
        else:
            break

    stopped_positions.update(falling.positions())
    min_y = min(min_y, falling.min_y())
    heights.append(-min_y)

    if len(heights) == 2022:
        answers["Part I"] = heights[-1]

    if len(heights) % (len(rocks) * len(jet_pattern)) == 0:
        cycle_length, cycle_height = find_cycle()

        if cycle_length != -1:
            total_rocks = 1000000000000
            heights_before_cycles = heights[-1]
            height_for_cycles = (total_rocks - len(heights)) // cycle_length * cycle_height
            length_after_cycles = (total_rocks - len(heights)) % cycle_length
            height_after_cycles = heights[-1 - cycle_length + length_after_cycles] - heights[-1 - cycle_length]
            answers["Part II"] = heights_before_cycles + height_for_cycles + height_after_cycles

for k, v in answers.items():
    print(k, v)