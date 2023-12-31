test_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

with open("day7.input") as file:
    input = file.read()

# input = test_input

cwd = []
sizes = {}

for line in input.splitlines():
    if line == "$ cd ..":
        cwd = cwd[:-1]
    elif line == "$ cd /":
        cwd = []
    elif line.startswith("$ cd"):
        cwd.append(line[5:])
    elif not line.startswith("$"):
        size, name = line.split(" ")
        if size != "dir":
            for i in range(0, len(cwd) + 1):
                folder = "/".join(cwd[:i])
                sizes[folder] = sizes.get(folder, 0) + int(size)

total = sum(size for size in sizes.values() if size <= 100000)
print("Part I", total)

needed = 30000000 - (70000000 - sizes[""])
print("Part II", next(size for size in sorted(sizes.values()) if size >= needed))
