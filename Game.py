import pygame
import pygame_gui
from Maze import Maze
from UI import *

RES = 1202, 1000
WIDTH = RES[0]
HEIGHT = RES[1]
TILE = 50
cols, rows = 20, 20


class Game:
    def __init__(self, screen, score=0):
        self.screen = screen
        self.state = "menu"
        if score != 0:
            print("yes")
            self.menu = Game_Over(RES, score)
        else:
            self.menu = Menu(RES)
        self.pause = pause(RES)
        self.maze = Maze(rows, cols, TILE, screen, score)


if __name__ == "__main__":
    pygame.init()
    sc = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()
    game = Game(sc)
    while True:
        time = pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                if game.state == "game":
                    game.state = "pause"
                else:
                    game.state = "game"
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                game.state = "game"
            if game.state == "game":
                game.maze.update_pers()
        if game.state == "menu":
            game.menu.gui_manager.process_events(event)
            game.menu.gui_manager.update(time)
            game.menu.render(sc)
        if game.state == "pause":
            game.pause.gui_manager.process_events(event)
            game.pause.gui_manager.update(time)
            game.pause.render(sc)
        elif game.state == "game":
            if game.maze.state == "win":
                game.maze.render()
                mes = Message("You Win!\nNext level", sc)
                pygame.display.update()
                clock.tick(1)
                game = Game(sc, game.maze.score.c_score + 500)
                game.state = "game"
            game.maze.update()
            game.maze.render()
        if game.maze.state == "gameover":
            game.maze.render()
            mes = Message("GAME OVER", sc)
            pygame.display.update()
            clock.tick(1)
            game = Game(sc, game.maze.score.c_score)
        if game.maze.state == "building":
            clock.tick(180)
        else:
            clock.tick(15)
        pygame.display.update()
