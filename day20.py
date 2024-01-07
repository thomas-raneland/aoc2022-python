from typing import NamedTuple


class Number(NamedTuple):
    id: int
    value: int


def grove_coordinates(data, mix_times=1, decryption_key=1):
    numbers = list(map(lambda x: Number(x[0], x[1] * decryption_key), enumerate(map(int, data.splitlines()))))
    order = numbers.copy()

    for i in range(0, mix_times):
        for n in order:
            old_pos = numbers.index(n)
            numbers.pop(old_pos)
            new_pos = (((old_pos + n.value) % len(numbers)) + len(numbers)) % len(numbers)
            numbers.insert(new_pos, n)

    while not numbers[0].value == 0:
        numbers.append(numbers.pop(0))

    coordinates = [numbers[1000 % len(numbers)], numbers[2000 % len(numbers)], numbers[3000 % len(numbers)]]
    return sum(map(lambda number: number.value, coordinates))


def day20():
    test_input = """1
        2
        -3
        3
        -2
        0
        4"""

    print("Part I test", grove_coordinates(test_input))

    with open("day20.input") as file:
        file_input = file.read()

    print("Part I file", grove_coordinates(file_input))
    print("Part II test", grove_coordinates(test_input, 10, 811589153))
    print("Part II file", grove_coordinates(file_input, 10, 811589153))


day20()
