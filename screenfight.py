import sys
import os
import pygame

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('ScreenFight')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():  # функция для выхода на любом экране
    pygame.quit()
    sys.exit()


def start_screen():  # стартовый экран
    font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
    string_rendered = font.render('Path to GLORY', 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 100
    intro_rect.x = 230
    screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


class ScreenFight:
    def __init__(self, name, lvl, HP, KR, w, h):
        self.name = name
        self.lvl = lvl
        self.hp = HP
        self.kr = KR
        self.image = pygame.Surface((800, 600))
        self.rect = ((width - w) // 2, 470 - h, w, h)
        self.font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
        self.check_turn = False
        self.color = 'orange'

    def draw_name(self):  # отрисовка имени
        string_rendered = self.font.render(self.name, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 490
        intro_rect.x = 0
        screen.blit(string_rendered, intro_rect)

    def draw_lvl(self):  # отрисовка уровня
        string_rendered = self.font.render(self.lvl, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 490
        intro_rect.x = 120
        screen.blit(string_rendered, intro_rect)

    def draw_hp(self):  # отрисовка хп
        font = pygame.font.Font('data/MonsterFriend2Fore.otf', 25)
        string_rendered = font.render(self.hp, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 492
        intro_rect.x = 250
        screen.blit(string_rendered, intro_rect)
        pygame.draw.rect(self.image, pygame.Color('yellow'), (310, 485, 170, 35))

    def draw_KR(self):  # отрисовка какого то кр
        font = pygame.font.Font('data/MonsterFriend2Fore.otf', 25)
        string_rendered = font.render(self.kr + f'   ? / ?', 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 492
        intro_rect.x = 490
        screen.blit(string_rendered, intro_rect)

    def draw_fight_button(self):  # отрисовка кнопки файт
        pygame.draw.rect(self.image, pygame.Color(self.color), (0, 530, 150, 70), 5)
        font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
        string_rendered = font.render('FIGHT', 1, pygame.Color(self.color))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 553
        intro_rect.x = 7
        screen.blit(string_rendered, intro_rect)

    def draw_act_button(self):  # отрисовка кнопки действия
        pygame.draw.rect(self.image, pygame.Color(self.color), (210, 530, 150, 70), 5)
        font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
        string_rendered = font.render('ACT', 1, pygame.Color(self.color))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 553
        intro_rect.x = 240
        screen.blit(string_rendered, intro_rect)

    def draw_item_button(self):  # отрисовка кнопки предметов
        pygame.draw.rect(self.image, pygame.Color(self.color), (430, 530, 150, 70), 5)
        font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
        string_rendered = font.render('ITEM', 1, pygame.Color(self.color))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 553
        intro_rect.x = 450
        screen.blit(string_rendered, intro_rect)

    def draw_mercy_button(self):  # отрисовка кнопки помиловать
        pygame.draw.rect(self.image, pygame.Color(self.color), (650, 530, 150, 70), 5)
        font = pygame.font.Font('data/MonsterFriend2Fore.otf', 25)
        string_rendered = font.render('MERCY', 1, pygame.Color(self.color))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 553
        intro_rect.x = 660
        screen.blit(string_rendered, intro_rect)

    def boss(self):  # отрисовка босса
        pass

    def player(self):  # отрисовка игрока
        pass

    def field(self):  # отрисовка поля битвы и вызов всех функций для отрисовки худа
        pygame.draw.rect(self.image, pygame.Color('white'), self.rect, 5)
        screen.blit(self.image, (0, 0))
        self.draw_name()
        self.draw_lvl()
        self.draw_hp()
        self.draw_KR()
        if self.check_turn:
            self.color = 'yellow'
        else:
            self.color = 'orange'
        self.draw_fight_button()
        self.draw_act_button()
        self.draw_item_button()
        self.draw_mercy_button()


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    screenfight = ScreenFight('KIRA', 'LV 19', 'HP', 'KR', 400, 200)
    clock = pygame.time.Clock()
    fps = 60
    start_screen()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill((0, 0, 0))
        screenfight.field()
        pygame.display.flip()
        clock.tick(60)
