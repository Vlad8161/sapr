import os

import sys


class SimpleRouting:
    def __init__(self, connections, positions, packages):
        super().__init__()
        self.current_backward_coord = None
        self.direction = None
        self.wave_length = None
        self.current_segment_index = None
        self.connections = connections
        self.positions = {v: k for k, v in positions.items()}
        self.packages = packages
        self.work_field = [[0] * 85 for i in range(27)]
        self.base_coords = {
            0: (1, 1),
            1: (6, 1),
            2: (6, 28),
            3: (6, 57),
            4: (14, 1),
            5: (14, 28),
            6: (14, 57),
            7: (22, 1),
            8: (22, 28),
            9: (22, 57),
        }
        self.segments = []

        self.compute_positions()
        self.print_pins()
        self.compute_segments()
        self.begin()

    def next_step(self):
        if self.current_segment_index >= len(self.segments):
            return True

        start_coord = self.segments[self.current_segment_index][0]
        end_coord = self.segments[self.current_segment_index][1]
        print(end_coord)

        if self.direction:
            if self.wave_length == 0:
                self.clear_work_field()
                segment_finished = False
                for i in self.get_closest_fields(start_coord):
                    if self.get_field_value(i) == 0:
                        self.set_field_value(i, self.wave_length + 1)
                    elif i == end_coord:
                        self.to_next_segment()
                        segment_finished = True
                        break
                if segment_finished:
                    self.to_next_segment()
                else:
                    self.wave_length += 1
            else:
                next_wave = False
                for i in range(len(self.work_field)):
                    for j in range(len(self.work_field[i])):
                        curr_coord = (i, j)
                        curr_val = self.get_field_value(curr_coord)

                        if curr_val != 0 and curr_val != -1:
                            continue
                        for k in self.get_closest_fields(curr_coord):
                            val = self.get_field_value(k)
                            if val == self.wave_length or k == start_coord:
                                if curr_coord == end_coord:
                                    self.direction = False
                                    break
                                elif curr_val == 0:
                                    self.set_field_value(curr_coord, self.wave_length + 1)
                                    next_wave = True
                if next_wave and self.direction:
                    self.wave_length += 1
                elif self.direction:
                    self.to_next_segment()
        else:
            if self.current_backward_coord is not None and self.current_backward_coord == start_coord:
                self.to_next_segment()

            if self.current_backward_coord is None:
                print(self.wave_length)
                buf = [i for i in self.get_closest_fields(end_coord) if self.get_field_value(i) == self.wave_length]
                self.current_backward_coord = buf[0]
            else:
                self.set_field_value(self.current_backward_coord, -1)
                self.current_backward_coord = [i for i in self.get_closest_fields(self.current_backward_coord)
                                               if self.get_field_value(i) == self.wave_length][0]
            self.wave_length -= 1

    def compute_positions(self):
        for i in self.packages.keys():
            p = self.positions[i]
            base_c = self.base_coords[p]
            for j in self.packages[i].keys():
                self.packages[i][j] = (
                    base_c[0] + self.packages[i][j][0],
                    base_c[1] + self.packages[i][j][1],
                )

    def print_pins(self):
        for k, v in self.packages.items():
            for k1, v1 in v.items():
                self.work_field[v1[0]][v1[1]] = -1

    def compute_segments(self):
        for k, v in self.connections.items():
            if len(v) < 2:
                continue

            for j in range(len(v) - 1):
                v0 = v[j][0]
                v1 = v[j][1]
                vv0 = v[j + 1][0]
                vv1 = v[j + 1][1]
                segment = (
                    self.packages[v0][v1],
                    self.packages[vv0][vv1],
                )
                self.segments.append(segment)

    def begin(self):
        self.current_segment_index = 0
        self.wave_length = 0
        self.direction = True
        self.current_backward_coord = None

    def to_next_segment(self):
        self.current_segment_index += 1
        self.wave_length = 0
        self.direction = True
        self.current_backward_coord = None

    def get_closest_fields(self, coord):
        ret_val = []
        if coord[0] - 1 >= 0:
            ret_val.append((coord[0] - 1, coord[1]))
        if coord[0] + 1 < len(self.work_field):
            ret_val.append((coord[0] + 1, coord[1]))
        if coord[1] - 1 >= 0:
            ret_val.append((coord[0], coord[1] - 1))
        if coord[1] + 1 < len(self.work_field[0]):
            ret_val.append((coord[0], coord[1] + 1))
        return ret_val

    def get_field_value(self, coord):
        return self.work_field[coord[0]][coord[1]]

    def set_field_value(self, coord, value):
        self.work_field[coord[0]][coord[1]] = value

    def clear_work_field(self):
        for i in self.work_field:
            for j in range(len(i)):
                if i[j] > 0:
                    i[j] = 0
