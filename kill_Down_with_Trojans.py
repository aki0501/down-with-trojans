import numpy as np
import scipy


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
    # TODO
    # Placeholder function - implement your logic here
    # Your code to check whether it is possible to reach the bottom-right
    # corner without running out of HP should go here.

    # You should use dynamic programming to solve the problem.
    # Return True if possible, False otherwise.

    # By defualt we return False

    memo = [[None] * n] * n
    res = helper(n, H, tile_types, tile_values, memo, 0, 0, False, False)

    return res


def helper(n, H, tile_types, tile_values, memo, x, y, protection, multiplier):
    # Check bounds
    if x >= n or y >= n:
        return False

    # Update hitpoints for current tile
    tile_value = tile_values[x][y]
    tile_type = tile_types[x][y]

    if tile_type == 0:               # DAMAGE
        if protection == False:
            H -= tile_value
        else:
            protection = False
    elif tile_type == 1:             # HEALING
        if multiplier == True:
            H += (2*tile_value)
            multiplier = False
        else:
            H += tile_value
    elif tile_type == 2:             # PROTECTION
        protection = True
    elif tile_type == 3:             # MULTIPLIER
        multiplier = True

    print("HP: {}".format(H))
    print("Protection: {}".format(protection))
    
    # Base cases
    if H < 0:                               # Fail if HP negative
        return False
    if x == n-1 and y == n-1:               # Success if reached end tiles
        return True
    if memo[x][y] != None:                  # Memoize
        return memo[x][y]

    # Recursive calls
    down = helper(n, H, tile_types, tile_values, memo, x+1, y, protection, multiplier)
    right = helper(n, H, tile_types, tile_values, memo, x, y+1, protection, multiplier)
    memo[x][y] = down or right

    return memo[x][y]


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
