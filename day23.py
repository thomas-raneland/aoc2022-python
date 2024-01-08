def empty_tiles(positions):
    min_x = min(map(lambda p: p[0], positions))
    max_x = max(map(lambda p: p[0], positions))
    min_y = min(map(lambda p: p[1], positions))
    max_y = max(map(lambda p: p[1], positions))
    return (max_y - min_y + 1) * (max_x - min_x + 1) - len(positions)


def parse(data):
    positions = []

    for y, line in enumerate(data.splitlines()):
        for x in range(0, len(line)):
            if line[x] == "#":
                positions.append((x, y))

    return set(positions)


n = lambda p: (p[0], p[1] - 1)
s = lambda p: (p[0], p[1] + 1)
w = lambda p: (p[0] - 1, p[1])
e = lambda p: (p[0] + 1, p[1])

tests = [
    lambda ps, p: n(p) if ps.isdisjoint([n(p), n(e(p)), n(w(p))]) else None,
    lambda ps, p: s(p) if ps.isdisjoint([s(p), s(e(p)), s(w(p))]) else None,
    lambda ps, p: w(p) if ps.isdisjoint([w(p), n(w(p)), s(w(p))]) else None,
    lambda ps, p: e(p) if ps.isdisjoint([e(p), n(e(p)), s(e(p))]) else None
]


def first_valid_direction(position_set, pos, round_nbr):
    if position_set.isdisjoint([n(w(pos)), n(pos), n(e(pos)), w(pos), e(pos), s(w(pos)), s(pos), s(e(pos))]):
        return pos

    new_pos = pos

    for t in range(round_nbr, round_nbr + 4):
        ix = t % 4
        p = tests[ix](position_set, pos)
        if p is not None:
            new_pos = p
            break

    return new_pos


def move(positions, round_nbr):
    # first half
    old_to_new = {}
    new_to_old = {}

    for p in positions:
        new_p = first_valid_direction(positions, p, round_nbr)

        if new_p in new_to_old:
            old_to_new.pop(new_to_old[new_p], None)
        else:
            old_to_new[p] = new_p
            new_to_old[new_p] = p

    # second half
    new_positions = set()

    for p in positions:
        new_positions.add(old_to_new[p] if p in old_to_new else p)

    return new_positions


def display(positions):
    min_x = min(map(lambda p: p[0], positions))
    max_x = max(map(lambda p: p[0], positions))
    min_y = min(map(lambda p: p[1], positions))
    max_y = max(map(lambda p: p[1], positions))
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print("#" if (x, y) in positions else ".", end="")
        print()
    print()


def part_i(data):
    positions = parse(data)

    for i in range(0, 10):
        positions = move(positions, i)

    print("Part I", empty_tiles(positions))


def part_ii(data):
    round_nbr = 0
    positions = parse(data)
    new_positions = move(positions, round_nbr)

    while not new_positions.issubset(positions):
        positions = new_positions
        round_nbr += 1
        new_positions = move(positions, round_nbr)

    print("Part II", round_nbr + 1)


def day23():
    test_input = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

    part_i(test_input)
    part_ii(test_input)

    with open("day23.input") as file:
        file_input = file.read()

    part_i(file_input)
    part_ii(file_input)


day23()
