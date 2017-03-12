class SequentialDisplacement:
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
            return False, None

        ret_val = '[connection matrix]\n'
        for i in self.connection_matrix:
            ret_val += str(i) + '\n'

        if self.first_step:
            ret_val += '\n[first step]\n'
            element_to_place, log = self.select_first_element()
            ret_val += log
            self.first_step = False
        else:
            ret_val += '\n[next_step]\n'
            element_to_place, log = self.select_next_element()
            ret_val += log

        ret_val += '\n[find pos]\n'
        place_for_element, log = self.select_place(element_to_place)
        ret_val += log
        self.map[place_for_element] = element_to_place

        return True, ret_val

    def compute_all(self):
        while self.next_step()[0]:
            pass

    def select_first_element(self):
        max_sum = None
        ret_val = None
        log = ''
        placed_elements = [i for i in self.elements_set if i in self.map.values()]
        log += 'placed elements: ' + str(placed_elements) + '\n'
        unplaced_elements = [i for i in self.elements_set if i not in self.map.values()]
        log += 'unplaced elements: ' + str(unplaced_elements) + '\n'
        for i in unplaced_elements:
            connections = self.connection_matrix[i]
            sum_connections = 0
            for j in unplaced_elements:
                if j != i:
                    sum_connections += connections[j]
            log += str(i) + ':' + str(sum_connections) + '\n'
            if max_sum is None or sum_connections > max_sum:
                max_sum = sum_connections
                ret_val = i
        log += 'max_sum = ' + str(max_sum) + '\n'
        log += 'i_max_sum = ' + str(ret_val) + '\n'
        return ret_val, log

    def select_next_element(self):
        max_sum = None
        ret_val = None
        log = ''
        placed_elements = [i for i in self.elements_set if i in self.map.values()]
        log += 'placed elements: ' + str(placed_elements) + '\n'
        unplaced_elements = [i for i in self.elements_set if i not in self.map.values()]
        log += 'unplaced elements: ' + str(unplaced_elements) + '\n'
        for i in unplaced_elements:
            connections = self.connection_matrix[i]
            sum_connections = 0
            for j in self.elements_set:
                if j != i:
                    if j in placed_elements:
                        sum_connections += connections[j]
                    elif j in unplaced_elements:
                        sum_connections -= connections[j]
            log += str(i) + ':' + str(sum_connections) + '\n'
            if max_sum is None or sum_connections > max_sum:
                max_sum = sum_connections
                ret_val = i
        log += 'max_sum = ' + str(max_sum) + '\n'
        log += 'i_max_sum = ' + str(ret_val) + '\n'
        return ret_val, log

    def select_place(self, element_to_place):
        free_positions = [key for key, value in self.map.items() if value is None]
        log = ''
        ret_val = None
        min_l = None
        for i in free_positions:
            l = self.compute_l(element_to_place, i)
            log += 'pos = ' + str(i) + ' : ' + str(l) + '\n'
            if ret_val is None or l < min_l:
                ret_val = i
                min_l = l
        log += 'min_l = ' + str(min_l) + '\n'
        log += 'min_pos = ' + str(ret_val) + '\n'
        return ret_val, log

    def compute_l(self, element, position):
        ret_val = 0
        for key, value in self.map.items():
            if value is not None:
                ret_val += self.connection_matrix[element][value] * self.distance_matrix[position][key]

        return ret_val
