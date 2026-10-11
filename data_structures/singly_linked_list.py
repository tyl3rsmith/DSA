class Node:
    def __init__(self, data):
        self.val = data
        self.next = None

class SinglyLinkedList:

    def __init__(self):
        self.head = None
        self.size = 0

    def prepend(self, val):
        # Insert a new node at the beginning
        temp = self.head
        self.head = Node(val)
        self.head.next = temp
        self.size += 1
    
    def append(self, val):
        # Insert a new node at the end
        new_node = Node(val)

        if not self.head:
            self.head = new_node
        else:
            curr = self.head

            while curr.next:
                curr = curr.next

            curr.next = new_node
            self.size += 1
    
    def search(self, val):
        # Search for a value and return the node's index
        curr = self.head
        i = 0
        while curr:
            if curr.val == val:
                return i
            curr = curr.next
            i += 1
        
        return -1
    
    def remove(self, val):
        # Removes the first node containing val
        if not self.head:
            return False

        if self.head.val  == val:
            self.head = self.head.next
            self.size -= 1
            return True


        prev, curr = self.head, self.head.next

        while prev and curr:
            if curr.val == val:
                prev.next = curr.next
                curr.next = None
                self.size -= 1
                return True
            
            prev, curr = curr, curr.next
        
        return False

    def get(self, index):
        # Get the node at index
        curr_index = 0
        curr = self.head

        while curr:
            if curr_index == index:
                return curr.val

            curr = curr.next
            curr_index += 1
        
        return None

    def insert(self, index, val):
        # Insert node at index
        if index < 0 or index > self.size:
            return False
        
        elif index == 0:
            self.prepend(val)
            return True
        
        else:
            curr_index = 0
            curr = self.head

            while curr:
                if curr_index == index - 1:
                    temp = curr.next
                    new_node = Node(val)
                    curr.next = new_node
                    new_node.next = temp
                    self.size += 1
                    return True
                
                curr = curr.next
                curr_index += 1
                    
            return False
    
    def reverse(self):
        # reverse the order of the linked list
        prev, curr = None, self.head

        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        
        self.head = prev

    def __str__(self):
        values = []
        curr = self.head

        while curr:
            values.append(str(curr.val))
            curr = curr.next

        values.append("None")
        return " -> ".join(values)


ll = SinglyLinkedList()

print("Empty list:", ll)

ll.append(10)
ll.append(20)
ll.append(30)
print("After appending:", ll)

ll.prepend(5)
print("After prepending 5:", ll)

ll.insert(2, 15)
print("After inserting 15 at index 2:", ll)

print("Value at index 2:", ll.get(2))
print("Index of value 30:", ll.search(30))
print("Index of value 99:", ll.search(99))

ll.remove(15)
print("After removing 15:", ll)

ll.reverse()
print("After reversing:", ll)

print("List size:", ll.size)