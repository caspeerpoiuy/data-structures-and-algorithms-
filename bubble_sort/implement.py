def bubble_sort(alist):
    """
    bubble_sort thinking:
        Compare with nearby elements if elementA greater than elementB switch theirs position.
        As my comprehend, with the loop count increase, the elements need to check decrease.
    """
    for i in range(len(li)-1, 0, -1):
        for j in range(i):
            if alist[j] > alist[j + 1]:
                alist[j], alist[j + 1] = alist[j + 1], alist[j]


if __name__ == '__main__':
    li = [35, 66, 21, 77, 54, 22]
    bubble_sort(li)
    print(li)
