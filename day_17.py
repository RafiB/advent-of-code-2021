TEST_INPUT = "target area: x=20..30, y=-10..-5"

def get_x_velocity_candidates(x_range):
    candidates = []
    for starting_x in range(x_range[1]+1, 0, -1):
        c = starting_x
        c_v = starting_x - 1
        while c_v >= 0 and c <= x_range[1] + 2:
            if x_range[0] <= c and c <= x_range[1]:
                candidates.append(starting_x)
                break
            c += c_v
            c_v -= 1
    return candidates


def lands(x_v, y_v, x_range, y_range):
    y = 0
    x = 0

    ox_v = x_v
    oy_v = y_v

    while True:

        if x > max(x_range) or y < min(y_range):
            # print(f"({ox_v}, {oy_v}) fell out at ({x}, {y})")
            return False

        y += y_v
        x += x_v
        if x_v > 0:
            x_v -= 1
        y_v -= 1

        if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
            # print(f"({ox_v}, {oy_v}) lands at ({x}, {y})")
            return True


def solve(target_area):
    ranges = target_area[len("target area: x="):]
    x_range_str, y_range_str = ranges.split(", y=")
    x_range = tuple(map(int, x_range_str.split("..")))
    y_range = tuple(map(int, y_range_str.split("..")))

    x_velocity_candidates = get_x_velocity_candidates(x_range)

    count = 0
    for y_candidate in range(y_range[0]-2, abs(y_range[0]) + 1):
        for x_candidate in x_velocity_candidates:
            if lands(x_candidate, y_candidate, x_range, y_range):
                count += 1
    return count


if __name__ == "__main__":
    assert solve(TEST_INPUT) == 112, solve(TEST_INPUT)
    print(solve("target area: x=288..330, y=-96..-50"))
