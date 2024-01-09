def parse(snafu):
    value = 0
    for c in snafu:
        value = value * 5 + "=-012".find(c) - 2
    return value


def display(value):
    if value < 5:
        return "=-012"[value + 2]

    v = value % 5

    if v > 2:
        return display(value // 5 + 1) + display(v - 5)
    else:
        return ("" if value < 5 else display(value // 5)) +  display(v)


def part_i(data):
    total = sum(map(parse, data.splitlines()))
    print(display(total))


test_input = """
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""[1:]

part_i(test_input)

with open("day25.input") as file:
    file_input = file.read()

part_i(file_input)
