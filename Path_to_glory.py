# Проект Марченко Андрея Дмитриевича и Кармышакова Азата Ильнуровича
import math
import os
import sys

import pygame

# создание всего нужного для работы проекта
pygame.init()
pygame.mixer.init()
choosing_sound = pygame.mixer.Sound('data/choosing_sound_effect.wav')
attack_sound = pygame.mixer.Sound('data/attack_sound.wav')
complete_game_sound = pygame.mixer.Sound('data/complete_game_sound.wav')
win_sound = pygame.mixer.Sound('data/win_sound.wav')
loose_sound = pygame.mixer.Sound('data/loose_sound.wav')
escaping_sound = pygame.mixer.Sound('data/escaping_sound.wav')
unlocking_enemy_sound = pygame.mixer.Sound('data/unlocking_enemy_sound.wav')
fighting_menu_music = pygame.mixer.Sound('data/fighting_menu_music.wav')
frog_battle_music = pygame.mixer.Sound('data/frog_battle_music.wav')
demon_battle_music = pygame.mixer.Sound('data/demon_fighting_music.wav')
cat_battle_music = pygame.mixer.Sound('data/cat_fighting_music.wav')
SOUND_EFFECTS = [choosing_sound, attack_sound, complete_game_sound, win_sound,
                 loose_sound, escaping_sound, unlocking_enemy_sound]
GAME_MUSIC = [fighting_menu_music, frog_battle_music, demon_battle_music,
              cat_battle_music]
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Путь к славе')
invincibility_color = [pygame.Color('orange'), pygame.Color('purple')]
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
buttons_group = pygame.sprite.Group()
clock = pygame.time.Clock()
fps = 60
swap = True


class MusicButton(pygame.sprite.Sprite):
    """Класс кнопки, отключающей/включающей музыку"""

    def __init__(self):
        super().__init__(buttons_group)
        # загружаем фотки
        self.on = pygame.transform.scale(load_image('music_on.png', colorkey='black'), (30, 30))
        self.off = pygame.transform.scale(load_image('mute_music.png', colorkey='black'), (30, 30))
        self.images = [self.on, self.off]
        self.status = 0  # 0 - музыка играет, 1 - музыка не играет
        self.image = self.images[self.status]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 10, 10

    def change_status(self):
        self.status = self.status + 1 if self.status == 0 else 0  # меняем статус
        self.image = self.images[self.status]
        # для каждой музыки из списка всей музыки меняется громкость в соответствии со статусом
        if self.status == 0:
            for music in GAME_MUSIC:
                music.set_volume(1)
        else:
            for music in GAME_MUSIC:
                music.set_volume(0)


class SoundButton(pygame.sprite.Sprite):
    """Класс кнопки, отключающей/включающей звуковые эффекты"""

    def __init__(self):
        super().__init__(buttons_group)
        # загружаем фотки
        self.on = pygame.transform.scale(load_image('sound_on.png', colorkey='black'), (30, 30))
        self.off = pygame.transform.scale(load_image('mute_sound.png', colorkey='black'), (30, 30))
        self.images = [self.on, self.off]
        self.status = 0  # 0 - звуки играют, 1 - звуки не играют
        self.image = self.images[self.status]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 40, 10

    def change_status(self):
        self.status = self.status + 1 if self.status == 0 else 0  # меняем статус
        self.image = self.images[self.status]
        # для каждого звуки из списка всех звуковых эффектов меняется громкость в соответствии со статусом
        if self.status == 0:
            for music in SOUND_EFFECTS:
                music.set_volume(1)
        else:
            for music in SOUND_EFFECTS:
                music.set_volume(0)


def load_image(name, colorkey=None):
    """Функция загружает фотки и делает прозрачными, если надо"""
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
    font_en = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
    # название игры
    string_title_rendered = font_en.render('Path to GLORY', 1, pygame.Color('white'))
    intro_title_rect = string_title_rendered.get_rect()
    intro_title_rect.top = 100
    intro_title_rect.x = 230
    screen.blit(string_title_rendered, intro_title_rect)
    color_guide = 'white'  # цвет для кнопки guide
    # кнопка с руководством по управлению
    string_guide_render = font_en.render('GUIDE', 1, pygame.Color(color_guide))
    intro_guide_rect = string_guide_render.get_rect()
    intro_guide_rect.top = 450
    intro_guide_rect.x = 370
    color_start = 'white'  # цвет для кнопки start
    # кнопка старт
    string_start_rendered = font_en.render('START', 1, pygame.Color(color_start))
    intro_start_rect = string_start_rendered.get_rect()
    intro_start_rect.top = 400
    intro_start_rect.x = 320
    hide = False  # переменная, чтобы прятать руководство при повторном нажатии
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                # проверки, что курсор находится на кнопке или нет
                if intro_start_rect.collidepoint(event.pos):
                    color_start = 'yellow'
                if intro_guide_rect.collidepoint(event.pos):
                    color_guide = 'yellow'
                if not intro_start_rect.collidepoint(event.pos):
                    color_start = 'white'
                if not intro_guide_rect.collidepoint(event.pos):
                    color_guide = 'white'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if intro_start_rect.collidepoint(event.pos):  # проверка, что игрок нажал на кнопку start
                    choosing_sound.play()
                    return  # начало игры
                if intro_guide_rect.collidepoint(event.pos):  # проверка, что игрок нажал на кнопку guide:
                    choosing_sound.play()
                    guide_screen(hide)
                    hide = not hide
                pos_x, pos_y = event.pos
                if 10 <= pos_x <= 40 and 10 <= pos_y <= 40:
                    music_btn.change_status()
                if 50 <= pos_x <= 80 and 10 <= pos_y <= 40:
                    sound_btn.change_status()
        string_start_rendered = font_en.render('START', 1, pygame.Color(color_start))
        intro_start_rect = string_start_rendered.get_rect()
        intro_start_rect.top = 400
        intro_start_rect.x = 320
        screen.blit(string_start_rendered, intro_start_rect)
        string_guide_render = font_en.render('GUIDE', 1, pygame.Color(color_guide))
        intro_guide_rect = string_guide_render.get_rect()
        intro_guide_rect.top = 450
        intro_guide_rect.x = 330
        screen.blit(string_guide_render, intro_guide_rect)
        pygame.draw.rect(screen, 'black', (0, 0, 80, 50))
        buttons_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


