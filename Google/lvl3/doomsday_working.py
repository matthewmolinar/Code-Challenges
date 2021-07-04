from fractions import Fraction
from fractions import gcd

def create_i_matrix(m):
    id_matrix = [[Fraction(1) if i == j else Fraction(0) for i in range(len(m))] for j in range(len(m))]
    return id_matrix


def matrix_add_subtract(mat_1, mat_2, operation):
    new_matrix = []
    if operation == 'add':
        for i in range(len(mat_1)):
            row = []
            for j in range(len(mat_1)):
                row.append(mat_1[i][j] + mat_2[i][j])
            new_matrix.append(row)
    elif operation == 'sub':
        for i in range(len(mat_1)):
            row = []
            for j in range(len(mat_1)):
                row.append(mat_1[i][j] - mat_2[i][j])
            new_matrix.append(row)
    return new_matrix


def matrix_multiply(mat_1, mat_2):
    new_matrix = []
    for i in range(len(mat_1)):
        row = []
        for j in range(len(mat_2[i])):
            num = Fraction(0)
            for k in range(len(mat_1)):
                num += mat_1[i][k] * mat_2[k][j]
            row.append(Fraction(num))
        new_matrix.append(row)
    return new_matrix


def matrix_inverse(a):
    # Make an id matrix
    identity_mat = create_i_matrix(a)
    # Perform operations on both matrices.
    for i in range(len(a)):
        for j in range(len(a[i])):
            # Found a diagonal
            if i == j:
                diagonal_element = a[i][j]
                diagonal_inverse = Fraction(1, diagonal_element)
                diag_row = i
                diag_col = j
                # Scale row i by the inverse
                for col in range(len(a[diag_row])):
                    a[diag_row][col] *= diagonal_inverse
                    identity_mat[diag_row][col] *= diagonal_inverse
                # Subtractions to get 0
                for row in range(len(a[diag_row])):
                    if row != diag_row:
                        multiplier = Fraction(a[row][diag_col])
                        for col in range(len(a[diag_row])):
                            a[row][col] -= multiplier * (a[diag_row][col])
                            identity_mat[row][col] -= multiplier * (identity_mat[diag_row][col])
    return identity_mat


def lcm_denominators(denominators):
    lcm = lambda num1, num2: abs(num1*num2) // gcd(num1,num2)
    current_lcm = lcm(denominators[0], denominators[1])
    for i in range(2, len(denominators)):
        current_lcm = lcm(current_lcm, denominators[i])
    return current_lcm
            

def solution(m):
    m = [[Fraction(m[i][j]) for j in range(len(m[i]))] for i in range(len(m))]
    absorbing_states = []
    non_absorbing_states = []
    # 1) Create standard form
    # identify absorbing states
    for i in range(len(m)):
        absorbing = True
        for j in range(len(m[i])):
            if m[i][j] > 1 or (m[i][j] == 1 and i != j):
                absorbing = False
                total = Fraction(sum(m[i]))
                for num in range(len(m[i])):
                    m[i][num] /= total
                break
        if absorbing:
            # convert classified absorbing states into 100% probability of staying same.
            m[i][i] = Fraction(1)
            absorbing_states.append(i)
        else:
            non_absorbing_states.append(i)
    # sort the states
    absorbing_states.sort()
    if 0 in absorbing_states:
        result = [0 if absorbing_states[i] > 0 else 1 for i in range(len(absorbing_states))]
        result.append(1)
        return result
    non_absorbing_states.sort()
    standard_order = absorbing_states + non_absorbing_states
    # create the standard form transition probability matrix.
    standard_form_transition_prob = [[m[num_1][num_2] for num_2 in standard_order] for num_1 in standard_order]
    # 2) Calculate F
    matrix_Q = [[(standard_form_transition_prob[i][j]) for j in range(len(absorbing_states), len(standard_order))] for i in range(len(absorbing_states), len(standard_form_transition_prob))]
    matrix_R = [[(standard_form_transition_prob[i][j]) for j in range(len(absorbing_states))] for i in range(len(absorbing_states), len(standard_form_transition_prob))]
    identity_Q = create_i_matrix(matrix_Q)
    i_q_term = matrix_add_subtract(identity_Q, matrix_Q, 'sub')
    matrix_F = matrix_inverse(i_q_term)
    # 3) Calculate FR
    matrix_FR = matrix_multiply(matrix_F, matrix_R)
    probabilities = [Fraction(val).limit_denominator() for val in matrix_FR[0]]
    denominators = [fraction.denominator for fraction in probabilities]
    lcm = lcm_denominators(denominators)
    result = []
    for fraction in probabilities:
        num = (fraction.numerator) * (lcm / fraction.denominator)
        result.append(num)
    result.append(lcm)
    return result


mat_1 = [
        [0, 2, 1, 0, 0],
        [0, 0, 0, 3, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

mat_2 = [
        [0, 1, 0, 0, 0, 1],
        [4, 0, 0, 3, 2, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]

mat_3 = [
        [1, 2, 3, 0, 0, 0],
        [4, 5, 6, 0, 0, 0],
        [7, 8, 9, 1, 0, 0],
        [0, 0, 0, 0, 1, 2],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]

mat_4 = [[0]]

mat_5 = [
        [0, 0, 12, 0, 15, 0, 0, 0, 1, 8],
        [0, 0, 60, 0, 0, 7, 13, 0, 0, 0],
        [0, 15, 0, 8, 7, 0, 0, 1, 9, 0],
        [23, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [37, 35, 0, 0, 0, 0, 3, 21, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

mat_6 = [
        [0, 7, 0, 17, 0, 1, 0, 5, 0, 2],
        [0, 0, 29, 0, 28, 0, 3, 0, 16, 0],
        [0, 3, 0, 0, 0, 1, 0, 0, 0, 0],
        [48, 0, 3, 0, 0, 0, 17, 0, 0, 0],
        [0, 6, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

mat_7 = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

mat_8 = [
        [1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

mat_9 = [
        [0, 86, 61, 189, 0, 18, 12, 33, 66, 39],
        [0, 0, 2, 0, 0, 1, 0, 0, 0, 0],
        [15, 187, 0, 0, 18, 23, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

mat_10 = [
        [0, 0, 0, 0, 3, 5, 0, 0, 0, 2],
        [0, 0, 4, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 4, 4, 0, 0, 0, 1, 1],
        [13, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [0, 1, 8, 7, 0, 0, 0, 1, 3, 0],
        [1, 7, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
print(solution(mat_1))
print(solution(mat_2))
print(solution(mat_3))
print(solution(mat_4))
print(solution(mat_5))
print(solution(mat_6))
print(solution(mat_7))
print(solution(mat_8))
print(solution(mat_9))
print(solution(mat_10))

def test_cases():
    assert solution(mat_1) == [7,6,8,21]
    assert solution(mat_2) == [0,3,2,9,14]
    assert solution(mat_3) == [1,2,3]
    assert solution(mat_4) == [1,1]
    assert solution(mat_5) == [1, 2, 3, 4, 5, 15]
    assert solution(mat_6) == [4, 5, 5, 4, 2, 20]
    assert solution(mat_7) == [1, 1, 1, 1, 1, 5]
    assert solution(mat_8) == [2, 1, 1, 1, 1, 6]
    assert solution(mat_9) == [6, 44, 4, 11, 22, 13, 100]
    assert solution(mat_10) == [1, 1, 1, 2, 5]

test_cases()