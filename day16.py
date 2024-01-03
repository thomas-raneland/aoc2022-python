from timeit import timeit
from typing import NamedTuple
from itertools import chain, combinations

test_input = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


class Valve(NamedTuple):
    name: str
    flow_rate: int
    tunnels: list


with open("day16.input") as file:
    input = file.read()

# input = test_input

valves = {}

for line in input.splitlines():
    name = line[6:8]
    flow_rate = int(line[line.index("=") + 1:line.index(";")])
    tunnels = list(map(lambda v: (v, 1), line[line.index("to valve") + 9:].strip().split(", ")))
    valves[name] = Valve(name, flow_rate, tunnels)


def remove_zero_valves():
    zero_valves = [x for x in valves.keys() if valves[x].flow_rate == 0 and x != "AA"]

    for zv in zero_valves:
        for k in valves:
            v = valves[k]

            if k != zv:
                new_tunnels = []

                for (t, dist) in v.tunnels:
                    if t == zv:
                        for (nt, dist2) in valves[zv].tunnels:
                            if nt != k:
                                new_tunnels.append((nt, dist + dist2))
                    else:
                        new_tunnels.append((t, dist))

                valves[k] = Valve(v.name, v.flow_rate, new_tunnels)

        valves.pop(zv)


remove_zero_valves()


def score(valve, time_left):
    return valve.flow_rate * time_left


class State(NamedTuple):
    pos: str
    total: int
    is_open: frozenset
    time_left: int

    def potential(self):
        p = self.total

        for v in valves:
            if v not in self.is_open:
                p += score(valves[v], self.time_left - (1 if self.pos == v else 2))

        return p


class MiniState(NamedTuple):
    pos: str
    is_open: frozenset


def bfs(time_left, valves_to_open):
    queue = [State("AA", 0, frozenset([]), time_left)]
    seen = {}
    max_total = 0

    while len(queue) > 0:
        state = queue.pop(0)
        mini_state = MiniState(state.pos, state.is_open)

        if mini_state in seen and seen[mini_state] >= state.total:
            continue

        seen[mini_state] = state.total

        if state.potential() <= max_total:
            continue

        if state.total > max_total:
            max_total = state.total
            # print(max_total, state.time_left)

        if state.time_left > 1:
            if state.pos in valves_to_open and state.pos not in state.is_open:
                new_total = state.total + score(valves[state.pos], state.time_left - 1)
                queue.append(State(state.pos, new_total, state.is_open.union([state.pos]), state.time_left - 1))

            for (v, dist) in valves[state.pos].tunnels:
                if state.time_left > dist:
                    queue.append(State(v, state.total, state.is_open, state.time_left - dist))

    return max_total


print("Part I", bfs(30, set(valves.keys())))


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


max_combined = 0
subsets = list(powerset(valves.keys()))

for nbr, i in enumerate(subsets):
    print(nbr, len(subsets))
    combined = bfs(26, set(i)) + bfs(26, set(valves.keys()).difference(set(i)))

    if combined > max_combined:
        max_combined = combined
        print(max_combined)

print("Part II", max_combined)
