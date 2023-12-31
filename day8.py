test_input = """30373
25512
65332
33549
35390"""

with open("day8.input") as file:
    input = file.read()

# input = test_input

grid = [[*line] for line in input.splitlines()]


def visible(x, y, dx, dy):
    height = grid[y][x]
    x += dx
    y += dy

    while x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid):
        if grid[y][x] >= height:
            return False
        x += dx
        y += dy

    return True


def viewing_distance(x, y, dx, dy):
    height = grid[y][x]
    x += dx
    y += dy
    distance = 0

    while x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid):
        distance += 1
        if grid[y][x] >= height:
            break
        x += dx
        y += dy

    return distance


count = 0
max_scenic_score = 0

for y in range(0, len(grid)):
    for x in range(0, len(grid[0])):
        if visible(x, y, 1, 0) or visible(x, y, -1, 0) \
                or visible(x, y, 0, 1) or visible(x, y, 0, -1):
            count += 1
        scenic_score = viewing_distance(x,y,1,0) * viewing_distance(x,y,-1,0) \
            * viewing_distance(x,y,0,1) * viewing_distance(x,y,0,-1)
        max_scenic_score = max(max_scenic_score, scenic_score)

print("Part I", count)
print("Part II", max_scenic_score)
