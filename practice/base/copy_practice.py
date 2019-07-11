import copy
import sys


def shallow_copy():
    """
    浅拷贝：
        切片，工厂函数以及copy.copy都是浅拷贝操作，即开辟一片新的内存空间，存储变量。
    """
    a = [1,2,"hello",['python', 'C++']]
    b = a[:]
    # b = [x for x in a]
    # b = list(a)
    # b = copy.copy(a)

    # a[3].append('java')
    print(b)
    # 如果对a的嵌套列表进行操作，b也会发生变化，这是因为，我们修改了嵌套的list，修改外层元素，会修改它的引用，
    # 让它们指向别的位置，修改嵌套列表中的元素，列表的地址并未发生变化，指向的都是用一个位置。
    print(a is b)


def deep_copy():
    """
    深拷贝只有一种形式，copy 模块中的deepcopy()函数。
    深拷贝和浅拷贝对应，深拷贝拷贝了对象的所有元素，包括多层嵌套的元素。因此，它的时间和空间开销要高。
    :return:
    """
    a = [1,2,"hello",['python', 'C++']]
    b = copy.deepcopy(a)
    print(b)

if __name__ == '__main__':
    shallow_copy()
    deep_copy()
