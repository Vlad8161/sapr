#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTextEdit

from displacement.sequential import SequentialDisplacement

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


class MainWidget(QWidget):
    def __init__(self, a_schema, flags=None, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)
        self.schema = a_schema
        self.displacement_alg = None
        self.setGeometry(300, 300, 600, 600)
        self.graphics_scene = QGraphicsScene()
        self.graphics_view = QGraphicsView(self.graphics_scene, self)
        self.graphics_view.setGeometry(0, 0, 300, 300)
        self.te_log = QTextEdit(self)
        self.te_log.setGeometry(0, 300, 600, 300)
        btn_start = QPushButton('Start', self)
        btn_start.setGeometry(320, 10, 80, 30)
        btn_start.clicked.connect(self.on_start_clicked)
        btn_next = QPushButton('Next', self)
        btn_next.setGeometry(320, 50, 80, 30)
        btn_next.clicked.connect(self.on_next_clicked)
        btn_end = QPushButton('End', self)
        btn_end.setGeometry(320, 90, 80, 30)
        btn_end.clicked.connect(self.on_end_clicked)

    def view_displacement(self, displacement_map):
        self.graphics_scene.clear()
        for k, v in displacement_map.items():
            if k != 0:
                item_pos = k - 1
                width = 30
                height = 30
                space = 10
                x_pos = 20 + (int(item_pos / 3) * (width + space)) + space
                if int(item_pos / 3) % 2 == 0:
                    y_pos = ((item_pos % 3) * (height + space)) + space
                else:
                    y_pos = 130 - height - (((item_pos % 3) * (height + space)) + space)
                self.graphics_scene.addRect(x_pos, y_pos, width, height)
                if v is not None:
                    self.graphics_scene.addText('{0}'.format(v)).setPos(x_pos, y_pos)
            else:
                self.graphics_scene.addRect(0, 0, 20, 130)
                if v is not None:
                    self.graphics_scene.addText('{0}'.format(v)).setPos(0, 50)

    def on_start_clicked(self):
        self.displacement_alg = SequentialDisplacement(self.schema['matr_d'], t)
        self.view_displacement(self.displacement_alg.map)
        self.te_log.setText('')

    def on_next_clicked(self):
        if self.displacement_alg is not None:
            self.te_log.setText('')
            res, log = self.displacement_alg.next_step()
            self.view_displacement(self.displacement_alg.map)
            if res:
                self.te_log.setText(log)

    def on_end_clicked(self):
        if self.displacement_alg is not None:
            self.te_log.setText('')
            self.displacement_alg.compute_all()
            self.view_displacement(self.displacement_alg.map)


def parse_input():
    with open('input.txt', 'rt') as f:
        wires_detailed = {}
        for line in f:
            k, v = line.split(':')
            v = v.strip()
            k = int(k)
            wire = [tuple([int(j) for j in i.strip().split('_')]) for i in v.split(',') if len(i) != 0]
            wires_detailed[k] = wire
        wires = {k: {i[0] for i in v} for k, v in wires_detailed.items()}
        elements_set = set()
        for k, v in wires.items():
            elements_set = elements_set | v
        matr_d = []
        for i in elements_set:
            connections = [0] * len(elements_set)
            for j in elements_set:
                for k, v in wires.items():
                    if i != j and (i in v) and (j in v):
                        connections[j] += 1
            matr_d.append(connections)
        return {
            'wires': wires,
            'wires_detailed': wires_detailed,
            'matr_d': matr_d,
            'elements_set': elements_set,
        }


if __name__ == '__main__':
    schema = parse_input()
    app = QApplication(sys.argv)
    main_widget = MainWidget(schema)
    main_widget.show()
    sys.exit(app.exec_())
