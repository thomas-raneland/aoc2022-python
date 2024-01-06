import time
from functools import reduce
from typing import NamedTuple, Set


class TypeCount(NamedTuple):
    ore: int
    clay: int
    obs: int
    geo: int

    def minus(self, count):
        return TypeCount(self.ore - count.ore, self.clay - count.clay, self.obs - count.obs, self.geo - count.geo)

    def plus(self, count):
        return TypeCount(self.ore + count.ore, self.clay + count.clay, self.obs + count.obs, self.geo + count.geo)

    def times(self, count):
        return TypeCount(self.ore * count.ore, self.clay * count.clay, self.obs * count.obs, self.geo * count.geo)

    def has(self, count):
        return self.ore >= count.ore and self.clay >= count.clay and self.obs >= count.obs and self.geo >= count.geo

    def compare_to(self, that):
        c = self.geo - that.geo
        if c == 0:
            c = self.obs - that.obs
            if c == 0:
                c = self.clay - that.clay
                if c == 0:
                    c = self.ore - that.ore
        return c


empty = TypeCount(0, 0, 0, 0)
ore = TypeCount(1, 0, 0, 0)
clay = TypeCount(0, 1, 0, 0)
obs = TypeCount(0, 0, 1, 0)
geo = TypeCount(0, 0, 0, 1)


class Blueprint(NamedTuple):
    id: int
    ore_price: TypeCount
    clay_price: TypeCount
    obs_price: TypeCount
    geo_price: TypeCount

    def search(self, start, best=None):
        if best is None:
            best = start

        stack: [] = [start]
        seen: Set = set()

        limit = TypeCount(max(self.ore_price.ore, self.clay_price.ore, self.obs_price.ore, self.geo_price.ore),
                          max(self.ore_price.clay, self.clay_price.clay, self.obs_price.clay, self.geo_price.clay),
                          max(self.ore_price.obs, self.clay_price.obs, self.obs_price.obs, self.geo_price.obs), 100000)

        while not len(stack) == 0:
            state = stack.pop()

            if state.compare_to(best) > 0:
                best = state

            if state.time_left > 0 and state not in seen and state.potential().compare_to(best) > 0:
                seen.add(state)
                harvested = state.harvest()
                if state.time_left > 1 and state.money.has(self.geo_price):
                    stack.append(harvested.buy(self.geo_price, geo))
                stack.append(harvested)
                if state.time_left > 2:
                    if limit.obs > state.robots.obs and state.money.has(self.obs_price):
                        stack.append(harvested.buy(self.obs_price, obs))
                    else:
                        if limit.ore > state.robots.ore and state.money.has(self.ore_price):
                            stack.append(harvested.buy(self.ore_price, ore))
                    if state.time_left > 3 and limit.clay > state.robots.clay \
                            and state.money.has(self.clay_price):
                        stack.append(harvested.buy(self.clay_price, clay))

        return best


class State(NamedTuple):
    money: TypeCount
    robots: TypeCount
    time_left: int

    def potential(self):
        potential_geo = self.money.geo + self.time_left * self.robots.geo + self.time_left * (self.time_left - 1) // 2
        potential_money = TypeCount(self.money.ore, self.robots.clay, self.robots.obs, potential_geo)
        return State(potential_money, self.robots, 0)

    def compare_to(self, that):
        c = self.money.compare_to(that.money)
        if c == 0:
            c = self.robots.compare_to(that.robots)
            if c == 0:
                c = self.time_left - that.time_left
        return c

    def buy(self, cost, robots):
        return State(self.money.minus(cost), self.robots.plus(robots), self.time_left)

    def harvest(self):
        return State(self.money.plus(self.robots), self.robots, self.time_left - 1)


def analyze_i(bp):
    best_alt1 = bp.search(State(ore, ore.plus(ore), 23 - bp.ore_price.ore))
    best_alt2 = bp.search(State(ore, ore.plus(clay), 23 - bp.clay_price.ore), best_alt1)
    best = best_alt1 if best_alt1.money.geo > best_alt2.money.geo else best_alt2
    quality_level = bp.id * best.money.geo
    print(str(bp.id) + " " + str(quality_level) + " " + str(best))
    return quality_level


def analyze_ii(bp):
    best = bp.search(State(empty, ore, 32))
    print(str(bp.id) + " " + str(best))
    return best.money.geo


def part_i(data):
    blueprints = []

    for i, line in enumerate(data.splitlines()):
        tokens = line.split(" ")
        a, b, c, d, e, f = map(int, [token for token in tokens if token.isdigit()])
        blueprints.append(Blueprint(i + 1, TypeCount(a, 0, 0, 0), TypeCount(b, 0, 0, 0), TypeCount(c, d, 0, 0),
                                    TypeCount(e, 0, f, 0)))

    start = time.time()
    results = list(map(analyze_i, blueprints))
    end = time.time()
    print("Part I", sum(results), end - start)


def part_ii(data):
    blueprints = []

    for i, line in enumerate(data.splitlines()):
        tokens = line.split(" ")
        a, b, c, d, e, f = map(int, [token for token in tokens if token.isdigit()])
        blueprints.append(Blueprint(i + 1, TypeCount(a, 0, 0, 0), TypeCount(b, 0, 0, 0), TypeCount(c, d, 0, 0),
                                    TypeCount(e, 0, f, 0)))

    start = time.time()
    results = list(map(analyze_ii, blueprints[:3]))
    end = time.time()
    print("Part II", reduce(lambda x, y: x * y, results), end - start)


def day19():
    test_input = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
    Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""
    part_i(test_input)
    part_ii(test_input)
    with open("day19.input") as file:
        file_input = file.read()
    part_i(file_input)
    part_ii(file_input)


day19()
