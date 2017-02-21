class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self, head=None):
        self.head = head

    def empty(self):
        if self.head:
            return False
        return True

    def printList(self):
        node = self.head
        while node:
            print(node.data, end="->")
            node = node.next
        print()

    def push(self, data):
        node = Node(data, next=self.head)
        self.head = node

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            node = self.head
            while node.next:
                node = node.next
            node.next = new_node

# !!! индексы с 0 !!!
    def insert(self, index, value):
        new_node = Node(value)
        if index <= self.size():
            if index != 0:
                cnt = 0
                current = self.head
                while cnt != index - 1:
                    cnt += 1
                    current = current.next
                new_node.next = current.next
                current.next = new_node

            else:
                self.head, new_node.next = new_node, self.head
        else:
            print('wrong index')

# !!! индексы с 0 !!!
    def delete(self, index):
        if index < self.size():
            if index != 0:
                cnt = 0
                current = self.head
                while cnt != index-1:
                    cnt += 1
                    current = current.next

                current.next = current.next.next
            else:
                self.head = self.head.next
        else:
            print('wrong index')

    def size(self):
        current = self.head
        cnt = 0
        while current:
            cnt += 1
            current = current.next
        return cnt

    def reverse(self):
        current = self.head
        link = None
        while current:
            mem = current.next
            current.next = link
            link = current
            self.head = current
            current = mem

# n3 = Node(3)
# n2 = Node(2, next=n3)
# n1 = Node(1, next=n2)
# n0 = Node(0, next=n1)
# l = LinkedList(head=n0)
# for i in [4,5,6]:
#     l.append(i)
# l = LinkedList()
# l.printList()
# l.reverse()
# l.delete(0)
# # l.insert(1, 28)
# l.printList()
# print(l.size())
