import itertools
def sub_set(l, basket, lo, permute_list):
    hi = len(l)
    if (lo == hi):
        permutations = list(itertools.permutations(basket))
        # print(f'adding {permutations} to permute_list')
        for subset in permutations:
            permute_str = ''.join(map(str, subset))
            if permute_str != '':
                permute_list.append(int(permute_str))
        # permute_list.append(permutations)
        return
    else:
        copy = basket[:]
        basket.append(l[lo])
        sub_set(l, basket, lo + 1, permute_list)
        sub_set(l, copy, lo + 1, permute_list)

def solution(l):
    l.sort()
    l = l[::-1]
    permute_list = []
    basket = []
    sub_set(l, basket, 0, permute_list)
    print(permute_list)
    maximum = 0
    for num in permute_list:
        if (num % 3 == 0) and (num > maximum):
            maximum = num
    return maximum
    

print(solution([3,1,4,1,5,9]))
    