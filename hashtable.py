from abc import ABC, abstractmethod
from typing import Optional


class ConflictResolutionStrategy(ABC):
    @abstractmethod
    def resolve_conflict(self, hash_table: 'HashTable', hashvalue: int, key: int) -> int:
        pass


class LinearProbingStrategy(ConflictResolutionStrategy):
    """
    O(n)  <--- Linear complexity
    """
    def resolve_conflict(self, hash_table: 'HashTable', hashvalue: int, key: int) -> int:
        size = len(hash_table.slots)
        nextslot = hash_table.rehash(hashvalue, size)

        # Track the initial position to avoid infinite loops (stop when we have cycled through all slots)
        startslot = nextslot
        while hash_table.slots[nextslot] is not None and hash_table.slots[nextslot] != key:
            nextslot = hash_table.rehash(nextslot, size)

            # If we loop back to the startslot, it means the table is full or no empty slots are available
            if nextslot == startslot:
                raise Exception("HashTable is full, cannot resolve conflict")

        return nextslot


class BSTStrategy(ConflictResolutionStrategy):
    """
    O(log n) <---- It is logrithmic since it is "binary search"
    during the interview, got asked about set insertion implementation. insertion in set and dictionary are the same
    """
    def resolve_conflict(self, hash_table: 'HashTable', hashvalue: int, key: int) -> int:
        pass


class HashTable(object):
    def __init__(self, size: int, conflict_strategy: ConflictResolutionStrategy) -> None:
        self.size = size
        self.slots = [None] * self.size
        self.data = [None] * self.size
        self.conflict_strategy = conflict_strategy  # Injected strategy

    def put(self, key: int, data: int) -> None:
        """Add Key/Value"""
        hashvalue = self.hashfunction(key, len(self.slots))

        # Slot is empty, just insert the data
        if self.slots[hashvalue] is None:
            self.slots[hashvalue] = key
            self.data[hashvalue] = data
        # Conflict Resolution Here !! (with different strategy injected from the caller)
        else:
            if self.slots[hashvalue] == key:
                self.data[hashvalue] = data
            else:
                # Use the conflict strategy to resolve (could be many strategy)
                nextslot = self.conflict_strategy.resolve_conflict(self, hashvalue, key)

                if self.slots[nextslot] is None:
                    self.slots[nextslot] = key
                    self.data[nextslot] = data
                else:
                    self.data[nextslot] = data

    def hashfunction(self, key: int, size: int) -> int:
        return key % size

    def rehash(self, oldhash: int, size: int) -> int:
        return (oldhash + 1) % size

    def get(self, key: int) -> Optional[int]:
        """Retrive Value By Key"""
        startslot = self.hashfunction(key, len(self.slots))
        data = None
        stop = False
        found = False
        position = startslot

        while self.slots[position] is not None and not found and not stop:
            if self.slots[position] == key:
                found = True
                data = self.data[position]
            else:
                position = self.rehash(position, len(self.slots))
                if position == startslot:
                    stop = True
        return data

    def __getitem__(self, key: int) -> Optional[int]:
        return self.get(key)

    def __setitem__(self, key: int, data: int) -> None:
        self.put(key, data)

    def __str__(self) -> str:
        result = ""
        for i in range(self.size):
            result += f"Slot {i}: Key = {self.slots[i]}, Data = {self.data[i]}\n"
        return result


if __name__ == "__main__":
    # bst_strategy = BSTStrategy()
    linear_strategy = LinearProbingStrategy()
    h = HashTable(5, linear_strategy)
    print('Insert 11, 22, 33')
    h[11] = 11
    h[22] = 22
    h[33] = 33
    print(h)

    print('Insert 44, 55. Now the hashtable is full')
    h[44] = 44
    h[55] = 55
    print(h)

    try:
        h[66] = 66
    except Exception as e:
        print(e)
        print(h)