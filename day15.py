import re
from typing import NamedTuple

test_input = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


class Sensor(NamedTuple):
    x: int
    y: int
    radius: int

    def cover(self, y_coord):
        y_dist = abs(y_coord - self.y)
        return (0, 0) if y_dist > self.radius else (self.x - self.radius + y_dist,
                                                    self.x + self.radius - y_dist + 1)


with open("day15.input") as file:
    input, the_y, max_coord = file.read(), 2000000, 4000000

#input, the_y, max_coord = test_input, 10, 20
sensors = []
beacons = []

for line in input.splitlines():
    x1, y1, x2, y2 = map(int, re.findall(r"[-]?\d+", line))
    sensors.append(Sensor(x1, y1, abs(x2 - x1) + abs(y2 - y1)))
    beacons.append((x2, y2))

covered_positions = set()

for sensor in sensors:
    r = sensor.cover(the_y)
    for pos in range(r[0], r[1]):
        covered_positions.add(pos)

for b in beacons:
    if b[1] == the_y:
        covered_positions.discard(b[0])

print("Part I", len(covered_positions))

for y in range(0, max_coord + 1):
    for x in range(0,  max_coord+1):
        free = True

        for sensor in sensors:
            r = sensor.cover(y)
            if x >= r[0] and x < r[1]:
                x = r[1]
                free = False

        if free:
            print("Part II", (x, y), x * 4000000 + y)
            exit(0)
