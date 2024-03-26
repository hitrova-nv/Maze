import pygame

sprites = {"normal": "sprites/ghost_normal.png", "shocked": "sprites/ghost_shocked.png"}


class Villian:
    def __init__(self):
        self.speed = 0.2  # 1 клетка в обновление
        self.cur_s = 0  # сколько прошёл на данный момент
        self.shocked = False
        self.time_shock = 15
        self.cur_time_shock = 0

    def update(self, pos_v, pos_h):
        if self.shocked:
            self.cur_time_shock += 1
            if self.cur_time_shock >= self.time_shock:
                self.cur_time_shock = 0
                self.shocked = False
            return 0, 0
        self.cur_s += self.speed
        if self.cur_s >= 1:
            s = self.cur_s
            self.cur_s = 0
            vector = (pos_h[0] - pos_v[0], pos_h[1] - pos_v[1])
            if abs(vector[0]) == abs(vector[1]) and vector[0] != 0:
                return vector[0] // abs(vector[0]) * int(s), vector[1] // abs(vector[1]) * int(s)
            else:
                if abs(vector[0]) > abs(vector[1]):
                    return vector[0] // abs(vector[0]) * int(s), 0
                elif abs(vector[0]) < abs(vector[1]):
                    return 0, vector[1] // abs(vector[1]) * int(s)
                else:
                    return 0, 0
        else:
            return 0, 0

    def shock(self):
        self.shocked = True

    def sprite(self):
        if self.shocked:
            return sprites["shocked"]
        return sprites["normal"]
