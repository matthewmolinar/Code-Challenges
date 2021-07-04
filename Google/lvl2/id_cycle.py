def length_helper(num_str, length):
    if len(num_str) != length:
        padding = '0' * (length - len(num_str))
        num_str = padding + num_str
    return num_str
    
    
def base_cal(str1, str2, base):
    num1 = int(str1, base)
    num2 = int(str2, base)
    z = num1 - num2
    string = ''
    if z == 0:
        return str(0)
    while z > 0:
        z, rem = divmod(z, base)
        string += str(rem)
    return string
    
    
def solution(n, b):
    n_string = str(n)
    k = len(n_string)
    memo = {}
    i_count = 0
    while True:
        y = [int(ch) for ch in n_string]
        y.sort()
        x = y[::-1]
        x_str = ''.join(map(str, x))
        y_str = ''.join(map(str, y))
        # padding the number and subtracting.
        z = length_helper(base_cal(x_str, y_str, b), k)
        n_string = z
        if n_string in memo:
            return (i_count - memo[n_string])
        else:
            memo[n_string] = i_count
            i_count += 1


def test_cases():
    assert solution('1211', 10) == 1
    assert solution('210022', 3) == 3
    assert solution('000000000', 10) == 1
    assert solution('0000', 10) == 1
    assert solution('0', 10) == 1

test_cases()