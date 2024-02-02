import numpy as np
import random


def is_duplicate(base, arrs):
    arr = random.choice(arrs)
    if base[0] < arr[0] + 10 or base[0] > arr[0] - 10:
        if base[1] < arr[1] + 10 or base[1] > arr[1] - 10:
            return True
    return False


def remove_duplicate(arr):
    if len(arr) == 0:
        return arr
    result = []
    for i in arr[0]:
        if len(result) == 0:
            result.append([i[0]])
            continue
        for j in result:
            if is_duplicate(i[0], j):
                result[result.index(j)].append(i[0])
        else:
            result.append([i[0]])
    return list(map(lambda x: np.mean(x, axis=0), result))
