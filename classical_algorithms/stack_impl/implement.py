class Node(object):
    def __init__(self, item):
        self.item = item
        self.next = None


class Stack(object):
    def __init__(self):
        self.top = None

    def is_empty(self):
        return self.top is None

    def peek(self):
        if self.top is not None:
            return self.top.item
        return None

    def push(self, item):
        node = Node(item)
        node.next = self.top
        self.top = node
        return node.item

    def pop(self):
        element = self.top
        self.top = element.next
        return element.item

    def clear(self):
        while self.top is not None:
            self.pop()

    def size(self):
        count = 0
        current_item = self.top
        while current_item is not None:
            current_item = current_item.next
            count += 1
        return count


if __name__ == '__main__':
    stack = Stack()
    print(stack.push(5))
    print(stack.push(4))
    print(stack.push(7))
    print(stack.size())
    print(stack.pop())
    print(stack.size())
    stack.clear()
    print(stack.is_empty())