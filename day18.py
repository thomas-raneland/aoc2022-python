from typing import NamedTuple


class Cube(NamedTuple):
    x: int
    y: int
    z: int

    def sides(self):
        return [
            (self.x - 0.5, self.y, self.z),
            (self.x + 0.5, self.y, self.z),
            (self.x, self.y - 0.5, self.z),
            (self.x, self.y + 0.5, self.z),
            (self.x, self.y, self.z - 0.5),
            (self.x, self.y, self.z + 0.5)
        ]


def parse(data):
    cubes = set()

    for line in data.splitlines():
        x, y, z = map(int, line.split(","))
        cubes.add(Cube(x, y, z))

    return cubes


def surface_area(cubes):
    sides = set()
    multi_sides = set()
    for cube in cubes:
        for side in cube.sides():
            if side in sides:
                multi_sides.add(side)
            else:
                sides.add(side)
    return len(sides) - len(multi_sides)


def is_outside(space, cubes, min_x, outside, inside):
    queue = [space]
    visited = set()
    while len(queue) > 0:
        cube = queue.pop(0)
        if cube not in cubes and cube not in visited:
            visited.add(cube)
            if cube.x < min_x or cube in outside:
                return True, visited
            if cube in inside:
                break
            for (dx, dy, dz) in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
                queue.append(Cube(cube.x + dx, cube.y + dy, cube.z + dz))
    return False, visited


def fill(cubes):
    min_x = min(map(lambda c: c.x, cubes))
    max_x = max(map(lambda c: c.x, cubes))
    min_y = min(map(lambda c: c.y, cubes))
    max_y = max(map(lambda c: c.y, cubes))
    min_z = min(map(lambda c: c.z, cubes))
    max_z = max(map(lambda c: c.z, cubes))
    outside = set()
    inside = set()
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                space = Cube(x, y, z)
                if space not in cubes:
                    was_outside, visited = is_outside(space, cubes, min_x, outside, inside)
                    (outside if was_outside else inside).update(visited)
                    if not was_outside:
                        cubes.add(space)


def part_i(data):
    cubes = parse(data)
    print("Part I", surface_area(cubes))


def part_ii(data):
    cubes = parse(data)
    fill(cubes)
    print("Part II", surface_area(cubes))


def day18():
    test_input = """2,2,2
    1,2,2
    3,2,2
    2,1,2
    2,3,2
    2,2,1
    2,2,3
    2,2,4
    2,2,6
    1,2,5
    3,2,5
    2,1,5
    2,3,5"""
    part_i(test_input)
    part_ii(test_input)
    with open("day18.input") as file:
        file_input = file.read()
    part_i(file_input)
    part_ii(file_input)


day18()
