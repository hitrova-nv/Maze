import pygame
import pygame_gui

image_menu = "sprites/menu.webp"


class Menu:
    def __init__(self, window_size):
        self.window_size = window_size
        button_size = (250, 75)
        button_pos = ((self.window_size[0] - button_size[0]) // 2, self.window_size[1] - button_size[1] - 100)
        button_text = 'Start'
        theme = {'button': {'hovered_bg_color': '#FF0000', 'pressed_bg_color': '#00FF00'}}
        self.gui_manager = pygame_gui.UIManager(window_size)
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_pos, button_size),
            text=button_text,
            manager=self.gui_manager)
        button.font = pygame.font.SysFont('serif', 25)
        self.font_t = pygame.font.SysFont('serif', 50)
        self.font = pygame.font.SysFont('serif', 25)
        self.title = self.font_t.render("Лабиринт", True, (255, 255, 255))
        self.text = self.font.render(
            f"{chr(7)} Цель игры - собрать как можно больше очков.\n"
            f"{chr(7)} Для перехода на следующий уровень вам надо собрать 30 монет.\n"
            f"{chr(7)} Остерегайтесь призрака! Чтобы его испугать, вы должны найти и активировать через пробел заряд.\n"
            f"{chr(7)} Управлять перемещением героя можно с помощью стрелок клавиатуры.",
            True, (255, 255, 255))
        self.image_name = image_menu

    def render(self, screen):
        screen.fill(pygame.Color('black'))
        self.gui_manager.draw_ui(screen)
        self.render_text(screen)
        self.render_image(screen)

    def render_text(self, screen):
        screen.blit(self.title, ((self.window_size[0] - self.title.get_width()) // 2, 100))
        screen.blit(self.text, (30, 200))

    def render_image(self, screen):
        img = pygame.image.load(self.image_name).convert()
        img.set_colorkey((0, 0, 0))
        rect = img.get_rect(
            center=(600, 500))
        screen.blit(img, rect)


class Game_Over(Menu):
    def __init__(self, window_size, scored):
        self.score = scored
        highscore = int(open("Highscore.txt").readline())
        super().__init__(window_size)
        self.text_s = self.font.render(f"You scored: {self.score}", True, (255, 255, 255))
        self.text_h = self.font.render(f"Your highscore: {highscore}", True, (255, 255, 255))
        print("game_over")

    def render(self, screen):
        screen.fill(pygame.Color('black'))
        self.gui_manager.draw_ui(screen)
        self.render_text(screen)

    def render_text(self, screen):
        screen.blit(self.text_s, ((self.window_size[0] - self.text_s.get_width()) // 2, self.window_size[1] // 2 - 110))
        screen.blit(self.text_h, ((self.window_size[0] - self.text_h.get_width()) // 2, self.window_size[1] // 2 - 60))


class pause:
    def __init__(self, window_size):
        button_size = (150, 50)
        button_pos = ((window_size[0] - button_size[0]) // 2, (window_size[1] - button_size[1]) // 2)
        button_text = 'Continue'
        self.gui_manager = pygame_gui.UIManager(window_size)
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_pos, button_size),
            text=button_text,
            manager=self.gui_manager)

    def render(self, screen):
        self.gui_manager.draw_ui(screen)


class score_panel:  # боковая панель, которая показывает во время игры сколько у игрока очков, зарядов и показывает его рекорд
    def __init__(self, c_score=0):
        pygame.font.init()
        self.font = pygame.font.SysFont('serif', 25)
        self.money = 0
        self.charges = 0
        self.c_score = c_score
        self.h_score = int(open("Highscore.txt").readline())
        self.text_m = self.font.render(f"money: {self.money}/30", True, (100, 100, 100))
        self.text_c = self.font.render(f"charge: {self.charges}", True, (100, 100, 100))
        self.text_s = self.font.render(f"Score: {self.c_score}", True, (100, 100, 100))
        self.text_h = self.font.render(f"High score: {self.h_score}", True, (100, 100, 100))

    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color('black'),
                         (1000, 0, 202, 1000))
        screen.blit(self.text_m, (1020, 10))
        screen.blit(self.text_c, (1020, 80))
        screen.blit(self.text_s, (1020, 150))
        screen.blit(self.text_h, (1020, 220))

    def update(self, money, charge):
        self.money = money
        self.charges = charge
        self.c_score = money * 100
        if self.c_score > self.h_score:
            self.h_score = self.c_score
            open("Highscore.txt", "w").write(str(self.h_score))

        self.text_m = self.font.render(f"money: {self.money}/30", True, (100, 100, 100))
        self.text_c = self.font.render(f"charge: {self.charges}", True, (100, 100, 100))
        self.text_s = self.font.render(f"Score: {self.c_score}", True, (100, 100, 100))
        self.text_h = self.font.render(f"High score: {self.h_score}", True, (100, 100, 100))


class Message:  # показывает сообщение о проигрыше или победе игрока
    def __init__(self, message, screen):
        self.font = pygame.font.SysFont('serif', 60)
        self.text = self.font.render(message, True, (255, 255, 255))
        screen.blit(self.text, (450, 450))
