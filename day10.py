test_input = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

with open("day10.input") as file:
    lines = file.read().splitlines()

# lines = test_input.splitlines()
line_nbr = 0
x = 1
cycle = 0
period = (cycle - 20) // 40
total = 0
crt = ""

while cycle < 241:
    line = lines[line_nbr]
    line_nbr = (line_nbr + 1) % len(lines)
    prev_period = period

    for i in range(0, 1 if line == "noop" else 2):
        crt += "#" if abs(x - cycle % 40) < 2 else "."
        cycle += 1

    period = (cycle - 20) // 40

    if period > prev_period:
        total += x * (period * 40 + 20)

    if line != "noop":
        x += int(line[5:])

print("Part I", total)
print("Part II")

for i in range(0, 6):
    print(crt[i * 40:(i + 1) * 40])