def guide_screen(hide):
    if not hide:  # если первое нажатие, или после повторного, то рендерим руководство
        image = load_image('controls.png')
        image_rect = image.get_rect()
        screen.blit(image, (230, 220))
        font_ru = pygame.font.Font('data/game_font.otf', 30)
        string_control_render = font_ru.render('Передвижение', 1, pygame.Color('white'))
        intro_control_rect = string_control_render.get_rect()
        intro_control_rect.top = 190
        intro_control_rect.x = 275
        screen.blit(string_control_render, intro_control_rect)
        string_esc_render = font_ru.render('ESC - сбежать с боя', 1, pygame.Color('white'))
        intro_esc_rect = string_esc_render.get_rect()
        intro_esc_rect.top = 330
        intro_esc_rect.x = 240
        screen.blit(string_esc_render, intro_esc_rect)
        string_space_render = font_ru.render('SPACE - остановить полоску на экране атаки', 1, pygame.Color('white'))
        intro_space_rect = string_space_render.get_rect()
        intro_space_rect.top = 360
        intro_space_rect.x = 30
        screen.blit(string_space_render, intro_space_rect)
    else:  # если повторное, то закрашиваем черным квадратом руководство
        black_image = pygame.Surface((800, 300))
        black_image_rect = black_image.get_rect()
        black_image.fill((0, 0, 0))
        screen.blit(black_image, (50, 180))


def fighting_menu():
    # читаем инфу о том, пройдены враги или нет
    with open('data/enemies_completed.txt', newline='') as file:
        data = file.readlines()
        data = [int(x.strip()) for x in data]
        file.close()
    com1, com2, com3 = data
    enemy1 = pygame.sprite.Sprite()
    enemy1.image = load_image('first_enemy.png', colorkey=-1)  # фото первого врага
    enemy1.rect = enemy1.image.get_rect()
    if not com1:  # затемняем, если враг не пройден
        rect = enemy1.image.get_rect()
        image = pygame.Surface([rect.width, rect.height])
        image.set_alpha(230)
        enemy1.image.blit(image, (0, 0))
    enemy1.image = pygame.transform.scale(enemy1.image, (400, 400))
    enemy2 = pygame.sprite.Sprite()
    enemy2.image = load_image('second_enemy.png', colorkey=-1)  # фото второго врага
    enemy2.rect = enemy1.image.get_rect()
    if not com2:  # затемняем, если враг не пройден
        rect = enemy2.image.get_rect()
        image = pygame.Surface([rect.width, rect.height])
        image.set_alpha(230)
        enemy2.image.blit(image, (0, 0))
    enemy2.image = pygame.transform.scale(enemy2.image, (400, 400))
    enemy3 = pygame.sprite.Sprite()
    enemy3.image = load_image('third_enemy.png')  # фото третьего врага
    enemy3.rect = enemy1.image.get_rect()
    if not com3:  # затемняем, если враг не пройден
        rect = enemy3.image.get_rect()
        image = pygame.Surface([rect.width, rect.height])
        image.set_alpha(230)
        enemy3.image.blit(image, (0, 0))
    enemy3.image = pygame.transform.scale(enemy3.image, (400, 400))
    enemy_shown = 0
    enemies = [enemy1, enemy2, enemy3]

    font = pygame.font.Font('data/game_font.otf', 32)
    text = font.render("Выберите врага", True, 'white')
    text_x = 257
    text_y = 535
    running = True
    enemy1.rect.x, enemy1.rect.y = 200, 68
    enemy2.rect.x, enemy2.rect.y = 200, 68
    enemy3.rect.x, enemy3.rect.y = 200, 68
    fighting_menu_music.play(loops=-1)  # включаем музыку
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                # меняем отображаемого врага
                if event.key == 1073741904:
                    enemy_shown = enemy_shown - 1 if enemy_shown - 1 >= 0 else 2
                if event.key == 1073741903:
                    enemy_shown = enemy_shown + 1 if enemy_shown + 1 <= 2 else 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if (270 - 35 < x < 270 - 30 + 330 and
                            530 - 10 < y < 530 - 10 + 55):
                        if data[enemy_shown]:
                            # выбор врага и остановка работы окна
                            fighting_menu_music.stop()
                            choosing_sound.play()
                            running = False
                    if 730 < x < 770 and 275 < y < 325:  # меняем отображаемого врага
                        choosing_sound.play()
                        enemy_shown = enemy_shown + 1 if enemy_shown + 1 <= 2 else 0
                    if 30 < x < 70 and 275 < y < 325:  # меняем отображаемого врага
                        choosing_sound.play()
                        enemy_shown = enemy_shown - 1 if enemy_shown - 1 >= 0 else 2
                    # взаимодействие со звуком
                    pos_x, pos_y = event.pos
                    if 10 <= pos_x <= 40 and 10 <= pos_y <= 40:
                        music_btn.change_status()
                    if 50 <= pos_x <= 80 and 10 <= pos_y <= 40:
                        sound_btn.change_status()
        # отрисовка всего в соответствии с параметрами
        screen.fill('black')
        enemies_group = pygame.sprite.Group()
        enemies_group.add(enemies[enemy_shown])
        enemies_group.draw(screen)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (270 - 35 < mouse_x < 270 - 30 + 330 and
                530 - 10 < mouse_y < 530 - 10 + 55):
            text = font.render("Выберите врага", True, 'yellow')
        else:
            text = font.render("Выберите врага", True, 'white')
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, 'white', (270 - 35, 530 - 10,
                                           330, 55), 1)
        pygame.draw.rect(screen, 'white', (200, 68, 400, 400), 1)
        pygame.draw.polygon(screen, ('yellow' if 730 < mouse_x < 770 and 275 < mouse_y < 325 else
                                     'white'), ((730, 275), (770, 300), (730, 325)))
        pygame.draw.polygon(screen, ('yellow' if 30 < mouse_x < 70 and 275 < mouse_y < 325 else
                                     'white'), ((800 - 730, 275), (800 - 770, 300), (800 - 730, 325)))
        buttons_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    return enemy_shown  # возврат выбранного врага


