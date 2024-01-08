import re
from enum import Enum


class Facing(Enum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    def left(self):
        return Facing((self.value + 3) % 4)

    def right(self):
        return Facing((self.value + 1) % 4)

    def opposite(self):
        return Facing((self.value + 2) % 4)


def parse(data):
    board_map, path = data.split("\n\n")

    board = {}

    for y, line in enumerate(board_map.splitlines()):
        for x in range(0, len(line)):
            if line[x] != " ":
                board[(x, y)] = line[x]

    pattern = r"(\d+)|(L)|(R)"
    matches = list(re.finditer(pattern, path))
    return board, matches


def part_i(data):
    board, matches = parse(data)
    pos = min([b for b in board if b[1] == 0], key=lambda b: b[0])
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    facing = 0

    for match in matches:
        if match[0] == "L":
            facing = (facing + 3) % 4
        elif match[0] == "R":
            facing = (facing + 1) % 4
        else:
            for i in range(0, int(match[0])):

                new_pos = (pos[0] + dx[facing], pos[1] + dy[facing])
                if new_pos not in board.keys():
                    if dx[facing] == 1:
                        new_pos = min([b for b in board if b[1] == pos[1]], key=lambda b: b[0])
                    elif dx[facing] == -1:
                        new_pos = max([b for b in board if b[1] == pos[1]], key=lambda b: b[0])
                    elif dy[facing] == 1:
                        new_pos = min([b for b in board if b[0] == pos[0]], key=lambda b: b[1])
                    elif dy[facing] == -1:
                        new_pos = max([b for b in board if b[0] == pos[0]], key=lambda b: b[1])
                if board[new_pos] == "#":
                    break
                pos = new_pos

    password = 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + facing
    print("Part I", password)


def part_ii(data, wormholes):
    board, matches = parse(data)
    pos = min([b for b in board if b[1] == 0], key=lambda b: b[0])
    facing: Facing = Facing.EAST

    for match in matches:
        if match[0] == "L":
            facing = facing.left()
        elif match[0] == "R":
            facing = facing.right()
        else:
            for i in range(0, int(match[0])):
                new_pos, new_facing = move(pos, facing, wormholes)
                if board[new_pos] == "#":
                    break
                pos = new_pos
                facing = new_facing

    password = 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + facing.value
    print("Part II", password)


def segment(x1, y1, x2, y2, scale):
    points = []

    if y1 != y2:
        for i in range(0, scale):
            points.append((x1 * scale, y1 * scale + i * (y2 - y1) + (0 if y1 < y2 else -1)))
    elif x1 != x2:
        for i in range(0, scale):
            points.append((x1 * scale + i * (x2 - x1) + (0 if x1 < x2 else -1), y1 * scale))

    return points


def walk(pos, facing):
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    return pos[0] + dx[facing.value], pos[1] + dy[facing.value]


def move(pos, facing, wormholes):
    found_pos = None
    found_facing = None
    search_pos = walk(pos, facing) if facing in [Facing.EAST, Facing.SOUTH] else pos

    for wh in wormholes:
        if wh[0] == search_pos and wh[1] == facing:
            found_pos, found_facing = wh[2], wh[3]
            break
        if wh[2] == search_pos and wh[3] == facing.opposite():
            found_pos, found_facing = wh[0], wh[1].opposite()
            break

    if found_pos is not None:
        return found_pos if found_facing in [Facing.EAST, Facing.SOUTH] else walk(found_pos, found_facing), found_facing

    return walk(pos, facing), facing


def test_wormholes():
    scale = 4
    wormholes = []
    wormholes.extend(zip(segment(2, 0, 3, 0, scale), [Facing.NORTH] * scale,
                         segment(1, 1, 0, 1, scale), [Facing.SOUTH] * scale))
    wormholes.extend(zip(segment(3, 0, 3, 1, scale), [Facing.EAST] * scale,
                         segment(4, 3, 4, 2, scale), [Facing.WEST] * scale))
    wormholes.extend(zip(segment(3, 1, 3, 2, scale), [Facing.EAST] * scale,
                         segment(4, 2, 3, 2, scale), [Facing.SOUTH] * scale))
    wormholes.extend(zip(segment(3, 3, 4, 3, scale), [Facing.SOUTH] * scale,
                         segment(0, 1, 0, 2, scale), [Facing.EAST] * scale))
    wormholes.extend(zip(segment(2, 3, 3, 3, scale), [Facing.SOUTH] * scale,
                         segment(1, 2, 0, 2, scale), [Facing.NORTH] * scale))
    wormholes.extend(zip(segment(2, 2, 2, 3, scale), [Facing.WEST] * scale,
                         segment(2, 2, 1, 2, scale), [Facing.NORTH] * scale))
    wormholes.extend(zip(segment(1, 1, 2, 1, scale), [Facing.NORTH] * scale,
                         segment(2, 0, 2, 1, scale), [Facing.EAST] * scale))
    return wormholes


# see day22-wormholes.png for folding instructions
def file_wormholes():
    scale = 50
    wormholes = []
    wormholes.extend(zip(segment(1, 0, 2, 0, scale), [Facing.NORTH] * scale,
                         segment(0, 3, 0, 4, scale), [Facing.EAST] * scale))
    wormholes.extend(zip(segment(2, 0, 3, 0, scale), [Facing.NORTH] * scale,
                         segment(0, 4, 1, 4, scale), [Facing.NORTH] * scale))
    wormholes.extend(zip(segment(3, 0, 3, 1, scale), [Facing.EAST] * scale,
                         segment(2, 3, 2, 2, scale), [Facing.WEST] * scale))
    wormholes.extend(zip(segment(2, 1, 3, 1, scale), [Facing.SOUTH] * scale,
                         segment(2, 1, 2, 2, scale), [Facing.WEST] * scale))
    wormholes.extend(zip(segment(1, 3, 2, 3, scale), [Facing.SOUTH] * scale,
                         segment(1, 3, 1, 4, scale), [Facing.WEST] * scale))
    wormholes.extend(zip(segment(0, 2, 0, 3, scale), [Facing.WEST] * scale,
                         segment(1, 1, 1, 0, scale), [Facing.EAST] * scale))
    wormholes.extend(zip(segment(0, 2, 1, 2, scale), [Facing.NORTH] * scale,
                         segment(1, 1, 1, 2, scale), [Facing.EAST] * scale))
    return wormholes


def day22():
    test_input = """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

    part_i(test_input[1:])
    part_ii(test_input[1:], test_wormholes())

    with open("day22.input") as file:
        file_input = file.read()

    part_i(file_input)
    part_ii(file_input, file_wormholes())


day22()
