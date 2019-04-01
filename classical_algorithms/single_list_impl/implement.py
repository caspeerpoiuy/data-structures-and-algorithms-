class Node(object):
    def __init__(self, item):
        self.item = item


class SingleList(object):
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def length(self):
        count = 0
        current_num = self.head
        while current_num is not None:
            count += 1
            current_num = current_num.next
        return count

    def loop(self):
        current_num = self.head
        while current_num is not None:
            print(current_num.item)
            current_num = current_num.next

    def add(self, item):
        node = Node(item)
        node.next = self.head
        self.head = node

    def extend(self, item):
        current_num = self.head
        node = Node(item)
        node.next = None
        while current_num.next is not None:
            current_num = current_num.next
        current_num.next = node

    def insert(self, index, item):
        if index > self.length() or index < 0:
            raise Exception
        elif index == self.length():
            self.extend(item)
        elif index == 0:
            self.add(item)
        else:
            preview_num = None
            current_num = self.head
            node = Node(item)
            count = 0
            while count < index:
                preview_num = current_num
                current_num = current_num.next
                count += 1
            preview_num.next = node
            node.next = current_num

    def remove(self, item):
        preview_num = None
        current_num = self.head
        while current_num is not None:
            if item == current_num.item:
                if preview_num is None:
                    self.head = current_num.next
                    return
                else:
                    preview_num.next = current_num.next
                    return
            preview_num = current_num
            current_num = current_num.next

    def search(self, item):
        current_num = self.head
        while current_num is not None:
            if item == current_num.item:
                return True
            current_num = current_num.next
        return False


if __name__ == '__main__':
    single_list = SingleList()
    single_list.add(3)
    single_list.add(2)
    single_list.add(1)
    single_list.extend(4)
    single_list.insert(1, 5)
    single_list.loop()
    single_list.remove(5)
    print("-"*20)
    single_list.loop()
    single_list.search(4)