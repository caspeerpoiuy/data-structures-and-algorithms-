class Node(object):
    def __init__(self, item):
        self.item = item
        self.next = None


class Stack(object):
    def __init__(self):
        self.top = None

    def peek(self):
        if self.top is not None:
            return self.top.item
        return None

    def push(self, item):
        node = Node(item)
        node.next = self.top
        self.top = node

    def pop(self):
        node=self.top
        self.top = node.next
        return node.item


if __name__ == '__main__':
    stack = Stack()
    print(stack.peek())
    stack.push(5)
    stack.push(4)
    stack.push(3)
    print(stack.peek())
    print(stack.pop())
    print(stack.peek())
