test_input = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

with open("day1.input") as file:
    input = file.read()

print("Part I:", max([sum(map(int, s.splitlines())) for s in input.split("\n\n")]))
print("Part II:", sum(sorted([sum(map(int, s.splitlines())) for s in input.split("\n\n")])[-3:]))
