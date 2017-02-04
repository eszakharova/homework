class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


class MyQueue:
    def __init__(self):
        self.inbox = Stack()
        self.outbox = Stack()

    def enqueue(self, x):
        self.inbox.push(x)

    def dequeue(self):
        if self.outbox.isEmpty():
            while not self.inbox.isEmpty():
                self.outbox.push(self.inbox.pop())
        return self.outbox.pop()

    def peek(self):
        if self.outbox.isEmpty():
            while not self.inbox.isEmpty():
                self.outbox.push(self.inbox.pop())
        return self.outbox.peek()

    def isEmpty(self):
        if self.inbox.isEmpty() and self.outbox.isEmpty():
            return True
        else:
            return False
