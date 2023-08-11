# Shared test cases with Cami Chou

import numpy as np
# import scipy


def load_input_file(file_name):
    with open(file_name, 'r') as file:
        n, H = map(int, file.readline().split())
        tile_types = np.zeros((n, n), dtype=int)
        tile_values = np.zeros((n, n), dtype=int)

        for i in range(n * n):
            if i == 0:
                continue  # the initial tile is zero type with zero value
            x, y, t, v = map(int, file.readline().split())
            tile_types[x][y] = t
            tile_values[x][y] = v

    return n, H, tile_types, tile_values


def print_tile_data(tile_types, tile_values):
    print("Tile Types:")
    print(tile_types)
    print("\nTile Values:")
    print(tile_values)


def DP(n, H, tile_types, tile_values):
    memo = np.ones((n, n, 2, 2), dtype=float) * -np.inf
    min_HP = helper(n, H, tile_types, tile_values, memo, 0, 0, 0, 0)

    if min_HP <= H:
        return True
    else:
        return False


def helper(n, H, tile_types, tile_values, memo, x, y, p, m):
    # Base cases
    if x == n-1 and y == n-1:
        # Reached the last tile
        if tile_types[x][y] == 0 and p == 0:
            # Damage tile, no protection
            value = tile_values[x][y]
            memo[x, y, p, m] = value
            return memo[x, y, p, m]
        else:
            memo[x, y, p, m] = 0
            return memo[x, y, p, m]
    elif x >= n or y >= n:
        # Out of bounds
        return np.inf
    elif memo[x, y, p, m] != -np.inf:
        # Spot visited before, return memo
        return memo[x, y, p, m]

    # Get tile value and type for current tile
    tile_value = tile_values[x][y]
    tile_type = tile_types[x][y]

    if tile_type == 0:
        # Danger tile
        if p == 1:
            # Currently have a protection token
            # Use it
            usep_right = helper(n, H, tile_types, tile_values, memo, x, y+1, 0, m)
            usep_down = helper(n, H, tile_types, tile_values, memo, x+1, y, 0, m)

            # Don't use it
            right = helper(n, H, tile_types, tile_values, memo, x, y+1, p, m) + tile_value
            down = helper(n, H, tile_types, tile_values, memo, x+1, y, p, m) + tile_value

            memo[x, y, p, m] = min(usep_right, usep_down, right, down)
            return memo[x, y, p, m]
        else:
            # Don't have a protection token
            right = helper(n, H, tile_types, tile_values, memo, x, y+1, p, m) + tile_value
            down = helper(n, H, tile_types, tile_values, memo, x+1, y, p, m) + tile_value

            memo[x, y, p, m] = min(right, down)
            return memo[x, y, p, m]
    elif tile_type == 1:
        # Healing tile
        if m == 1:
            # Currently have a multiplier token
            # Use it
            usem_right = helper(n, H, tile_types, tile_values, memo, x, y+1, p, 0) - (2*tile_value)
            usem_down = helper(n, H, tile_types, tile_values, memo, x+1, y, p, 0) - (2*tile_value)

            # Don't use it
            right = helper(n, H, tile_types, tile_values, memo, x, y+1, p, m) - tile_value
            down = helper(n, H, tile_types, tile_values, memo, x+1, y, p, m) - tile_value

            # Don't store a negative value, leads to trouble
            if min(usem_right, usem_down, right, down) < 0:
                memo[x, y, p, m] = 0
            else:
                memo[x, y, p, m] = min(usem_right, usem_down, right, down)
            return memo[x, y, p, m]
        else:
            # Don't have a multiplier token
            right = helper(n, H, tile_types, tile_values, memo, x, y+1, p, m) - tile_value
            down = helper(n, H, tile_types, tile_values, memo, x+1, y, p, m) - tile_value

            if min(right, down) < 0:
                memo[x, y, p, m] = 0
            else:
                memo[x, y, p, m] = min(right, down)
            return memo[x, y, p, m]
    elif tile_type == 2:
        # Protection tile
        right = helper(n, H, tile_types, tile_values, memo, x, y+1, 1, m) # 0
        down = helper(n, H, tile_types, tile_values, memo, x+1, y, 1, m) # inf

        memo[x, y, p, m] = min(right, down)
        return memo[x, y, p, m]

    elif tile_type == 3:
        # Multiplier tile
        right = helper(n, H, tile_types, tile_values, memo, x, y+1, p, 1)
        down = helper(n, H, tile_types, tile_values, memo, x+1, y, p, 1)

        memo[x, y, p, m] = min(right, down)
        return memo[x, y, p, m]


def write_output_file(output_file_name, result):
    with open(output_file_name, 'w') as file:
        file.write(str(int(result)))


def main(input_file_name):
    n, H, tile_types, tile_values = load_input_file(input_file_name)
    print_tile_data(tile_types, tile_values)
    result = DP(n, H, tile_types, tile_values)
    print("Result: " + str(result))
    output_file_name = input_file_name.replace(".txt", "_out.txt")
    write_output_file(output_file_name, result)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python kill_Down_with_Trojans.py a_file_name.txt")
    else:
        main(sys.argv[1])
