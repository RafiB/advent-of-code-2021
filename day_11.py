TEST_INPUT = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

PUZZLE_INPUT = """5433566276
6376253438
8458636316
6253254525
7211137138
1411526532
5788761424
8677841514
1622331631
5876712227"""

FLASHED = -1


def step(octopuses):
    return [[i + 1 for i in row] for row in octopuses]


DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]


def flash(state):
    n_flashes = 0
    go_again = True
    while go_again:
        go_again = False
        for y, row in enumerate(state):
            for x, c in enumerate(row):
                if c > 9:
                    row[x] = FLASHED
                    n_flashes += 1
                    for dx, dy in DIRS:
                        if y + dy < 0 or x + dx < 0 or y + dy >= len(state) or x + dx >= len(state[0]):
                            continue
                        if state[y + dy][x + dx] != FLASHED:
                            state[y + dy][x + dx] += 1
                            if state[y + dy][x + dx] > 9:
                                go_again = True

    return n_flashes, state

def solve(octopuses_str):
    state = [[int(c) for c in row] for row in octopuses_str.split("\n")]


    steps = 0
    while True:
        state = step(state)
        n_flashes, state = flash(state)
        state = [[0 if i == FLASHED else i for i in row] for row in state]
        steps += 1
        if n_flashes == len(state) * len(state[0]):
            break

    return steps

if __name__ == "__main__":
    assert solve(TEST_INPUT) == 195
    print(solve(PUZZLE_INPUT))
