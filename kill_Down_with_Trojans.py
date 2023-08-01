# Shared test cases with Cami Chou

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
    memo = [[None] * n] * n
    res = helper(n, H, tile_types, tile_values, memo, 0, 0, False, False)

    return res


def helper(n, H, tile_types, tile_values, memo, x, y, protection, multiplier):
    # Base cases
    print("HP: {}".format(H))
    if H < 0:                                 # Fail if HP negative
        return False
    elif x == n and y == n-1:                   # We passed last tile successfully!
        # print("Do I ever get here?")
        return True
    elif x == n-1 and y == n:                   # We passed last tile successfully!
        # print("Do I ever get here?")
        return True
    elif x >= n or y >= n:                    # Fail if out of bounds
        # print("I am out of bounds at HP: {}".format(H))
        return False
    elif memo[x][y] != None and memo[x][y] == True:                  # Memoize
        # print("Returning memo")
        return memo[x][y]
        # return memo[x][y] if we used multiplier at that location OR memo[x][y] if we did not use multiplier at that location

    # Update hitpoints for current tile
    tile_value = tile_values[x][y]
    tile_type = tile_types[x][y]

    if tile_type == 0:                                                      # DAMAGE
        if protection == False:
            # No protection, must lose HP
            # print("I have protection here: {}".format(protection))
            down = helper(n, H - tile_value, tile_types, tile_values, memo, x+1, y, protection, multiplier)
            right = helper(n, H - tile_value, tile_types, tile_values, memo, x, y+1, protection, multiplier)
            memo[x][y] = down or right
        else:
            # print("I got protection!")
            # print("I have protection: {}".format(protection))

            # Choose to use protection, don't lose HP
            prot_down = helper(n, H, tile_types, tile_values, memo, x+1, y, not protection, multiplier)
            prot_right = helper(n, H, tile_types, tile_values, memo, x, y+1, not protection, multiplier)

            # Choose NOT to use protection, lose HP
            down = helper(n, H - tile_value, tile_types, tile_values, memo, x+1, y, protection, multiplier)
            right = helper(n, H - tile_value, tile_types, tile_values, memo, x, y+1, protection, multiplier)

            # print("down: {}, right: {}, prot_down: {}, prot_right: {}".format(down, right, prot_down, prot_right))
            memo[x][y] = down or right or prot_down or prot_right
    elif tile_type == 1:                                                    # HEALING
        if multiplier == False:
            # No multiplier, gain original HP
            down = helper(n, H + tile_value, tile_types, tile_values, memo, x+1, y, protection, multiplier)
            right = helper(n, H + tile_value, tile_types, tile_values, memo, x, y+1, protection, multiplier)
            memo[x][y] = down or right
        else:
            # print("I got a multiplier!")
            # Choose to use multiplier, gain 2xHP
            mult_down = helper(n, H + (2*tile_value), tile_types, tile_values, memo, x+1, y, protection, not multiplier)
            mult_right = helper(n, H + (2*tile_value), tile_types, tile_values, memo, x, y+1, protection, not multiplier)

            # Choose NOT to use multiplier, gain original HP
            down = helper(n, H + tile_value, tile_types, tile_values, memo, x+1, y, protection, multiplier)
            right = helper(n, H + tile_value, tile_types, tile_values, memo, x, y+1, protection, multiplier)

            # print("down: {}, right: {}, mult_down: {}, mult_right: {}".format(down, right, mult_down, mult_right))
            memo[x][y] = down or right or mult_down or mult_right
            # print("After multiplier tile, I'm getting: {}".format(memo[x][y]))
    else:
        if tile_type == 2:                                                  # PROTECTION
            protection = True
        elif tile_type == 3:                                                # MULTIPLIER
            multiplier = True

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
