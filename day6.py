test_input = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""

with open("day6.input") as file:
    input = file.read()

#input = test_input
recent = [*input[:3]]

for i in range(0, len(input)):
    if i >= 4 and len(set(input[i-4:i])) == 4:
        print("Part I", i)
        break

for i in range(0, len(input)):
    if i >= 14 and len(set(input[i-14:i])) == 14:
        print("Part II", i)
        break
