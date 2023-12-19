class ListNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        """Append a new node with the provided data to the end of the list."""
        new_node = ListNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def remove(self, node):
        """Remove the specified node from the list."""
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node == self.head:
            self.head = node.next
        if node == self.tail:
            self.tail = node.prev
        del node


    def find(self, data):
        """Find the first node with the specified data."""
        current = self.head
        while current:
            if current.data == data:
                return current
            current = current.next
        return None
    

    def insert(self, data, after_node=None):
        """Insert a new node with the provided data after the specified node.
        If no node is specified, insert at the beginning of the list."""
        new_node = ListNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        elif not after_node:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        else:
            new_node.next = after_node.next
            new_node.prev = after_node
            after_node.next = new_node
            if new_node.next:
                new_node.next.prev = new_node
            if after_node == self.tail:
                self.tail = new_node
 