def parse(data):
    initial_blizzards = {}
    width = 0
    height = 0

    for y, line in enumerate(data.splitlines()[1:-1]):
        height += 1
        width = len(line[1:-1])

        for x in range(0, len(line) - 2):
            blizzard = line[x + 1]

            if blizzard != ".":
                if (x, y) not in initial_blizzards:
                    initial_blizzards[(x, y)] = []
                initial_blizzards[(x, y)].append(blizzard)

    return initial_blizzards, width, height, (0, -1), (width - 1, height)


def update_blizzards(blizzards, width, height, time, cache):
    if time in cache:
        return cache[time]

    new_blizzards = {}

    for (x, y) in blizzards:
        for blizzard in blizzards[(x, y)]:
            pos = None

            match blizzard:
                case "^":
                    pos = (x, (y + height - 1) % height)
                case ">":
                    pos = ((x + 1) % width, y)
                case "<":
                    pos = ((x + width - 1) % width, y)
                case "v":
                    pos = (x, (y + 1) % height)

            if pos is not None:
                if pos not in new_blizzards:
                    new_blizzards[pos] = []
                new_blizzards[pos].append(blizzard)

    cache[time] = new_blizzards
    return new_blizzards


def bfs(initial_blizzards, width, height, start, goal):
    cache = {}
    states = [(0, start, initial_blizzards, [])]
    seen = set()

    while states:
        time, pos, blizzards, history = states.pop(0)

        if pos not in [start, goal]:
            if not (0 <= pos[0] < width and 0 <= pos[1] < height) or pos in blizzards or (time, pos) in seen:
                continue

        seen.add((time, pos))
        new_history = history + [(pos, blizzards)]

        if pos == goal:
            return time, new_history

        new_blizzards = update_blizzards(blizzards, width, height, time + 1, cache)
        states.append((time + 1, pos, new_blizzards, new_history))
        states.append((time + 1, (pos[0] + 1, pos[1]), new_blizzards, new_history))
        states.append((time + 1, (pos[0] - 1, pos[1]), new_blizzards, new_history))
        states.append((time + 1, (pos[0], pos[1] + 1), new_blizzards, new_history))
        states.append((time + 1, (pos[0], pos[1] - 1), new_blizzards, new_history))

    raise Exception("Path not found")


def display(history, width, height):
    for (pos, blizzards) in history:
        for y in range(0, height):
            for x in range(0, width):
                b = "E" if (x, y) == pos else "."
                if (x, y) in blizzards:
                    bs = blizzards[(x, y)]
                    b = str(len(bs)) if len(bs) > 1 else bs[0]
                print(b, end="")
            print()
        print()


def part_i(data):
    initial_blizzards, width, height, start, goal = parse(data)
    time, history = bfs(initial_blizzards, width, height, start, goal)
    print("Part I", time)


def part_ii(data):
    initial_blizzards, width, height, start, goal = parse(data)
    time1, history1 = bfs(initial_blizzards, width, height, start, goal)
    time2, history2 = bfs(history1[-1][1], width, height, goal, start)
    time3, history3 = bfs(history2[-1][1], width, height, start, goal)
    print("Part II", time1 + time2 + time3)


test_input = """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""[1:]

part_i(test_input)
part_ii(test_input)

with open("day24.input") as file:
    file_input = file.read()

part_i(file_input)
part_ii(file_input)
