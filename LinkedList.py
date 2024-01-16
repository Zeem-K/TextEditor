class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self) -> None:
        self.head = None
    
    def is_empty(self):
        return self.head is None
    
    def append(self,data):
        node = Node(data)
        if(self.is_empty()):
            self.head = node
        current = self.head
        while current.next != None:
            current = current.next
        current.next = node
    
    def delete(self,data):
        if self.is_empty():
            return
        current = self.head
        while current.next and current.data != data:
            current = current.next
        if current.next:
            current.next = current.next.next
