from collections import defaultdict

TEST_INPUT_SMALL = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

TEST_INPUT_MEDIUM = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

TEST_INPUT_LARGE = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

PUZZLE_INPUT = """cz-end
cz-WR
TD-end
TD-cz
start-UM
end-pz
kb-UM
mj-UM
cz-kb
WR-start
WR-pz
kb-WR
TD-kb
mj-kb
TD-pz
UM-pz
kb-start
pz-mj
WX-cz
sp-WR
mj-WR"""


def can_revisit(cave, path):
    if cave == 'start':
        return False

    if cave == cave.upper():
        return True

    already_visited = set()
    small_cave_revisited = False
    this_cave_visited = False
    for c in path:
        if c != c.lower():
            continue

        if c in already_visited:
            small_cave_revisited = True
            if this_cave_visited:
                return False

        if c == cave:
            this_cave_visited = True
            if small_cave_revisited:
                return False

        already_visited.add(c)

    return True


def count_paths(cave_map):
    paths = set()

    stack = [('start',)]

    while stack:
        curr_path = stack.pop()

        last = curr_path[-1]

        if last == 'end':
            paths.add(curr_path)
            continue

        for neighbour in cave_map[last]:
            if neighbour == 'end' or can_revisit(neighbour, curr_path):
                stack.append(curr_path + (neighbour,))

    return len(paths)


def solve(edges_str):
    cave_map = defaultdict(list)
    for edge in edges_str.split("\n"):
        start, end = edge.split("-")
        cave_map[start].append(end)
        cave_map[end].append(start)

    return count_paths(cave_map)


if __name__ == "__main__":
    assert solve(TEST_INPUT_SMALL) == 36
    assert solve(TEST_INPUT_MEDIUM) == 103
    assert solve(TEST_INPUT_LARGE) == 3509
    print(solve(PUZZLE_INPUT))
