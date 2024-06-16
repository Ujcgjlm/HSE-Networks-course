def binary_search(low, high, checker):
    high += 1
    while low + 1 < high:
        mid = (low + high) // 2
        if checker(mid):
            low = mid
        else:
            high = mid

    final = checker(low)

    return low if final else None
