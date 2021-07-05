def print_menu():
    print("""1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit""")


def input_matrices():
    row_len1, col_len1 = [int(i) for i in input("Enter size of first matrix: ").split()]
    if col_len1 is None:
        raise Exception("The operation cannot be performed.")
    print("Enter first matrix:")
    matrix1 = [[float(i) for i in input().split()] for _ in range(row_len1)]

    row_len2, col_len2 = [int(i) for i in input("Enter size of second matrix: ").split()]
    if col_len1 is None:
        raise Exception("The operation cannot be performed.")
    print("Enter second matrix:")
    matrix2 = [[float(i) for i in input().split()] for _ in range(row_len2)]

    return matrix1, matrix2


def print_matrix(matrix):
    print("The result is:")
    for row in matrix:
        print(*row)
    print()


def add_matrices(matrix1, matrix2):
    if len(matrix1) != len(matrix2) and len(matrix1[0]) != len(matrix2[0]):
        raise Exception("The operation cannot be performed.")

    rows, cols = range(len(matrix1)), range(len(matrix2[0]))
    sum_matrix = [[matrix1[row][col] + matrix2[row][col] for col in cols] for row in rows]
    return sum_matrix


def input_matrix_scalar():
    row_len, col_len = [int(i) for i in input("Enter size of matrix: ").split()]
    print("Enter matrix:")
    matrix = [[float(i) for i in input().split()] for _ in range(row_len)]
    constant = float(input("Enter constant: "))
    return matrix, constant


def multiply_matrix(matrix, scalar):
    rows, cols = range(len(matrix)), range(len(matrix[0]))
    scaled_matrix = [[matrix[row][col] * scalar for col in cols] for row in rows]
    return scaled_matrix


def multiply_matrices(matrix1, matrix2):
    if len(matrix1[0]) != len(matrix2):
        raise Exception("The operation cannot be performed.")

    rows, cols = range(len(matrix1)), range(len(matrix2[0]))
    product_matrix = [[0 for _ in cols] for _ in rows]

    for row in rows:
        for col in cols:
            product_matrix[row][col] = sum(float(matrix1[row][i] * matrix2[i][col]) for i in range(len(matrix2)))

    return product_matrix


def print_menu_transpose():
    print("""1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line""")


def input_matrix():
    row_len, col_len = [int(i) for i in input("Enter size of matrix: ").split()]
    print("Enter matrix:")
    matrix = [[float(i) for i in input().split()] for _ in range(row_len)]
    return matrix


def transpose_wrapper(matrix, option: int = 1):
    options: dict = {1: "MAIN", 2: "SIDE", 3: "VERTICAL", 4: "HORIZONTAL"}
    if options[option] == "MAIN":
        return [list(ele) for ele in list(zip(*matrix))]
    elif options[option] == "SIDE":
        return [list(ele)[::-1] for ele in list(zip(*matrix))][::-1]
    elif options[option] == "VERTICAL":
        return [lst[::-1] for lst in matrix]
    elif options[option] == "HORIZONTAL":
        return matrix[::-1]
    else:
        raise Exception("Invalid input")


def minor(matrix, pivot_row_idx, pivot_col_idx):
    deepcopy_matrix = [row[:] for row in matrix]

    del deepcopy_matrix[pivot_row_idx]
    for row in deepcopy_matrix:
        del row[pivot_col_idx]

    return deepcopy_matrix


def co_factor_scalar(matrix, pivot_row_idx, pivot_col_idx):
    unary_operator = 1 if pivot_row_idx + pivot_col_idx % 2 == 0 else -1
    pivot_cell = matrix[pivot_row_idx][pivot_col_idx]
    return pivot_cell * unary_operator


def determinant(matrix):
    if len(matrix) == 2:
        main_diagonal = matrix[0][0] * matrix[1][1]
        counter_diagonal = matrix[0][1] * matrix[1][0]
        return main_diagonal - counter_diagonal
    if len(matrix) == 1:
        return matrix[0][0]

    minors = [minor(matrix, 0, col) for col in range(len(matrix[0]))]
    co_factors_scalar = [co_factor_scalar(matrix, 0, col) for col in range(len(matrix[0]))]
    return sum(determinant(minors[i]) * co_factors_scalar[i] for i in range(len(matrix[0])))


def print_determinant(matrix):
    print("The result is:")
    print(matrix)


def minor_matrix(matrix):
    rows, cols = range(len(matrix)), range(len(matrix[0]))
    return [[determinant(minor(matrix, row, col)) for col in cols] for row in rows]


def co_factor_matrix(matrix):
    matrix_minor = minor_matrix(matrix)

    co_factors_matrix = [row[:] for row in matrix_minor]
    for row_idx, row in enumerate(co_factors_matrix):
        for col_idx, col in enumerate(co_factors_matrix):
            if (row_idx + col_idx) % 2 == 1:
                co_factors_matrix[row_idx][col_idx] *= -1

    return co_factors_matrix


def invert_matrix(matrix):
    det = determinant(matrix)

    if det == 0:
        raise Exception("Determinant zero. Matrix is not invertible")

    co_factor_ad_joint = transpose_wrapper(co_factor_matrix(matrix))
    det_inv = 1 / det

    return multiply_matrix(co_factor_ad_joint, det_inv)


while True:
    print_menu()
    choice = int(input("Your choice:"))

    if choice == 0:
        break
    if choice == 1:
        addend1, addend2 = input_matrices()
        print_matrix(add_matrices(addend1, addend2))
    elif choice == 2:
        matrix_to_scale, scale_factor = input_matrix_scalar()
        print_matrix(multiply_matrix(matrix_to_scale, scale_factor))
    elif choice == 3:
        multiplicand, multiplier = input_matrices()
        print_matrix(multiply_matrices(multiplicand, multiplier))
    elif choice == 4:
        print_menu_transpose()
        transpose_choice = int(input("Your choice: "))
        matrix_to_transpose = input_matrix()
        print_matrix(transpose_wrapper(matrix_to_transpose, transpose_choice))
    elif choice == 5:
        matrix_det = input_matrix()
        print_determinant(determinant(matrix_det))
    elif choice == 6:
        matrix_inv = input_matrix()
        print_matrix(invert_matrix(matrix_inv))

    else:
        raise Exception("Invalid input")
