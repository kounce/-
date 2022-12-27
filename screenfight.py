import sys
import os
import pygame

'''
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('ScreenFight')
'''


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.screen.load(fullname)
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
    string_title_rendered = font.render('Path to GLORY', 1, pygame.Color('white'))
    intro_title_rect = string_title_rendered.get_rect()
    intro_title_rect.top = 100
    intro_title_rect.x = 230
    screen.blit(string_title_rendered, intro_title_rect)
    color = 'white'  # цвет для кнопки
    # кнопка старт
    string_start_rendered = font.render('START', 1, pygame.Color(color))
    intro_start_rect = string_start_rendered.get_rect()
    intro_start_rect.top = 400
    intro_start_rect.x = 320
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # проверка, что курсор находится на кнопке или нет
            elif event.type == pygame.MOUSEMOTION and intro_start_rect.collidepoint(event.pos):
                color = 'yellow'
            elif event.type == pygame.MOUSEMOTION and not intro_start_rect.collidepoint(event.pos):
                color = 'white'
            # проверка, что игрок нажал именно на кнопку "start"
            if event.type == pygame.MOUSEBUTTONDOWN and intro_start_rect.collidepoint(event.pos):
                return  # начало игры
        string_start_rendered = font.render('START', 1, pygame.Color(color))
        intro_start_rect = string_start_rendered.get_rect()
        intro_start_rect.top = 400
        intro_start_rect.x = 320
        screen.blit(string_start_rendered, intro_start_rect)
        pygame.display.flip()
        clock.tick(fps)


class ScreenFight:
    def __init__(self, name, lvl, HP, KR, w, h):
        self.name = name
        self.lvl = lvl
        self.hp = HP
        self.kr = KR
        self.screen = pygame.Surface((800, 600))
        self.font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
        self.check_turn = False
        # установка цвета для отрисовки кнопок, чтобы игрок понял, на какой кнопке находится(во время своего хода)
        self.color = 'orange'
        self.w, self.h = w, h

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
        pygame.draw.rect(self.screen, pygame.Color('yellow'), (310, 485, 170, 35))

    def draw_KR(self):  # отрисовка какого то кр
        font = pygame.font.Font('data/MonsterFriend2Fore.otf', 25)
        string_rendered = font.render(self.kr + f'   ? / ?', 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 492
        intro_rect.x = 490
        screen.blit(string_rendered, intro_rect)

    def draw_fight_button(self):  # отрисовка кнопки файт
        pygame.draw.rect(self.screen, pygame.Color(self.color), (0, 530, 150, 70), 5)
        font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
        string_rendered = font.render('FIGHT', 1, pygame.Color(self.color))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 553
        intro_rect.x = 7
        screen.blit(string_rendered, intro_rect)

    def draw_act_button(self):  # отрисовка кнопки действия
        pygame.draw.rect(self.screen, pygame.Color(self.color), (210, 530, 150, 70), 5)
        font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
        string_rendered = font.render('ACT', 1, pygame.Color(self.color))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 553
        intro_rect.x = 240
        screen.blit(string_rendered, intro_rect)

    def draw_item_button(self):  # отрисовка кнопки предметов
        pygame.draw.rect(self.screen, pygame.Color(self.color), (430, 530, 150, 70), 5)
        font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
        string_rendered = font.render('ITEM', 1, pygame.Color(self.color))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 553
        intro_rect.x = 450
        screen.blit(string_rendered, intro_rect)

    def draw_mercy_button(self):  # отрисовка кнопки помиловать
        pygame.draw.rect(self.screen, pygame.Color(self.color), (650, 530, 150, 70), 5)
        font = pygame.font.Font('data/MonsterFriend2Fore.otf', 25)
        string_rendered = font.render('MERCY', 1, pygame.Color(self.color))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 553
        intro_rect.x = 660
        screen.blit(string_rendered, intro_rect)

    def player_field(self):  # отрисовка поля для перемещений игрока
        pygame.draw.rect(self.screen, pygame.Color('white'), ((width - self.w) // 2, 470 - self.h, self.w, self.h), 5)
        screen.blit(self.screen, (0, 0))

    def update_rect(self, w, h):  # смена размеров поля, где находится игрок
        pygame.draw.rect(self.screen, pygame.Color('black'), ((width - self.w) // 2, 470 - self.h, self.w, self.h))
        self.w, self.h = w, h

    def boss(self):  # отрисовка босса
        pass

    def player(self):  # отрисовка игрока
        pass

    def draw_all(self):  # отрисовка всего, что будет на экране
        self.player_field()
        self.draw_name()
        self.draw_lvl()
        self.draw_hp()
        self.draw_KR()
        if self.check_turn:  # проверка на ход игрока
            self.color = 'yellow'
        else:
            self.color = 'orange'
        self.draw_fight_button()
        self.draw_act_button()
        self.draw_item_button()
        self.draw_mercy_button()


'''
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
        screenfight.draw_all()
        pygame.display.flip()
        clock.tick(fps)
'''
