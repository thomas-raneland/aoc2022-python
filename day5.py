test_input = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

stacks, instructions = test_input.split("\n\n")

with open("day5.input") as file:
    stacks, instructions = file.read().split("\n\n")

stack_dict = {}

for line in stacks.splitlines()[:-1]:
    crates = line[1::4]

    for (c, v) in enumerate(crates):
        if v != " ":
            if c not in stack_dict:
                stack_dict[c] = []
            stack_dict[c].insert(0, v)

for instr in instructions.splitlines():
    move, n, fro, s, to, d = instr.split(" ")

    for i in range(0, int(n)):
        v = stack_dict.get(int(s) - 1).pop()
        if int(d) - 1 not in stack_dict:
            stack_dict[int(d) - 1] = []
        stack_dict.get(int(d) - 1).append(v)

answerI = "".join(map(lambda x: stack_dict.get(x).pop(), sorted(stack_dict.keys())))
print("Part I", answerI)

stack_dict = {}

for line in stacks.splitlines()[:-1]:
    crates = line[1::4]

    for (c, v) in enumerate(crates):
        if v != " ":
            if c not in stack_dict:
                stack_dict[c] = []
            stack_dict[c].insert(0, v)

for instr in instructions.splitlines():
    move, n, fro, s, to, d = instr.split(" ")

    if int(d) - 1 not in stack_dict:
        stack_dict[int(d) - 1] = []

    vs = stack_dict.get(int(s) - 1)[-int(n):]

    for v in vs:
        stack_dict.get(int(s) - 1).pop()
        stack_dict.get(int(d) - 1).append(v)

answerII = "".join(map(lambda x: stack_dict.get(x).pop(), sorted(stack_dict.keys())))
print("Part II", answerII)
