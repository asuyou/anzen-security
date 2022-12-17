from typing import TypeVar, Generic
from dataclasses import dataclass
import math
import random

T = TypeVar('T')

@dataclass
class Position(Generic[T]):
    data: T
    priority: float = math.inf

class Queue(Generic[T]):
    """
    This acts as a min-value binary heap
    Minimum value is stored at the root
    This is stored as an array
    We return (integer, value). Integer acts a pointer
    """
    def __init__(self):
        self.array = []
    
    def insert(self, data: T, priority: int) -> bool:
        
        self.array.append(Position(data, priority))

        self._shift_node_up(len(self.array) - 1)

        return True

    def remove(self) -> T | None:
        if len(self.array) == 0:
            return None

        data = self.array[0].data

        self.swap(0, -1)
        del self.array[-1]

        self._heapify(0)


        return data

    def _parent(self, pos: int) -> int:
        """
        Returns the parent node of the current node
        """
        return ((pos - 1) // 2)

    def _left(self, pos: int) -> int:
        """
        Returns the left node of the current node
        """
        return ((pos * 2) + 1)

    def _right(self, pos: int) -> int:
        """
        Returns the right node of the current node
        """
        return ((pos * 2) + 2)


    def _is_root(self, pos: int) -> bool:
        return pos == 0

    def _heapify(self, pos: int):
        size = len(self.array) - 1
        if pos >= size:
            return

        left_index = self._left(pos)
        right_index = self._right(pos)
    
        min = pos

        if left_index < size and self.array[left_index].priority < self.array[min].priority:
            min = left_index

        if right_index < size and self.array[right_index].priority < self.array[min].priority:
            min = right_index

        if min != pos:
            self.swap(pos, min)
            self._heapify(min)

    def _shift_node_up(self, pos: int):
        if self._is_root(pos):
            return

        parent = self._parent(pos)
        current = pos
        priority = self.array[pos].priority
        
        while parent >= 0 and priority < self.array[parent].priority:
            self.swap(parent, current)
            current = self._parent(current)
            parent = self._parent(current)

    def swap(self, pos_1: int, pos_2: int):
        """
        Swaps the position of 2 nodes
        """
        self.array[pos_1], self.array[pos_2] = self.array[pos_2], self.array[pos_1]

    def __str__(self) -> str:
        self.print()
        return super().__str__()

    def print(self, pos:int = 0, depth: int = 0):
        if pos >= len(self.array):
            return

        print("  |"*depth + f"--{self.array[pos].priority}")

        self.print(self._left(pos), depth + 1)
        self.print(self._right(pos), depth + 1)


if __name__ == "__main__":
    p: Queue[int] = Queue()

    for i in range(0, 50):
        v = random.randint(0, 200)
        p.insert(v, v)

    print(p)

    for i in range(0, 10):
        print(p.remove())

