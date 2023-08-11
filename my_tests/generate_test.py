def generate_test(n, H, out_file):
    """
    Generate a test case for the Down with Trojans dynamic programming assignment

    Parameters:
        n (int): grid size
        H (int): initial hit points
        out_file (string): the name to use for the output file

    Output:
        out_file (file): output file to test the algorithm on

    """


    import random
    n = int(n)

    try:
        with open(out_file, "w") as file:
            file.write("{} {}\n".format(n, H))

            for i in range(n):
                for j in range(n):
                    if i == 0 and j == 0:
                        continue

                    type = random.randint(0,3)
                    if type == 0 or type == 1:
                        value = random.randrange(0, 20, 5)
                    else:
                        value = 0

                    file.write("{} {} {} {}\n".format(i, j, type, value))
    except IOError:
        print("Error: An I/O error occurred")


def main(n, H, out_file):
    generate_test(n, H, out_file)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python generate_test.py <integer_grid_size> <integer_hit_points> <a_file_name.txt>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
