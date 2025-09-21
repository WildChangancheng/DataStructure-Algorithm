from pprint import pprint
from typing import Any


class Array:
    def __init__(self, max_length: int =20):
        self.__length = 0
        self.__max_length = max_length
        self.__content = []
    def __is_valid_index(self, index:int) -> bool:
        return ((index<self.__max_length) and (index >= 0))
    def show(self) -> None:
        pprint(self.__content)
    def read(self, index:int):
        if not self.__is_valid_index(index=index):
            raise IndexError("Invalid index of this array.")
        if index > self.__length:
            raise IndexError("Invalid index of this array.")
        return self.__content[index]
    def insert(self, index:int, value:Any) -> None:
        if not self.__is_valid_index(index=index):
            raise IndexError("Invalid index of this array.")
        if index > self.__length:
            raise IndexError("Invalid index of this array.")
        if index == self.__length:
            self.__content.append(value)
            self.__length += 1
            return 
        self.__content.append(0)
        for i in range(index, self.__length+1)[::-1]:
            self.__content[i] = self.__content[i-1]
        self.__content[index] = value
        self.__length += 1
        return 
    def delete(self, index:int)->None:
        if not self.__is_valid_index(index=index):
            raise IndexError("Invalid index of this array.")
        if index >= self.__length:
            raise IndexError("Invalid index of this array.")
        if (index == (self.__length-1)):
            self.__content.pop()
            self.__length -= 1
            return 
        for i in range(index, self.__length-1):
            self.__content[i] = self.__content[i+1]
        self.__content.pop()
        self.__length -= 1
        return 
    def update(self, index:int, new_value:Any) -> None:
        self.delete(index=index)
        self.insert(index=index, value=new_value)
        return 

if __name__ == "__main__":
    array = Array()
    array.insert(0, 2)
    array.insert(0, 1)
    array.insert(0, 0)
    array.show()
    array.insert(3, 4)
    array.insert(3, 3)
    array.show()
    print(array.read(index=3))
    array.insert(3, 3)
    array.show()
    array.delete(3)
    array.show()
    array.insert(5, 6)
    array.update(5, 5)
    array.show()
    