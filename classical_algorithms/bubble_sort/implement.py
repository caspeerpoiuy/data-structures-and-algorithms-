def bubble_sort(alist):
    """
    bubble_sort thinking:
        Compare with nearby elements if elementA greater than elementB switch theirs position.
        As my comprehend, with the loop count increase, the elements need to check decrease.
    """
    if len(alist) == 0:
        return
    for i in range(1, len(alist)):
        for j in range(len(alist)-i):
            if alist[j] > alist[j + 1]:
                alist[j], alist[j + 1] = alist[j + 1], alist[j]


if __name__ == '__main__':
    li = [35, 66, 21, 77, 54, 22]
    bubble_sort(li)
    print(li)
