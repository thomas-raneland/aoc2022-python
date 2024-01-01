test_input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def parse(lines):
    tiles = set()

    for line in lines:
        points = line.split(" -> ")
        prev_pos = None

        for p in points:
            x, y = map(int, p.split(","))
            pos = (x, y)

            if prev_pos is not None:
                for x in range(min(prev_pos[0], pos[0]), max(prev_pos[0], pos[0]) + 1):
                    for y in range(min(prev_pos[1], pos[1]), max(prev_pos[1], pos[1]) + 1):
                        tiles.add((x, y))

            prev_pos = pos

    max_y = max(map(lambda p: p[1], tiles))
    return tiles, max_y


def free_pos(sand_pos):
    next_pos = [
        (sand_pos[0], sand_pos[1] + 1),
        (sand_pos[0] - 1, sand_pos[1] + 1),
        (sand_pos[0] + 1, sand_pos[1] + 1)
    ]

    first_free_pos = None

    for p in next_pos:
        if p not in tiles:
            first_free_pos = p
            break

    return first_free_pos


with open("day14.input") as file:
    lines = file.read().splitlines()

# lines = test_input.splitlines()
tiles, max_y = parse(lines)
added = 0

while True:
    sand_pos = (500, 0)
    while True:
        next_pos = free_pos(sand_pos)
        if next_pos is None or next_pos[1] > max_y:
            break
        sand_pos = next_pos
    if sand_pos[1] >= max_y:
        break
    tiles.add(sand_pos)
    added += 1

print("Part I", added)
tiles, max_y = parse(lines)
added = 0

while True:
    sand_pos = (500, 0)
    while True:
        next_pos = free_pos(sand_pos)
        if next_pos is None or next_pos[1] > max_y + 1:
            break
        sand_pos = next_pos
    if sand_pos in tiles:
        break
    tiles.add(sand_pos)
    added += 1

print("Part II", added)
