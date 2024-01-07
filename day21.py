class Expr:
    def eval(self):
        return 0


class BinExpr(Expr):
    lhs: Expr
    rhs: Expr
    op: str

    def __init__(self, lhs, rhs, op):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def eval(self):
        match self.op:
            case "+":
                return self.lhs.eval() + self.rhs.eval()
            case "-":
                return self.lhs.eval() - self.rhs.eval()
            case "*":
                return self.lhs.eval() * self.rhs.eval()
            case "/":
                return self.lhs.eval() / self.rhs.eval()


class LiteralExpr(Expr):
    value: int

    def __init__(self, v):
        self.value = v

    def eval(self):
        return self.value


def parse(env, n):
    e = env[n].split(" ")

    if len(e) == 1:
        expr = LiteralExpr(int(e[0]))
        return expr, expr if n == "humn" else None

    op = e[1]
    lhs, humn1 = parse(env, e[0])
    rhs, humn2 = parse(env, e[2])
    return BinExpr(lhs, rhs, op), humn1 if humn1 is not None else humn2


def part_i(data):
    env = {}

    for line in data.splitlines():
        n, e = line.split(": ")
        env[n] = e

    root, _ = parse(env, "root")
    print("Part I", int(root.eval()))


def test(root, you, you_value):
    you.value = you_value
    return root.lhs.eval() - root.rhs.eval()


def part_ii(data):
    env = {}

    for line in data.splitlines():
        n, e = line.split(": ")
        env[n] = e

    root, you = parse(env, "root")

    lo_you = 0
    hi_you = 2
    lo_root = test(root, you, lo_you)

    while hi_you - lo_you > 1:
        hi_you = lo_you + 1
        hi_root = test(root, you, hi_you)

        while lo_root * hi_root > 0:
            hi_you += (hi_you - lo_you)
            hi_root = test(root, you, hi_you)

        lo_you = hi_you - 1
        lo_root = test(root, you, lo_you)

        while lo_root * hi_root > 0:
            lo_you -= (hi_you - lo_you)
            lo_root = test(root, you, lo_you)

    print("Part II", lo_you if lo_root == 0 else hi_you)


test_input = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

part_i(test_input)
part_ii(test_input)

with open("day21.input") as file:
    file_input = file.read()

part_i(file_input)
part_ii(file_input)
