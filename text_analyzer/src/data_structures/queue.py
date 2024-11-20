class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """Add an item to the back of the queue."""
        self.items.append(item)

    def dequeue(self):
        """Remove and return the item at the front of the queue.
        If the queue is empty, return None."""
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def front(self):
        """Return the item at the front of the queue without removing it.
        If the queue is empty, return None."""
        if not self.is_empty():
            return self.items[0]
        return None

    def is_empty(self):
        """Check if the queue is empty."""
        return len(self.items) == 0

    def size(self):
        """Return the number of items in the queue."""
        return len(self.items)

    def __str__(self):
        """Return a string representation of the queue."""
        return str(self.items)
