class DynamicArray:

    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.arr = [None] * self.capacity

    def __len__(self):
        return self.size

    def get(self, index):
        if index >= 0 and index < self.size:
            return self.arr[index]
        else:
            return None

    def set(self, index, val):
        if index >= 0 and index < self.size:
            self.arr[index] = val
    
    def append(self, val):
        if self.size >= self.capacity:
            self.resize()

        self.arr[self.size] = val
        self.size += 1

    def insert(self, index, val):
        if index >= 0 and index <= self.size:
            if self.size >= self.capacity:
                self.resize()

            for i in range(self.size, index, -1):
                self.arr[i] = self.arr[i - 1]
    
            self.arr[index] = val
            self.size += 1

    def remove(self, index):
        if index >= 0 and index < self.size:
            for i in range(index, self.size - 1):
                self.arr[i] = self.arr[i + 1]
        
            self.size -= 1
            self.arr[self.size] = None
            
    def resize(self):
        copy = self.arr
        self.capacity *= 2

        new_arr = [None] * self.capacity
        for i in range(self.size):
            new_arr[i] = copy[i]
        
        self.arr = new_arr
    
    def __str__(self):
        return str(self.arr)
