test_input = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

with open("day4.input") as file:
    lines = file.read().splitlines()

# lines = test_input.splitlines()

countI = 0
countII = 0

for line in lines:
    a, b = line.split(",")
    aMin, aMax = map(int, a.split("-"))
    bMin, bMax = map(int, b.split("-"))
    if aMin <= bMin and aMax >= bMax or bMin <= aMin and bMax >= aMax:
        countI += 1
    if aMin <= bMax and aMax >= bMin:
        countII += 1

print("Part I", countI)
print("Part II", countII)
