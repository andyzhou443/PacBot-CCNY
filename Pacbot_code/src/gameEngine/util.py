class Stack:
    # A 'container' with a last-in-first-out (LIFO) queue policy
    def __init__(self):
        self.list = []

    def push(self,item):
        # Push 'item' onto the stack
        self.list.append(item)

    def pop(self):
        # Pop the most recently pushed item from the stack
        return self.list.pop()

    def isEmpty(self):
        # Returns true if the stack is empty
        return len(self.list) == 0

class Queue:
    # A 'container' with a first-in-first-out (FIFO) queue policy
    def __init__(self):
        self.list = []

    def push(self,item):
        # Enqueue the 'item' into the queue
        self.list.insert(0,item)

    def pop(self):
        #   Dequeue the earliest enqueued item still in the queue. This
        #   operation removes the item from the queue.
        
        return self.list.pop()

    def isEmpty(self):
        # Returns true if the queue is empty
        return len(self.list) == 0

