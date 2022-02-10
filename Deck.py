import numpy as np
from random import seed, randint
class Deck():
    def __init__(self, name):
        self.name = name
        self.arr = np.empty((0, 2), str)
    def fill_new(self, suits):
        np.delete(self.arr, 1, axis=1)
        np.delete(self.arr, 0, axis=1)
        for num in range(2):
            for i in range(4):
                for x in range(9):
                    self.arr = np.append(self.arr, np.array([[suits[i], str(x+1)]]), axis=0)
                self.arr = np.append(self.arr, [[suits[i], '@']], axis=0)
                self.arr = np.append(self.arr, [[suits[i], 'r']], axis=0)
                self.arr = np.append(self.arr, [[suits[i], 'S']], axis=0)
        for i in range(4):
            self.arr = np.append(self.arr, [[suits[i], '0']], axis=0)
            self.arr = np.append(self.arr, np.array([['W','C']]), axis=0)
            self.arr = np.append(self.arr, np.array([['+','$']]), axis=0)
    def shuffle(self):
            for i in range(len(self.arr)):
                swap_idx = randint(0, (len(self.arr)-1))
                rand_value = [self.arr[swap_idx, 0], self.arr[swap_idx, 1]] # Taking Random Value
                temp_value = [self.arr[i, 0], self.arr[i, 1]] # Taking Current Card Value

                self.arr[i, 0] = rand_value[0] # Setting Current Card to Random
                self.arr[i, 1] = rand_value[1] # Setting Current Card to Random

                self.arr[swap_idx, 0] = temp_value[0] # Setting Random Card to Current
                self.arr[swap_idx, 1] = temp_value[1] # Setting Random Card to Current
                seed(randint(0, 9999999999999999))
    def get_next_card(self):
        card_to_return = [self.arr[len(self.arr)-1, 0], self.arr[len(self.arr)-1, 1]]
        self.arr = np.delete(self.arr, len(self.arr)-1,axis=0)
        if len(self.arr) == 0:
            self.fill_new(['R', 'G', 'B', 'Y'])
            self.shuffle()
        return card_to_return