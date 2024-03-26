import pygame
from Hero import Hero
from Villian import Villian
from UI import score_panel
from random import choice
from random import randint

wall_colors = ['darkblue', 'darkorange', 'darkgrey', 'darkgreen']
build_colors = ['orange', 'green', 'blue', 'red', 'yellow', 'white', 'darkblue']

class Cell:
    def __init__(self, x, y, maze):
        self.maze = maze
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.money = False
        self.charge = False
        self.hero = False
        self.villian = False

    def draw(self, wall_color):
        x, y = self.x * self.maze.TILE, self.y * self.maze.TILE
        if self.visited:
            pygame.draw.rect(self.maze.screen, pygame.Color('black'), (x, y, self.maze.TILE, self.maze.TILE))
        if self.money and not self.maze.state == "building":
            pygame.draw.circle(self.maze.screen, pygame.Color('yellow'), (x + self.maze.TILE // 2, y + self.maze.TILE // 2),
                               5)
        if self.charge and not self.maze.state == "building":
            pygame.draw.circle(self.maze.screen, pygame.Color('orange'), (x + self.maze.TILE // 2, y + self.maze.TILE // 2),
                               10)
        if self.walls['top']:
            pygame.draw.line(self.maze.screen, pygame.Color(wall_color), (x, y), (x + self.maze.TILE, y), 3)
        if self.walls['right']:
            pygame.draw.line(self.maze.screen, pygame.Color(wall_color), (x + self.maze.TILE, y),
                             (x + self.maze.TILE, y + self.maze.TILE), 3)
        if self.walls['bottom']:
            pygame.draw.line(self.maze.screen, pygame.Color(wall_color), (x + self.maze.TILE, y + self.maze.TILE),
                             (x, y + self.maze.TILE), 3)
        if self.walls['left']:
            pygame.draw.line(self.maze.screen, pygame.Color(wall_color), (x, y + self.maze.TILE), (x, y), 3)

    def check_cell(self, x, y):
        find_index = lambda cx, cy: cx + cy * self.maze.cols
        if x < 0 or x > self.maze.cols - 1 or y < 0 or y > self.maze.rows - 1:
            return False
        return self.maze.grid_cells[find_index(x, y)]

    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False


class Maze:
    def __init__(self, rows, cols, TILE, screen, c_score):
        self.score = score_panel(c_score)
        self.TILE = TILE
        self.rows = rows
        self.cols = cols
        self.screen = screen
        self.wall_color = choice(wall_colors)
        self.build_color = choice(build_colors)
        self.grid_cells = [Cell(col, row, self) for row in range(rows) for col in range(cols)]
        for y in range(1, 17, 2):
            for x in range(2, 18, 3):
                self.grid_cells[y * 20 + x].money = True
        for y in range(6, 19, 6):
            for x in range(4, 16, 11):
                self.grid_cells[y * 20 + x].charge = True

        self.current_cell = self.grid_cells[0]
        self.stack = []
        self.colors, self.color = [], randint(10, 70)
        self.state = "building"
        self.hero = Hero()
        self.villian = Villian()
        self.pos_h = (0, 0)
        self.pos_v = (19, 19)
        self.cur_pos_v = (0, 0)
        self.sprite_hero = 'sprites/pacman_close.png'
        self.sprite_villian = 'sprites/ghost_normal.png'

    def remove_walls(self, current, next):
        dx = current.x - next.x
        if dx == 1:
            current.walls['left'] = False
            next.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            next.walls['left'] = False
        dy = current.y - next.y
        if dy == 1:
            current.walls['top'] = False
            next.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom'] = False
            next.walls['top'] = False

    def sprite(self, img_n, pos):
        img = pygame.image.load(img_n).convert()
        img.set_colorkey((0, 0, 0))
        img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
        rect = img.get_rect(
            center=(pos[0] * self.TILE + self.TILE // 2, pos[1] * self.TILE + self.TILE // 2))
        self.screen.blit(img, rect)
        if img_n == self.sprite_villian and not self.villian.shocked:
            pygame.draw.rect(self.screen, pygame.Color("black"),
                             (self.pos_v[0] * self.TILE + self.TILE // 2 - 12 + 2 * self.cur_pos_v[0],
                              self.pos_v[1] * self.TILE + self.TILE // 2 - 10 + 2 * self.cur_pos_v[1], 4, 4))
            pygame.draw.rect(self.screen, pygame.Color("black"),
                             (self.pos_v[0] * self.TILE + self.TILE // 2 + 8 + 2 * self.cur_pos_v[0],
                              self.pos_v[1] * self.TILE + self.TILE // 2 - 10 + 2 * self.cur_pos_v[1], 4, 4))

    def render(self):
        self.screen.fill(pygame.Color(self.build_color))
        [cell.draw(self.wall_color) for cell in self.grid_cells]
        self.score.render(self.screen)
        if self.state == "building":
            [pygame.draw.rect(self.screen, self.colors[i],
                              (cell.x * self.TILE + 2, cell.y * self.TILE + 2, self.TILE - 4, self.TILE - 4)) for
             i, cell in enumerate(self.stack)]
        elif self.state == 'game':
            self.sprite(self.sprite_villian, self.pos_v)
            self.sprite(self.sprite_hero, self.pos_h)

    def update(self):
        if self.state == "building":
            self.current_cell.visited = True
            next_cell = self.current_cell.check_neighbors()
            if next_cell:
                next_cell.visited = True
                self.stack.append(self.current_cell)
                self.colors.append((min(self.color, 255), 0, 100))
                self.color += 1
                self.remove_walls(self.current_cell, next_cell)
                self.current_cell = next_cell
            elif self.stack:
                self.current_cell = self.stack.pop()
            else:
                self.state = "game"

    def update_pers(self):
        if self.state == "game":
            move = self.hero.update(self.villian.shocked)
            if move == "shock":
                self.villian.shock()
            elif move != "stay":
                is_moving = False
                if move == "top" and not self.grid_cells[self.pos_h[0] + 20 * self.pos_h[1]].walls["top"]:
                    self.grid_cells[self.pos_h[0] + 20 * self.pos_h[1]].hero = False
                    self.pos_h = (self.pos_h[0], self.pos_h[1] - 1)
                    self.grid_cells[self.pos_h[0] + 20 * self.pos_h[1]].hero = True
                    is_moving = True
                elif move == "bottom" and not self.grid_cells[self.pos_h[0] + 20 * self.pos_h[1]].walls["bottom"]:
                    self.grid_cells[self.pos_h[0] + 20 * self.pos_h[1]].hero = False
                    self.pos_h = (self.pos_h[0], self.pos_h[1] + 1)
                    self.grid_cells[self.pos_h[0] + 20 * self.pos_h[1]].hero = True
                    is_moving = True
                elif move == "left" and not self.grid_cells[self.pos_h[0] + 20 * self.pos_h[1]].walls["left"]:
                    self.grid_cells[self.pos_h[0] + 20 * self.pos_h[1]].hero = False
                    self.pos_h = (self.pos_h[0] - 1, self.pos_h[1])
                    self.grid_cells[self.pos_h[0] + 20 * self.pos_h[1]].hero = True
                    is_moving = True
                elif move == "right" and not self.grid_cells[self.pos_h[0] + 20 * self.pos_h[1]].walls["right"]:
                    self.grid_cells[self.pos_h[0] + 20 * self.pos_h[1]].hero = False
                    self.pos_h = (self.pos_h[0] + 1, self.pos_h[1])
                    self.grid_cells[self.pos_h[0] + 20 * self.pos_h[1]].hero = True
                    is_moving = True
                if is_moving:
                    self.sprite_hero = self.hero.sprite(move)
                    if self.grid_cells[self.pos_h[0] + 20 * self.pos_h[1]].money:
                        self.hero.money += 1
                        self.grid_cells[self.pos_h[0] + 20 * self.pos_h[1]].money = False
                    if self.grid_cells[self.pos_h[0] + 20 * self.pos_h[1]].charge:
                        self.hero.charge += 1
                        self.grid_cells[self.pos_h[0] + 20 * self.pos_h[1]].charge = False
                cur_pos_v = self.villian.update(self.pos_v, self.pos_h)
                if cur_pos_v != (0, 0): self.cur_pos_v = cur_pos_v
                self.pos_v = (self.pos_v[0] + cur_pos_v[0], self.pos_v[1] + cur_pos_v[1])
                self.sprite_villian = self.villian.sprite()
                self.score.update(self.hero.money, self.hero.charge)
                if self.hero.money == 30:
                    self.state = "win"
                elif self.pos_v[0] == self.pos_h[0] and self.pos_h[1] == self.pos_v[1] and not self.villian.shocked:
                    self.state = "gameover"
