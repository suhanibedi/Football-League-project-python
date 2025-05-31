""" Hash Table ADT

Defines a Hash Table using a modified Linear Probe implementation for conflict resolution.
"""
from __future__ import annotations
__author__ = 'Jackson Goerner'
__since__ = '07/02/2023'

from data_structures.referential_array import ArrayR
from typing import Generic, TypeVar, Union

K = TypeVar('K')
V = TypeVar('V')


class FullError(Exception):
    pass

class Sentinel():
    pass

class HashyStepTable(Generic[K, V]):
    """
    Hashy Step Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes=None) -> None:
        """
        Initialise the Hash Table.

        Complexity:
        Best Case Complexity: O(max(N, M)) where N is the length of TABLE_SIZES and M is the length of sizes.
        Worst Case Complexity: O(max(N, M)) where N is the length of TABLE_SIZES and M is the length of sizes.
        """
        if sizes is not None:
            self.TABLE_SIZES = sizes
        self.size_index = 0
        self.array: ArrayR[Union[tuple[K, V], None]] = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

    def hash(self, key: K) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.

        Complexity:
        Best Case Complexity: O(len(key))
        Worst Case Complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K) -> int:
        """
        Used to determine the step size for our hash table.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        value = (4*len(key)*ord(key[0]) + 3) % 13
        return value

    @property
    def table_size(self) -> int:
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def _hashy_probe(self, key: K, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using hashy probing.

        Raises:
        KeyError: When the key is not in the table, but is_insert is False.
        FullError: When a table is full and cannot be inserted.

        Complexity:
        Best Case Complexity: O(k), where k is the len(key)
        Worst Case Complexity: O(k + N), where k is the len(key) and N is self.table_size

        Complexity Analysis:
        The best case scenario occurs when the initial position is determined, and in the first iteration of the
        for loop, self.array[position] is None and the is_insert argument is True. This allows the loop to terminate
        early, as the final position is quickly returned. Therefore, making the best case complexity O(k), where k is the len(key).

        The worst case scenario occurs when the initial position is determined, and the for loop has to run through the capacity 
        of the hash table (self.table_size) because the key being search for is not in the hash table. This means the is_insert
        argument is False, and the key is searched in the list outputted by self.keys() to then raise a keyerror. Hence, this makes the
        worst case complexity simplified to O(k + N)), where k is the len(key) and N is self.table_size.
        """
        # Initial position
        position = self.hash(key)

        # Custom logic to be implemented here
        step_size = self.hash2(key)

        for _ in range(0,self.table_size):
            if self.array[position] is None:
                if is_insert:
                    return position
                else:
                    position = (position + step_size) % self.table_size
                    continue
            elif self.array[position] is Sentinel:
                if is_insert:
                    return position
            elif self.array[position][0] == key:
                return position
            else:
                position = (position + step_size) % self.table_size

        if is_insert:
            raise FullError("Table is full!")
        else:
            if key not in self.keys():
                raise KeyError(key)

    
    def keys(self) -> list[K]:
        """
        Returns all keys in the hash table.

        :complexity: O(N) where N is self.table_size.
        """
        res = []
        for x in range(self.table_size):
            if self.array[x] is not None:
                res.append(self.array[x][0])
        return res

    def values(self) -> list[V]:
        """
        Returns all values in the hash table.

        :complexity: O(N) where N is self.table_size.
        """
        res = []
        for x in range(self.table_size):
            if self.array[x] is not None:
                res.append(self.array[x][1])
        return res

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See hashy probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :complexity: See hashy probe.
        :raises KeyError: when the key doesn't exist.
        """
        position = self._hashy_probe(key, False)
        return self.array[position][1]

    def __setitem__(self, key: K, data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        :complexity: See hashy probe.
        :raises FullError: when the table cannot be resized further.
        """
        position = self._hashy_probe(key, True)

        if self.array[position] is None:
            self.count += 1

        self.array[position] = (key, data)

        if len(self) > self.table_size * 2 / 3:
            self._rehash()

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) using lazy deletion

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(N), where N is self.table_size.

        Complexity analysis:
        The best case occurs when the value of the first element of self.array corresponds to the 
        key argument. This allows the loop to terminate early, hence the best case complexity being constant.

        The worst case occurs when the value of the last element of self.array corresponds to the key argument.
        This means the loop runs through all elements in self.array, meaning N times, hence the worst case
        complexity being O(N), where N is self.table_size.
        """
        position = None
        for elem in range(len(self.array)):
            if self.array[elem] is None:
                continue
            if self.array[elem][0] == key:
                position = elem
                break
        if position is not None:
            self.array[position] = (Sentinel, Sentinel)
        self.count -= 1

    def is_empty(self) -> bool:
        return self.count == 0

    def is_full(self) -> bool:
        return self.count == self.table_size

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        Complexity:
        Best Case Complexity: O(l + N)), where l is the number of elements in self.TABLE_SIZES, and N is self.table_size 
        Worst Case Complexity: O(l + N)), where l is the number of elements in self.TABLE_SIZES and N is self.table_size

        Complexity analysis:
        The best case and worst case scenario occurs when the index of self.table_size is found from the 
        self.TABLE_SIZES list in HashyStepTable class, which has a time complexity of O(l), where l is the 
        number of elements in self.TABLE_SIZES. To add all the elements in the current hash table into the new hash 
        table, the for loop iterates through all current elements, which has a time complexity of O(N), where N is
        self.table_size. Hence, the best case and worst case complexity is when these two complexities are added, so
        it is expressed as O(l + N), where l is the number of elements in self.TABLE_SIZES, and N is self.table_size. 

        """
        i = self.TABLE_SIZES.index(self.table_size)
        old_table = self.array
        self.table = ArrayR(self.TABLE_SIZES[i + 1])
        # Empty
        x = 0
        for item in old_table:
            if item is not None:
                # Insert
                self.table[x] = (item[0],item[1])
            x += 1
        self.array = self.table

    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular
        order).
        :complexity: O(N * (str(key) + str(value))) where N is the table size
        """
        result = ""
        for item in self.array:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result
