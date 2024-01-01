import heapq

test_input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


class Node:
    def __init__(self):
        self.distance = float('inf')  # current distance from source node
        self.parent = None
        self.finished = False


def dijkstra(graph, source):
    nodes = {}
    for node in graph:
        nodes[node] = Node()
    nodes[source].distance = 0
    queue = [(0, source)]  # priority queue
    while queue:
        d, node = heapq.heappop(queue)
        if nodes[node].finished:
            continue
        nodes[node].finished = True
        for neighbor in graph[node]:
            if nodes[neighbor].finished:
                continue
            new_d = d + graph[node][neighbor]
            if new_d < nodes[neighbor].distance:
                nodes[neighbor].distance = new_d
                nodes[neighbor].parent = node
                heapq.heappush(queue, (new_d, neighbor))
    return nodes


with open("day12.input") as file:
    lines = file.read().splitlines()

# lines = test_input.splitlines()
start = None
end = None

for y in range(0, len(lines)):
    for x in range(0, len(lines[y])):
        if lines[y][x] == "S":
            start = (x, y)
            lines[y] = lines[y].replace("S", "a")
        if lines[y][x] == "E":
            end = (x, y)
            lines[y] = lines[y].replace("E", "z")

graph = {}

for y in range(0, len(lines)):
    for x in range(0, len(lines[y])):
        node = {}
        if y > 0 and ord(lines[y - 1][x]) < ord(lines[y][x]) + 2:
            node[(x, y - 1)] = 1
        if y < len(lines) - 1 and ord(lines[y + 1][x]) < ord(lines[y][x]) + 2:
            node[(x, y + 1)] = 1
        if x > 0 and ord(lines[y][x - 1]) < ord(lines[y][x]) + 2:
            node[(x - 1, y)] = 1
        if x < len(lines[y]) - 1 and ord(lines[y][x + 1]) < ord(lines[y][x]) + 2:
            node[(x + 1, y)] = 1
        graph[(x, y)] = node

nodes = dijkstra(graph, start)
print("Part I", nodes[end].distance)
min_distance = float('inf')

for y in range(0, len(lines)):
    for x in range(0, len(lines[y])):
        if lines[y][x] == "a":
            nodes = dijkstra(graph, (x, y))
            min_distance = min(min_distance, nodes[end].distance)

print("Part II", min_distance)
