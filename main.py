import sys


class DisplacementAlgorithm:
    def __init__(self, connection_matrix, distance_matrix):
        super().__init__()
        self.connection_matrix = connection_matrix
        self.distance_matrix = distance_matrix
        self.elements_set = set(range(len(distance_matrix)))
        self.map = {i: None for i in self.elements_set}
        self.map[0] = 0
        self.first_step = True

    def next_step(self):
        if set(self.map.values()).issuperset(self.elements_set):
            return False

        if self.first_step:
            element_to_place = self.select_first_element()
            self.first_step = False
        else:
            element_to_place = self.select_next_element()

        place_for_element = self.select_place(element_to_place)
        self.map[place_for_element] = element_to_place

        return True

    def select_first_element(self):
        max_sum = None
        ret_val = None
        placed_elements = [i for i in self.elements_set if i in self.map.values()]
        unplaced_elements = [i for i in self.elements_set if i not in self.map.values()]
        for i in unplaced_elements:
            connections = self.connection_matrix[i]
            sum_connections = 0
            for j in unplaced_elements:
                if j != i:
                    sum_connections += connections[j]
            if max_sum is None or sum_connections > max_sum:
                max_sum = sum_connections
                ret_val = i
        return ret_val

    def select_next_element(self):
        max_sum = None
        ret_val = None
        placed_elements = [i for i in self.elements_set if i in self.map.values()]
        unplaced_elements = [i for i in self.elements_set if i not in self.map.values()]
        for i in unplaced_elements:
            connections = self.connection_matrix[i]
            sum_connections = 0
            for j in self.elements_set:
                if j != i:
                    if i in placed_elements:
                        sum_connections += connections[j]
                    elif i in unplaced_elements:
                        sum_connections -= connections[j]
            if max_sum is None or sum_connections > max_sum:
                max_sum = sum_connections
                ret_val = i
        return ret_val

    def select_place(self, element_to_place):
        free_positions = [key for key, value in self.map.items() if value is None]
        ret_val = None
        min_l = None
        for i in free_positions:
            l = self.compute_l(element_to_place, i)
            if ret_val is None or l < min_l:
                ret_val = i
                min_l = l
        return ret_val

    def compute_l(self, element, position):
        ret_val = 0
        for key, value in self.map.items():
            if value is not None:
                ret_val += self.connection_matrix[element][value] * self.distance_matrix[position][key]

        return ret_val


d = [
    [0, 0, 0, 0, 3, 2, 2, 4, 2, 1],
    [0, 0, 4, 4, 0, 0, 0, 0, 0, 0],
    [0, 4, 0, 4, 0, 1, 0, 0, 0, 0],
    [0, 4, 4, 0, 0, 2, 2, 4, 1, 2],
    [3, 0, 0, 0, 0, 2, 2, 1, 0, 1],
    [2, 0, 1, 2, 2, 0, 2, 2, 0, 0],
    [2, 0, 0, 2, 2, 2, 0, 2, 0, 0],
    [4, 0, 0, 4, 1, 2, 2, 0, 0, 2],
    [2, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 2, 0, 0, 0, 2, 0, 0],
]

t = [
    [0, 1, 1, 1, 2, 2, 2, 3, 3, 3],
    [1, 0, 1, 2, 3, 2, 1, 2, 3, 4],
    [1, 1, 0, 1, 2, 1, 2, 3, 2, 3],
    [1, 2, 1, 0, 1, 2, 3, 4, 3, 2],
    [2, 3, 2, 1, 0, 1, 2, 3, 2, 1],
    [2, 2, 1, 2, 1, 0, 1, 2, 1, 2],
    [2, 1, 2, 3, 2, 1, 0, 1, 2, 3],
    [3, 2, 3, 4, 3, 2, 1, 0, 1, 2],
    [3, 3, 2, 3, 2, 1, 2, 1, 0, 1],
    [3, 4, 3, 2, 1, 2, 3, 2, 1, 0],
]

alg = DisplacementAlgorithm(connection_matrix=d, distance_matrix=t)
while alg.next_step():
    for pos, elem in alg.map.items():
        print('{0} : {1}'.format(pos, elem))
    sys.stdin.read(1)
