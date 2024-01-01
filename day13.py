import functools
import re

test_input = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def parse(s):
    if not s.startswith("["):
        match = re.search("[,\\]]", s)
        if match is None:
            comma = len(s)
        else:
            comma = match.span()[0]
        return [int(s[:comma])], comma
    else:
        list = []
        pos = 1
        while pos < len(s) and not (s[pos] == "," or s[pos] == "]"):
            v, next_pos = parse(s[pos:])
            pos += next_pos + 1
            list.append(v)
        return list, pos + 1


def compare(a, b):
    if isinstance(a, list) and isinstance(b, list):
        for i in range(0, min(len(a), len(b))):
            c = compare(a[i], b[i])
            if c != 0:
                return c

        return len(a) - len(b)
    elif isinstance(a, list):
        return compare(a, [b])
    elif isinstance(b, list):
        return compare([a], b)
    else:
        return a - b


with open("day13.input") as file:
    pairs = file.read().split("\n\n")

# pairs = test_input.split("\n\n")
packets = [2, 6]
total = 0

for (index, pair) in enumerate(pairs):
    a, b = pair.splitlines()
    a_list, _ = parse(a)
    b_list, _ = parse(b)
    total += index + 1 if compare(a_list, b_list) <= 0 else 0
    packets.extend([a_list, b_list])

print("Part I", total)

packets.sort(key=functools.cmp_to_key(compare))
ix1 = packets.index(2) + 1
ix2 = packets.index(6) + 1
print("Part II", ix1 * ix2)