class HUD:
    def __init__(self, hp):
        super().__init__()
        self.hp = hp
        self.screen = pygame.Surface((800, 135))
        self.font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
        # установка цвета для отрисовки кнопок, чтобы игрок понял, на какой кнопке находится(во время своего хода)
        self.color = 'orange'

    def draw_hp(self):  # отрисовка хп
        font = pygame.font.Font('data/MonsterFriend2Fore.otf', 25)
        string_rendered = font.render('HP', 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 522
        intro_rect.x = 50
        screen.blit(string_rendered, intro_rect)
        pygame.draw.rect(self.screen, pygame.Color('yellow'), (120, 30, self.hp * 4, 35))
        pygame.draw.rect(self.screen, pygame.Color('red'),
                         (520 - abs(self.hp - 100) * 4, 30, abs(self.hp - 100) * 4, 35))

    def draw_all(self):  # отрисовка всего, что будет на экране
        screen.blit(self.screen, (0, 485))
        self.draw_hp()


class Border(pygame.sprite.Sprite):  # класс для стенок поля
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        # боковые стенки поля
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface((5, y2 - y1))
            self.image.fill((255, 255, 255))
            self.rect = pygame.Rect(x1, y1, 5, y2 - y1)
        # верхние и нижние стенки поля
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface((x2 - x1, 5))
            self.image.fill((255, 255, 255))
            self.rect = pygame.Rect(x1, y1, x2 - x1, 5)


class Player(pygame.sprite.Sprite):  # класс игрока
    def __init__(self):
        super().__init__(all_sprites)
        # создание игрока в поле
        self.image = pygame.Surface((15, 15))
        self.image.fill(pygame.Color('orange'))
        self.rect = self.image.get_rect()
        self.rect.x = 393
        self.rect.y = 355
        self.invincibility = False
        # таймер для неуязвимости игрока после получения урона
        self.timer = 0
        # пауза для скиллчека, когда останавливается полоска и игрок увидел где остановилась полоска + сколько снял хп
        self.pause = 0
        # переменная, чтобы узнать прошло ли время, чтобы сменить цвет игрока во время неуязвимости
        self.change_color = 0
        # переменная, запускающая таймер "паузы" игры
        self.do_damage = False
        self.can_deal_damage = True

    # функции передвижения
    def move_right(self):
        self.rect = self.rect.move(3, 0)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.rect = self.rect.move(-3, 0)

    def move_left(self):
        self.rect = self.rect.move(-3, 0)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.rect = self.rect.move(3, 0)

    def move_up(self):
        self.rect = self.rect.move(0, -3)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.rect = self.rect.move(0, 3)

    def move_down(self):
        self.rect = self.rect.move(0, 3)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.rect = self.rect.move(0, -3)

    # функция для получения урона игроком
    def take_damage(self, health, invincibility):
        for particle in enemy.particles_list:
            if pygame.sprite.collide_mask(self, particle) and not invincibility:
                health -= enemy.damage
                hud.hp = health
                self.invincibility = True
                break

    # функция атаки противника
    def attack(self):
        if self.can_deal_damage:
            self.can_deal_damage = False
            attack_sound.play()
            damage = int(80 + 50 * (1 - math.fabs(skillcheck.rect.x - 385) / 400))
            enemy.get_hit(damage)
            self.do_damage = True
            self.set_back()

    def update(self):
        global swap
        if self.invincibility:
            self.timer += 1
            self.image.fill(invincibility_color[1])
            if self.timer >= 120:
                self.invincibility = False
                self.timer = 0
                self.change_color = 0
                self.image.fill(pygame.Color('orange'))
        if self.timer == self.change_color + 15:
            self.change_color += 15
            invincibility_color.reverse()
        if self.do_damage:  # если игрок наносит урон, запускается таймер на 150 итераций
            self.pause += 1
            if self.pause == 150:  # если 150 итераций, то производятся действия по продолжению игры
                all_sprites.remove(skillcheck)
                swap = not swap  # меняет направление движения полоски
                enemy.attack()
                all_sprites.add(player)
                self.pause = 0
                self.do_damage = False

    def set_back(self):
        self.rect.x = 393
        self.rect.y = 355


def load_tactic(file_name):
    """Функция загружает тактику боя для соперника"""
    import csv
    fullname = 'data/' + file_name
    with open(fullname, mode='r', encoding='utf8') as file:
        reader = csv.reader(file, delimiter=';', quotechar='"')
        data = [x for x in reader]
    res = {}
    for part in data:
        # завершающая "частица"
        if len(part) == 2:
            res[int(part[0])] = 'END'
            break
        # Частица в формате кадр: изображение, x, y, скорость по x, скорость по y, ускорение по x, ускорение по y,
        # colorkey
        # всё сразу переделывается в нужные типы
        if len(part) == 9:
            res[int(part[0])] = [load_image(part[1], colorkey=part[-1]),
                                 *[int(x) for x in part[2:6]], *[float(x) for x in part[6:8]]]
        if len(part) == 8:  # работает, если убирать фон не надо
            res[int(part[0])] = [load_image(part[1]), *[int(x) for x in part[2:6]], *[float(x) for x in part[6:8]]]
    # возвращает значения в виде библиотеки
    return res


def get_rect_from_sheet(sheet, columns, rows):
    """Возвращает рект исходя из sprite sheet"""
    rect = pygame.Rect(pygame.Rect(0, 0, sheet.get_width() // columns,
                                   sheet.get_height() // rows))
    return rect


def cut_sheet(sheet, rect, columns, rows):
    """Режет sprite sheet"""
    frames = []
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)))
    return frames


class SpriteSheet:
    """Класс упрощает работу с анимированными спрайтами"""

    def __init__(self, sheet, columns, rows, s):
        """Класс принимает sheet, кол-во колон, рядов и частоту обновления"""
        self.rect = get_rect_from_sheet(sheet, columns, rows)
        self.images = cut_sheet(sheet, self.rect, columns, rows)
        self.s, self.st, self.cur_frame = s, 0, 0

    def get_frame(self):
        return self.images[self.cur_frame]  # возвращает показываемый кадр

    def update(self):
        self.st += 1  # + счётчик кадров
        if self.st == self.s:  # если счётчик совпадает с частотой обновление, то кадр обновляется
            self.st = 0
            self.cur_frame += 1
            if self.cur_frame == len(self.images):  # зацикленность анимации
                self.cur_frame = 0

    def set_back(self):
        # возврат в начальное состояние
        self.cur_frame, self.st = 0, 0

    def get_rect(self):
        return self.rect

    def get_frames_num(self):
        # возврат суммы кадром
        return len(self.images) * self.s

    def get_last_frame(self):
        # возврат последнего кадра
        return self.images[-1]


class Particle(pygame.sprite.Sprite):
    """Класс частиц"""

    def __init__(self, im, x, y, vx, vy, ax, ay):
        """На вход принимаются изображение, x, y, скорость по x, скорость по y, ускорение по x, ускорение по y"""
        # порядок записи сверху соответствует расположению переменных при принятии
        super().__init__(all_sprites)
        self.image, self.rect = im, im.get_rect()  # изображение
        self.mask = pygame.mask.from_surface(self.image)  # маска
        self.x, self.y = x, y  # позиция
        self.vx, self.vy = vx, vy  # скорость по обеим осям
        self.ax, self.ay = ax, ay  # ускорение по обеим осям

    def update(self):
        t = 60
        """Меняет скорость в соответствии с ускорением и положение"""
        self.vx, self.vy = self.vx + self.ax, self.vy + self.ay
        # значения положения созданы отдельно, чтобы они могли иметь вид вещественных чисел, рект так не умеет (вроде)
        self.x, self.y = self.x + self.vx / t, self.y + self.vy / t
        self.rect.x, self.rect.y = int(self.x), int(self.y)


