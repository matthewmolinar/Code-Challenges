# THIS SOLUTION GOT 4/5 TEST CASES
# The solution that got 5/5 was not saved on my machine.
# bomb baby
# if F == M: cannot solve
# if f and m == 1: return 0
# if f and m are both even: cannot solve
# if f and m are 1 apart: return smallest of two
def solvable(x,y):
    if x == 0 or y == 0:
        return False
    if x == y and (x != 1 and y != 1):
        return False
    if (x % 2 == 0) and (y % 2 == 0):
        return False
    if (x < 0) or (y < 0):
        return False
    return True
    

def helper(x, y, count):
    if not solvable(x,y):
        return x, y, count
    # base case.
    if x == 1 and y == 1:
        return x, y, count
    
    if (x - y == 1) or (y - x == 1):
        smaller = min(x, y)
        count += smaller
        return helper(1, 1, count)
    
    bigger = max(x, y)
    smaller = min(x, y)
    if count == 0:
        cycles = bigger // smaller
        count += cycles
        difference = bigger - (smaller * cycles)
    else:
        difference = bigger - smaller
        count += 1
    if bigger == x:
        x = difference
    else:
        y = difference
    return helper(x, y, count)


def test_cases():
    assert solution('2', '1') == '1'
    assert solution('4', '7') == '4'
    assert solution('31', '4') == '10'
    # assert solution('', '4') == '10'
    # assert solution('31', '4') == '10'
    
def solution(x, y):
    x = int(x)
    y = int(y)
    if x == 1 and y == 1:
        return 0
    if not solvable(x,y):
        return 'impossible'
    x, y, count = helper(x, y, 0)
    if x == 1 and y == 1:
        return str(count)
    else:
        return 'impossible'

# test_cases()

print(solution(10**50, 10**50))        
