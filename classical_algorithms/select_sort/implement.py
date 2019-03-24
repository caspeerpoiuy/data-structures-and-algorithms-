def select_sort(alist):
    """
    select sort thinking:
        compare element and find the min index, if element less than min, change their position.
    """
    for i in range(1, len(alist)):
        min_index = i - 1
        for j in range(i, len(alist)):
            if alist[j] < alist[min_index]:
                min_index = j
        alist[i - 1], alist[min_index] = alist[min_index], alist[i - 1]


if __name__ == '__main__':
    li = [35, 66, 21, 77, 54, 22]
    select_sort(li)
    print(li)