class Node(object):
    def __init__(self, item):
        self.item = item
        self.next = None


class SingleList(object):
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def loop(self):
        current_num = self.head
        while current_num is not None:
            print(current_num.item)
            current_num = current_num.next

    def add(self, item):
        node = Node(item)
        node.next = self.head
        self.head = node

if __name__ == '__main__':
    sl = SingleList()
    print(sl.is_empty())
    sl.add(1)
    sl.add(2)
    sl.add(3)
    sl.loop()