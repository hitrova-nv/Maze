import pygame

sprites = {"close": "pacman_close.png", "right": "pacman_open_right.png", "bottom": "pacman_open_bottom.png",
           "left": "pacman_open_left.png", "top": "pacman_open_top.png"}


class Hero:
    def __init__(self):
        self.money = 0
        self.charge = 0
        self.change_sprite = 0

    def update(self, is_shock):
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            return "bottom"
        if pygame.key.get_pressed()[pygame.K_UP]:
            return "top"
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            return "left"
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            return "right"
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.charge > 0 and not is_shock:
            self.charge -= 1
            return "shock"
        return "stay"

    def sprite(self, direction):
        if self.change_sprite == 0:
            self.change_sprite = (self.change_sprite + 1) % 2
            return "sprites/" + sprites["close"]
        else:
            self.change_sprite = (self.change_sprite + 1) % 2
            return "sprites/" + sprites[direction]