class HealthStripe(pygame.sprite.Sprite):
    def __init__(self, max_health, rn_health, bf_health):
        super().__init__(all_sprites)
        self.max_health, self.rn_health, self.bf_health = max_health, rn_health, bf_health
        self.start = int(bf_health / max_health * 200)
        self.end = int(rn_health / max_health * 200) if int(rn_health / max_health * 200) > 0 else 0
        self.rn = self.start
        self.move = (self.start - self.end) / 60
        self.steps = 150
        self.image = pygame.Surface([200, 40])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 300, 50
        self.image.fill('yellow')
        pygame.draw.rect(self.image, 'red', (int(self.rn), 0, 200, 40))

    def update(self):
        if 60 <= self.steps <= 120:
            self.rn -= self.move
            if self.rn < 0:
                self.rn = 0
            self.image.fill('yellow')
            pygame.draw.rect(self.image, 'red', (int(self.rn), 0, 200, 40))
        self.steps -= 1
        if self.steps == 0:
            self.kill()


class AnimatedEnemy(pygame.sprite.Sprite):
    """Базовый класс для всех врагов"""

    def __init__(self, sheets, x, y, width, height):
        """На вход принимаются sprite sheets, его ширина, его высота,
         х, y, количество кадров для изменения изображения, высота врага, ширина врага"""
        super().__init__(all_sprites)
        self.particles = pygame.sprite.Group()  # тут будут храниться частицы, создающиеся для атаки врага
        # создаем sprite sheet для каждого состояния врага
        self.waiting_sheet = sheets[0]
        self.attacking_sheet = sheets[1]
        self.dying_sheet = sheets[2]
        self.sheet = self.waiting_sheet
        self.statuses = ['waiting', 'attacking', 'dying']  # статусы
        self.status = 0  # изначально враг ожидает
        self.x, self.y = x, y  # расположение
        self.width, self.height = width, height
        self.image = self.sheet.get_frame()  # задаем изображение
        self.image = pygame.transform.scale(self.image, (self.width, self.height))  # подстраиваем размер
        self.rect = self.waiting_sheet.get_rect()  # задаем рект
        self.rect = self.rect.move(x, y)
        self.ending_frames = 0
        self.ending_frames_sum = self.dying_sheet.get_frames_num() + 180  # кол-во кадров при анимации смерти
        self.dying_sheet_frames_num = self.dying_sheet.get_frames_num()  # номер кадра, когда пора выводить текст
        self.health = 0

    def update(self):
        self.sheet.update()
        self.image = self.sheet.get_frame()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # обновляем все значения для атакующей анимации, если это требуется
        if self.statuses[self.status] == 'attacking':
            if self.sheet != self.attacking_sheet:
                self.sheet.set_back()
                self.sheet = self.attacking_sheet
                self.rect = self.sheet.get_rect()
                self.rect = self.rect.move(self.x, self.y)
                self.image = self.sheet.get_frame()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # обновляем все значения для умирающей анимации, если это требуется
        if self.statuses[self.status] == 'dying':
            if self.sheet != self.dying_sheet:
                self.sheet.set_back()
                self.sheet = self.dying_sheet
                self.rect = self.sheet.get_rect()
                self.rect = self.rect.move(self.x, self.y)
                self.image = self.sheet.get_frame()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # обновляем все значения для ожидающей анимации, если это требуется
        if self.statuses[self.status] == 'waiting':
            if self.sheet != self.waiting_sheet:
                self.sheet.set_back()
                self.sheet = self.waiting_sheet
                self.rect = self.sheet.get_rect()
                self.rect = self.rect.move(self.x, self.y)
                self.image = self.sheet.get_frame()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))

    # функции ниже взаимодействуют со статусом врага
    def attack(self):
        self.status = 1

    def wait(self):
        # запускается атака игрока и ставится ожидающий статус
        global skillcheck
        self.status = 0
        skillcheck = SkillCheck()
        skillcheck.swap_sides(swap)

    def die(self):
        self.status = 2

    def is_attacking(self):
        return True if self.status == 1 else False

    def dying_animation(self, enemies_won):
        # отрисовка врага при смерти
        if self.status == 2:
            self.ending_frames += 1  # подсчет кадров
            if self.ending_frames == self.dying_sheet.get_frames_num():
                # если пора, то рисуется текст
                self.dying_sheet = SpriteSheet(self.dying_sheet.get_last_frame(), 1, 1, 180)
                font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
                font1 = pygame.font.Font('data/MonsterFriend2Fore.otf', 15)
                ending_text = font.render('you won!', 1, pygame.Color('white'))
                e_w_t = font1.render(f'enemies won: {enemies_won}', 1, pygame.Color('white'))  # подсчет убитых врагов
                # отрисовка
                sprite = pygame.sprite.Sprite(all_sprites)
                sprite.image = ending_text
                sprite.rect = ending_text.get_rect()
                sprite.rect.x, sprite.rect.y = 400 - (sprite.rect.width // 2), (210 - sprite.rect.height) // 2
                e_w = pygame.sprite.Sprite(all_sprites)
                e_w.image = e_w_t
                e_w.rect = e_w_t.get_rect()
                e_w.rect.x, e_w.rect.y = 400 - (e_w.rect.width // 2), (150 - e_w.rect.height) // 2
            if self.ending_frames == self.ending_frames_sum:  # возвращает True, если пора завершать бой
                return True
            else:
                return False

    def get_hit(self, n):
        if self.hp - n > 0:
            HealthStripe(self.max_hp, self.hp - n, self.hp)
        self.hp -= n


class Frog(AnimatedEnemy):
    """Класс первого врага - лягушки"""

    def __init__(self, sheets, x, y, width, height):
        """На вход принимаются sprite sheets, х, y, высота врага, ширина врага"""
        # все значения передаются в базовый класс
        super().__init__(sheets, x, y, width, height)
        self.max_hp = self.hp = 400
        self.damage = 5
        self.particles_list = []  # список атакующих частиц
        self.enemy_name = 'frog'  # названия врага, для взаимодействия с файлами игры
        self.attacking_count = 0  # подсчёт кадров, чтобы создавать частицы по счёту
        self.tactic = None  # тактика атаки
        self.past_attack = 0  # переменная, чтобы атаки не повторялись слишком часто
        self.type = 'Frog'

    def move(self):
        """Функция выбирает случайную тактику из возможных и использует ее для атаки"""
        if self.attacking_count == 0:  # если это первый кадр, то выбирается случайная тактика
            from random import choice
            attack = choice([int(x) for x in range(1, 5) if x != self.past_attack])
            self.past_attack = attack
            self.tactic = load_tactic(self.enemy_name + '_attack_' + str(attack) + '.txt')
        try:
            self.attacking_count += 1  # считаем кадры
            # если кадр не последний, то успешно создается новая частица
            im, x, y, vx, vy, ax, ay = self.tactic[self.attacking_count]
            # добавляется в группы и списки частиц
            self.particles_list.append(Particle(im, x, y, vx, vy, ax, ay))
            self.particles.add(self.particles_list[-1])
        except KeyError:
            # срабатывает, если по счету нет нужных частиц
            pass
        except ValueError:
            # срабатывает, если сейчас по счёту последний кадр
            # уничтожаются все спрайты, очищаются списки, тактика и лягушка переходит в ожидание
            self.attacking_count = 0
            self.tactic = None
            self.wait()
            for part in self.particles_list:
                part.kill()
            self.particles_list = []


class Demon(AnimatedEnemy):
    """Класс второго врага - демона"""

    def __init__(self, sheets, x, y, width, height):
        """На вход принимаются sprite sheets, х, y, высота врага, ширина врага"""
        # все значения передаются в базовый класс
        super().__init__(sheets, x, y, width, height)
        self.max_hp = self.hp = 800
        self.damage = 10
        self.particles_list = []  # список атакующих частиц
        self.enemy_name = 'demon'  # названия врага, для взаимодействия с файлами игры
        self.attacking_count = 0  # подсчёт кадров, чтобы создавать частицы по счёту
        self.tactic = None  # тактика атаки
        self.past_attack = 0  # переменная, чтобы атаки не повторялись слишком часто
        self.type = 'Demon'

    def move(self):
        """Функция выбирает случайную тактику из возможных и использует ее для атаки"""
        if self.attacking_count == 0:  # если это первый кадр, то выбирается случайная тактика
            from random import choice, randint
            attack = choice([int(x) for x in range(1, 7) if x != self.past_attack])
            self.past_attack = attack
            if attack > 4:
                self.tactic = {}
                for i in range(1, 51):
                    w = randint(1, 4)
                    if w == 1:
                        self.tactic[60 + i * 20] = [load_image('fireball.png', colorkey='white'),
                                                    100, randint(250, 450), 70, 0, 2, 0]
                    if w == 2:
                        self.tactic[60 + i * 20] = [load_image('fireball.png', colorkey='white'),
                                                    randint(200, 580), 120, 0, 70, 0, 2]
                    if w == 3:
                        self.tactic[60 + i * 20] = [load_image('fireball.png', colorkey='white'),
                                                    680, randint(250, 450), -70, 0, -2, 0]
                    if w == 4:
                        self.tactic[60 + i * 20] = [load_image('fireball.png', colorkey='white'),
                                                    randint(200, 580), 550, 0, -70, 0, -2]
                    self.tactic[1300] = 'END'
            else:
                self.tactic = load_tactic(self.enemy_name + '_attack_' + str(attack) + '.txt')
        try:
            self.attacking_count += 1  # считаем кадры
            # если кадр не последний, то успешно создается новая частица
            im, x, y, vx, vy, ax, ay = self.tactic[self.attacking_count]
            # добавляется в группы и списки частиц
            self.particles_list.append(Particle(im, x, y, vx, vy, ax, ay))
            self.particles.add(self.particles_list[-1])
        except KeyError:
            # срабатывает, если по счету нет нужных частиц
            pass
        except ValueError:
            # срабатывает, если сейчас по счёту последний кадр
            # уничтожаются все спрайты, очищаются списки, тактика и лягушка переходит в ожидание
            self.attacking_count = 0
            self.tactic = None
            self.wait()
            for part in self.particles_list:
                part.kill()
            self.particles_list = []


class Cat(AnimatedEnemy):
    """Класс третьего врага - кота"""

    def __init__(self, sheets, x, y, width, height):
        """На вход принимаются sprite sheets, х, y, высота врага, ширина врага"""
        # все значения передаются в базовый класс
        super().__init__(sheets, x, y, width, height)
        self.max_hp = self.hp = 1200
        self.damage = 15
        self.particles_list = []  # список атакующих частиц
        self.enemy_name = 'cat'  # названия врага, для взаимодействия с файлами игры
        self.attacking_count = 0  # подсчёт кадров, чтобы создавать частицы по счёту
        self.tactic = None  # тактика атаки
        self.past_attack = 0  # переменная, чтобы атаки не повторялись слишком часто
        self.type = 'Cat'

    def move(self):
        """Функция выбирает случайную тактику из возможных и использует ее для атаки"""
        if self.attacking_count == 0:  # если это первый кадр, то выбирается случайная тактика
            from random import choice, randint
            attack = choice([int(x) for x in range(1, 6) if x != self.past_attack])
            self.past_attack = attack
            # куча разных тактик, требующих рандомное генерирование
            if attack == 1:
                self.tactic = {}
                for i in range(1, 51):
                    w = randint(1, 4)
                    c = choice(['red', 'blue', 'green', 'grey', 'purple'])
                    if w == 1:
                        self.tactic[60 + i * 10] = [load_image(f'cotton_{c}_ball.png', colorkey='black'),
                                                    100, randint(250, 440), 70, 0, 4, 0]
                    if w == 2:
                        self.tactic[60 + i * 10] = [load_image(f'cotton_{c}_ball.png', colorkey='black'),
                                                    randint(200, 570), 120, 0, 70, 0, 4]
                    if w == 3:
                        self.tactic[60 + i * 10] = [load_image(f'cotton_{c}_ball.png', colorkey='black'),
                                                    680, randint(250, 440), -70, 0, -4, 0]
                    if w == 4:
                        self.tactic[60 + i * 10] = [load_image(f'cotton_{c}_ball.png', colorkey='black'),
                                                    randint(200, 570), 550, 0, -70, 0, -4]
                self.tactic[250 + 50 * 10] = 'END'
            elif attack == 2:
                self.tactic = {}
                self.tactic[1] = [load_image(f'leftcatwall.png'),
                                  200, 250, 0, 0, 0, 0]
                self.tactic[2] = [load_image(f'rightcatwall.png'),
                                  455, 250, 0, 0, 0, 0]
                s = 0
                for i in range(1, 21):
                    w = choice([int(x) for x in range(1, 4) if x != s])
                    c = choice(['red', 'blue', 'green', 'grey', 'purple'])
                    if w == 1:
                        self.tactic[60 + i * 30] = [load_image(f'cotton_{c}_ball.png', colorkey='black'),
                                                    350, 100, 0, 80, 0, 2]
                    if w == 2:
                        self.tactic[60 + i * 30] = [load_image(f'cotton_{c}_ball.png', colorkey='black'),
                                                    385, 100, 0, 80, 0, 2]
                    if w == 3:
                        self.tactic[60 + i * 30] = [load_image(f'cotton_{c}_ball.png', colorkey='black'),
                                                    420, 100, 0, 80, 0, 2]
                    s = w
                self.tactic[830] = 'END'
            elif attack == 3:
                self.tactic = {}
                for i in range(1, 61):
                    w = randint(1, 2)
                    c = choice(['red', 'blue', 'green', 'grey', 'purple'])
                    if w == 1:
                        self.tactic[60 + i * 10] = [load_image(f'cotton_{c}_ball.png', colorkey='black'),
                                                    20, 440, randint(40, 180), -300, 0, 3]
                    if w == 2:
                        self.tactic[60 + i * 10] = [load_image(f'cotton_{c}_ball.png', colorkey='black'),
                                                    750, 440, -randint(40, 180), -300, 0, 3]
                self.tactic[360 + 60 * 10] = 'END'
            elif attack == 4:
                self.tactic = {}
                self.tactic[1] = [load_image(f'waves.png', colorkey=(3, 3, 3)),
                                  800, 250, -200, 0, 0, 0]
                for i in range(1, 61):
                    w = randint(1, 2)
                    c = choice(['red', 'blue', 'green', 'grey', 'purple'])
                    if w == 1:
                        self.tactic[60 + i * 30] = [load_image(f'cotton_{c}_ball.png', colorkey='black'),
                                                    randint(200, 570), 120, 0, 80, 0, 3]
                    if w == 2:
                        self.tactic[60 + i * 30] = [load_image(f'cotton_{c}_ball.png', colorkey='black'),
                                                    randint(200, 570), 600, 0, -80, 0, -3]
                self.tactic[360 + 60 * 30] = 'END'
            elif attack == 5:
                self.tactic = {}
                player.rect.x = 500
                player.rect.y = 325
                self.tactic[1] = [load_image(f'cotton_red_ball.png', colorkey='black'),
                                  385, 345, 0, 0, 0, 0]
                self.tactic[2] = [load_image(f'square_borders.png', colorkey='black'),
                                  202, 252, 0, 0, 0, 0]
                y_r = [1, 0.8, 0.6, 0.4, 0.2, 0, -0.2, -0.4, -0.6, -0.8, -1]
                y = sorted(y_r)[1:]
                x_r = [0, 0.2, 0.4, 0.6, 0.8, 1, 0.8, 0.6, 0.4, 0.2, 0]
                x = [-e for e in x_r][1:]
                for i in range(3):
                    for j in range(11):
                        c = choice(['red', 'blue', 'green', 'grey', 'purple'])
                        self.tactic[i * 20 * 10 + j * 10 + 60] = [load_image(f'cotton_{c}_ball.png', colorkey='black'),
                                                                  385, 345, 80 * x_r[j], 80 * y_r[j], 0, 0]
                    for j in range(9):
                        c = choice(['red', 'blue', 'green', 'grey', 'purple'])
                        self.tactic[i * 20 * 10 +
                                    (j + 11) * 10 + 60] = [load_image(f'cotton_{c}_ball.png', colorkey='black'),
                                                           385, 345, 80 * x[j], 80 * y[j], 0, 0]
                self.tactic[60 * 10 + 260] = 'END'
        try:
            self.attacking_count += 1  # считаем кадры
            # если кадр не последний, то успешно создается новая частица
            im, x, y, vx, vy, ax, ay = self.tactic[self.attacking_count]
            # добавляется в группы и списки частиц
            self.particles_list.append(Particle(im, x, y, vx, vy, ax, ay))
            self.particles.add(self.particles_list[-1])
        except KeyError:
            # срабатывает, если по счету нет нужных частиц
            pass
        except ValueError:
            # срабатывает, если сейчас по счёту последний кадр
            # уничтожаются все спрайты, очищаются списки, тактика и лягушка переходит в ожидание
            self.attacking_count = 0
            self.tactic = None
            self.wait()
            for part in self.particles_list:
                part.kill()
            self.particles_list = []


class SkillCheck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((20, 200))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = -15
        self.rect.y = 262
        self.left_to_right = True  # переменная, для определения направления движения полоски

    def draw_skillcheck(self):
        pygame.draw.ellipse(screen, (190, 245, 116), (5, 255, 790, 215), 10)
        # красный левый сегмент
        pygame.draw.line(screen, pygame.Color('red'), (73, 311), (73, 413), 3)
        pygame.draw.line(screen, pygame.Color('red'), (93, 331), (113, 331), 4)
        pygame.draw.line(screen, pygame.Color('red'), (137, 331), (157, 331), 4)
        pygame.draw.line(screen, pygame.Color('red'), (182, 331), (202, 331), 4)
        pygame.draw.line(screen, pygame.Color('red'), (113, 361), (133, 361), 4)
        pygame.draw.line(screen, pygame.Color('red'), (157, 361), (177, 361), 4)
        pygame.draw.line(screen, pygame.Color('red'), (93, 393), (113, 393), 4)
        pygame.draw.line(screen, pygame.Color('red'), (137, 393), (157, 393), 4)
        pygame.draw.line(screen, pygame.Color('red'), (182, 393), (202, 393), 4)
        # красный правый сегмент
        pygame.draw.line(screen, pygame.Color('red'), (726, 311), (726, 413), 3)
        pygame.draw.line(screen, pygame.Color('red'), (706, 331), (687, 331), 4)
        pygame.draw.line(screen, pygame.Color('red'), (662, 331), (642, 331), 4)
        pygame.draw.line(screen, pygame.Color('red'), (596, 331), (616, 331), 4)
        pygame.draw.line(screen, pygame.Color('red'), (686, 361), (666, 361), 4)
        pygame.draw.line(screen, pygame.Color('red'), (642, 361), (622, 361), 4)
        pygame.draw.line(screen, pygame.Color('red'), (706, 393), (686, 393), 4)
        pygame.draw.line(screen, pygame.Color('red'), (662, 393), (642, 393), 4)
        pygame.draw.line(screen, pygame.Color('red'), (616, 393), (596, 393), 4)
        # желтый левый сегмент
        pygame.draw.line(screen, pygame.Color('yellow'), (222, 276), (222, 448), 8)
        pygame.draw.line(screen, pygame.Color('yellow'), (242, 306), (252, 306), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (252, 334), (272, 334), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (252, 362), (272, 362), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (252, 390), (272, 390), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (242, 418), (252, 418), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (296, 306), (306, 306), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (306, 334), (326, 334), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (306, 362), (326, 362), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (306, 390), (326, 390), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (296, 418), (306, 418), 4)
        # желтый правый сегмент
        pygame.draw.line(screen, pygame.Color('yellow'), (576, 276), (576, 448), 8)
        pygame.draw.line(screen, pygame.Color('yellow'), (556, 306), (546, 306), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (546, 334), (526, 334), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (546, 362), (526, 362), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (546, 390), (526, 390), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (556, 418), (546, 418), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (502, 306), (492, 306), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (492, 334), (472, 334), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (492, 362), (472, 362), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (492, 390), (472, 390), 4)
        pygame.draw.line(screen, pygame.Color('yellow'), (502, 418), (492, 418), 4)
        # зеленый
        pygame.draw.line(screen, (190, 245, 116), (356, 266), (356, 458), 10)
        pygame.draw.line(screen, (0, 153, 0), (366, 270), (366, 454), 10)
        pygame.draw.line(screen, (0, 153, 0), (366, 272), (432, 272), 10)
        pygame.draw.line(screen, (0, 153, 0), (366, 452), (432, 452), 10)
        pygame.draw.line(screen, (0, 153, 0), (432, 270), (432, 454), 10)
        pygame.draw.line(screen, (190, 245, 116), (442, 266), (442, 458), 10)

    def move_left_to_right(self):
        self.rect = self.rect.move(5, 0)

    def move_right_to_left(self):
        self.rect = self.rect.move(-5, 0)

    def swap_sides(self, swap):
        self.left_to_right = swap
        if self.left_to_right:
            self.rect.x = -15
        else:
            self.rect.x = 795


def escape_screen():
    """Функция рисует окно, с соответствующей информацией"""
    font = pygame.font.Font('data/MonsterFriend2Fore.otf', 40)
    escaping_text = font.render('you ran away...', 1, pygame.Color('white'))
    rect = escaping_text.get_rect()
    rect.x, rect.y = 400 - (rect.width // 2), 300 - (rect.height // 2)
    sc = 300
    running = True
    escaping_sound.play()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = event.pos
                if 10 <= pos_x <= 40 and 10 <= pos_y <= 40:
                    music_btn.change_status()
                if 50 <= pos_x <= 80 and 10 <= pos_y <= 40:
                    sound_btn.change_status()
        screen.fill('black')
        screen.blit(escaping_text, rect)
        if sc == 0:
            running = False
        sc -= 1
        buttons_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


def player_lost_screen():
    """Функция рисует окно, с соответствующей информацией"""
    font = pygame.font.Font('data/MonsterFriend2Fore.otf', 40)
    loosing_text = font.render('you died...', 1, pygame.Color('red'))
    rect = loosing_text.get_rect()
    rect.x, rect.y = 400 - (rect.width // 2), 300 - (rect.height // 2)
    sc = 300
    running = True
    loose_sound.play()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = event.pos
                if 10 <= pos_x <= 40 and 10 <= pos_y <= 40:
                    music_btn.change_status()
                if 50 <= pos_x <= 80 and 10 <= pos_y <= 40:
                    sound_btn.change_status()
        screen.fill('black')
        screen.blit(loosing_text, rect)
        if sc == 0:
            running = False
        sc -= 1
        buttons_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


def unlocking_new_enemy_screen():
    """Функция рисует окно, с соответствующей информацией"""
    font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
    unlock_text = font.render('you unlocked new enemy!', 1, pygame.Color('yellow'))
    rect = unlock_text.get_rect()
    rect.x, rect.y = 400 - (rect.width // 2), 300 - (rect.height // 2)
    sc = 300
    running = True
    unlocking_enemy_sound.play()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = event.pos
                if 10 <= pos_x <= 40 and 10 <= pos_y <= 40:
                    music_btn.change_status()
                if 50 <= pos_x <= 80 and 10 <= pos_y <= 40:
                    sound_btn.change_status()
        screen.fill('black')
        screen.blit(unlock_text, rect)
        if sc == 0:
            running = False
        sc -= 1
        buttons_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


def game_completed_screen():
    """Функция рисует окно, с соответствующей информацией"""
    font_c = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
    font_t = pygame.font.Font('data/MonsterFriend2Fore.otf', 20)
    complete_text = font_c.render('you completed the game!', 1, pygame.Color('white'))
    thanks_text = font_t.render('thank you for playing', 1, pygame.Color('white'))
    rect_c = complete_text.get_rect()
    rect_c.x, rect_c.y = 400 - (rect_c.width // 2), 300 - (rect_c.height // 2)
    rect_t = thanks_text.get_rect()
    rect_t.x, rect_t.y = 400 - (rect_t.width // 2), 330 - (rect_t.height // 2)
    sc = 500
    running = True
    complete_game_sound.play()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = event.pos
                if 10 <= pos_x <= 40 and 10 <= pos_y <= 40:
                    music_btn.change_status()
                if 50 <= pos_x <= 80 and 10 <= pos_y <= 40:
                    sound_btn.change_status()
        screen.fill('black')
        screen.blit(complete_text, rect_c)
        screen.blit(thanks_text, rect_t)
        if sc == 0:
            running = False
        sc -= 1
        buttons_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


def battle_screen(sound):
    result = False
    key_a = False
    key_d = False
    key_w = False
    key_s = False
    running = True
    enemies_won = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                # если нажата клавиша, то игрок движется
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    key_a = True
                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    key_d = True
                if event.key in (pygame.K_w, pygame.K_UP):
                    key_w = True
                if event.key in (pygame.K_s, pygame.K_DOWN):
                    key_s = True
                # если пробел нажат, и в данный момент враг ожидает хода игрока, то игрок атакует
                if event.key == pygame.K_SPACE and enemy.status == 0:
                    player.attack()
                if event.key == pygame.K_ESCAPE:
                    sound.stop()
                    result = 'escaped'
                    running = False
            if event.type == pygame.KEYUP:
                # если клавиша отжата, то движение останавливается
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    key_a = False
                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    key_d = False
                if event.key in (pygame.K_w, pygame.K_UP):
                    key_w = False
                if event.key in (pygame.K_s, pygame.K_DOWN):
                    key_s = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = event.pos
                if 10 <= pos_x <= 40 and 10 <= pos_y <= 40:
                    music_btn.change_status()
                if 50 <= pos_x <= 80 and 10 <= pos_y <= 40:
                    sound_btn.change_status()
        screen.fill((0, 0, 0))
        if enemy.is_attacking():
            player.can_deal_damage = True
            enemy.move()
            player.take_damage(hud.hp, player.invincibility)
        if key_a:
            player.move_left()
        if key_d:
            player.move_right()
        if key_w:
            player.move_up()
        if key_s:
            player.move_down()
        if hud.hp <= 0:
            player.can_deal_damage = True
            sound.stop()
            result = 'died'
            running = False
        if enemy.hp <= 0:
            player.can_deal_damage = True
            sound.stop()
            skillcheck.kill()
            enemy.die()
            if enemy.ending_frames == 1:
                # обновляется инфа о врагах
                with open('data/enemies_won.txt', 'r', newline='') as file:
                    data = int(file.read())
                    enemies_won = data + 1
                    file.close()
                with open('data/enemies_won.txt', 'w', newline='') as file:
                    file.write(str(enemies_won))
                    file.close()
                with open('data/enemies_completed.txt', 'r', newline='') as file2:
                    data = file2.readlines()
                    data = [int(x.strip()) for x in data]
                    file2.close()
                com1, com2, com3 = data
                with open('data/enemies_completed.txt', 'w', newline='') as file1:
                    if enemy.type == 'Frog':
                        if not com2:
                            result = 'won_un'
                        file1.write(f'1\n1\n{com3}')
                    elif enemy.type == 'Demon':
                        if not com3:
                            result = 'won_un'
                        file1.write(f'1\n{com2}\n1')
                    else:
                        result = 'completed'
                        file1.write(f'1\n1\n1')
                    file1.close()
            if enemy.ending_frames == enemy.dying_sheet_frames_num:
                win_sound.play()
            if enemy.dying_animation(enemies_won):
                sound.stop()
                running = False
        if enemy.status == 0:
            # когда противник ждет хода игрока, убирается поле битвы и добавляется большое для атаки игрока
            all_sprites.remove(border_top_fight)
            all_sprites.remove(border_bottom_fight)
            all_sprites.remove(border_left_fight)
            all_sprites.remove(border_right_fight)
            all_sprites.add(border_top)
            all_sprites.add(border_bottom)
            all_sprites.add(border_left)
            all_sprites.add(border_right)
            all_sprites.remove(player)
            player.update()
            skillcheck.draw_skillcheck()
            if skillcheck.left_to_right and skillcheck.rect.x <= 775 and not player.do_damage:
                skillcheck.move_left_to_right()
                if skillcheck.rect.x == 780:
                    player.attack()
            elif not skillcheck.left_to_right and skillcheck.rect.x >= 5 and not player.do_damage:
                skillcheck.move_right_to_left()
                if skillcheck.rect.x == 0:
                    player.attack()
        if enemy.status == 1:
            # если противник атакует, то удаляется поле для атаки игрока, и добавляется поле для битвы
            player.can_deal_damage = True
            all_sprites.add(border_top_fight)
            all_sprites.add(border_bottom_fight)
            all_sprites.add(border_left_fight)
            all_sprites.add(border_right_fight)
            all_sprites.remove(border_top)
            all_sprites.remove(border_bottom)
            all_sprites.remove(border_left)
            all_sprites.remove(border_right)
        hud.draw_all()
        all_sprites.draw(screen)
        all_sprites.update()
        buttons_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    return result  # возвращает результат боя


# загружаем все спрайты
WAITING_FROG = SpriteSheet(load_image('waiting_frog.png', colorkey=-1), 14, 1, 10)
ATTACKING_FROG = SpriteSheet(load_image('attacking_frog.png', colorkey=-1), 14, 1, 10)
DYING_FROG = SpriteSheet(load_image('dying_frog.png', colorkey=-1), 14, 1, 10)
WAITING_DEMON = SpriteSheet(load_image('waiting_demon.png', colorkey=-1), 6, 1, 6)
ATTACKING_DEMON = SpriteSheet(load_image('attacking_demon.png', colorkey=-1), 15, 1, 6)
DYING_DEMON = SpriteSheet(load_image('dying_demon.png', colorkey=-1), 22, 1, 6)
ATTACKING_CAT = WAITING_CAT = SpriteSheet(load_image('waiting_cat.png', colorkey=-1), 57, 1, 4)
DYING_CAT = SpriteSheet(load_image('dying_cat.png', colorkey=-1), 46, 1, 4)
# кнопки взаимодействия со звуком
sound_btn = SoundButton()
music_btn = MusicButton()
# начало работы
start_screen()
while True:  # основной цикл
    chosen_enemy = fighting_menu()  # выбор врага
    # создание соответствующего врага и выбор музыки
    if chosen_enemy == 0:
        enemy = Frog([WAITING_FROG,
                      ATTACKING_FROG,
                      DYING_FROG], 320, 150, 160, 100)
        music = frog_battle_music
    elif chosen_enemy == 1:
        enemy = Demon([WAITING_DEMON,
                       ATTACKING_DEMON,
                       DYING_DEMON], 200, 28, 400, 222)
        music = demon_battle_music
    elif chosen_enemy == 2:
        enemy = Cat([WAITING_CAT,
                     ATTACKING_CAT,
                     DYING_CAT], 250, 90, 300, 160)
        music = cat_battle_music
    # подготовка к бою
    player = Player()
    skillcheck = SkillCheck()
    border_top = Border(0, 250, 800, 250)
    border_bottom = Border(0, 470, 800, 250)
    border_left = Border(0, 250, 0, 470)
    border_right = Border(795, 250, 795, 470)
    border_top_fight = Border(200, 250, 600, 250)
    border_bottom_fight = Border(200, 470, 605, 470)
    border_left_fight = Border(200, 250, 200, 470)
    border_right_fight = Border(600, 250, 600, 470)
    hud = HUD(100)
    music.play(loops=-1)
    res = battle_screen(music)  # запуск боя и запись результата
    # обновление окна в соответствии с результатом
    if res == 'escaped':
        escape_screen()
    elif res == 'died':
        player_lost_screen()
    elif res == 'won_un':
        unlocking_new_enemy_screen()
    elif res == 'completed':
        game_completed_screen()
        screen.fill('black')
        start_screen()  # если игра пройдена, то запускается стартовый экран
    # обновление спрайтов и музыки
    all_sprites = pygame.sprite.Group()
    WAITING_FROG.set_back()
    ATTACKING_FROG.set_back()
    DYING_FROG.set_back()
    WAITING_DEMON.set_back()
    ATTACKING_DEMON.set_back()
    DYING_DEMON.set_back()
    WAITING_CAT.set_back()
    ATTACKING_CAT.set_back()
    DYING_CAT.set_back()
