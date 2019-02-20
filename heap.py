class Heap:
    def __init__(self):
        self._heap = []

    @property
    def size(self):
        return len(self._heap)

    def parent(self, i):
        index = int((i + 1) / 2)
        return (index - 1) if index else None

    def left(self, i):
        index = (i + 1) * 2
        return (index - 1) if index <= len(self._heap) else None

    def right(self, i):
        index = (i + 1) * 2
        return index if (index + 1) <= len(self._heap) else None

    def balance(self, i):
        if len(self._heap) == 0:
            return

        while True:
            parent_index = self.parent(i)
            if parent_index and self._heap[parent_index] < self._heap[i]:
                self._heap[parent_index], self._heap[i] = self._heap[i], self._heap[parent_index]
                i = parent_index
                continue

            left, right = self.left(i), self.right(i)
            if left and right:
                target = left if self._heap[left] > self._heap[right] else right
            elif left or right:
                target = left or right
            else:
                break

            if self._heap[i] < self._heap[target]:
                self._heap[target], self._heap[i] = self._heap[i], self._heap[target]
                i = target
                continue

            break

    def balance_first(self):
        self.balance(0)

    def balance_last(self):
        self.balance(len(self._heap) - 1)

    def add(self, value):
        self._heap.append(value)
        self.balance_last()

    def pop(self):
        self._heap[0], self._heap[-1] = self._heap[-1], self._heap[0]
        value = self._heap.pop()
        self.balance_first()
        return value

data = [234,3,5,64,3321,5435,65,73,42254,7356,4,3525,6,5,3,45,46,456,435,4523,535,757,8887]

h = Heap()
for i in data:
    h.add(i)

out = []
while h.size:
    out.append(h.pop())

print(out)
