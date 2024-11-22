class LinkedListNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = LinkedListNode(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def remove(self, data):
        if not self.head:
            return
        if self.head.data == data:
            self.head = self.head.next
            return
        current = self.head
        while current.next and current.next.data != data:
            current = current.next
        if current.next:
            current.next = current.next.next

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def is_empty(self):
        return self.head is None

    def __bool__(self):
        return not self.is_empty()

    def to_list(self):
        return list(self)

    def from_list(self, data_list):
        for item in data_list:
            self.append(item)
