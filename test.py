import math
import os
import sys

import pygame

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Путь к славе')
invincibility_color = [pygame.Color('orange'), pygame.Color('purple')]
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
clock = pygame.time.Clock()
fps = 60
swap = True


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
    if not com1:
        rect = enemy1.image.get_rect()
        image = pygame.Surface([rect.width, rect.height])
        image.set_alpha(230)
        enemy1.image.blit(image, (0, 0))
    enemy1.image = pygame.transform.scale(enemy1.image, (400, 400))
    enemy2 = pygame.sprite.Sprite()
    enemy2.image = load_image('second_enemy.png', colorkey=-1)  # фото второго врага
    enemy2.rect = enemy1.image.get_rect()
    if not com2:
        rect = enemy2.image.get_rect()
        image = pygame.Surface([rect.width, rect.height])
        image.set_alpha(230)
        enemy2.image.blit(image, (0, 0))
    enemy2.image = pygame.transform.scale(enemy2.image, (400, 400))
    enemy3 = pygame.sprite.Sprite()
    enemy3.image = load_image('third_enemy.png')  # фото третьего врага
    enemy3.rect = enemy1.image.get_rect()
    if not com3:
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
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
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
                            running = False
                    if 730 < x < 770 and 275 < y < 325:
                        enemy_shown = enemy_shown + 1 if enemy_shown + 1 <= 2 else 0
                    if 30 < x < 70 and 275 < y < 325:
                        enemy_shown = enemy_shown - 1 if enemy_shown - 1 >= 0 else 2
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
        pygame.display.flip()
        clock.tick(fps)
    return enemy_shown


class HUD:
    def __init__(self, hp):
        super().__init__()
        self.hp = hp
        self.screen = pygame.Surface((800, 135))
        self.font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
        self.check_turn = False
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
        # переменная
        self.do_damage = False
        # переменная
        self.wait = True

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

    # функция хода игрока
    def turn(self):
        ...

    # функция для получения урона игроком
    def take_damage(self, health, invincibility):
        for particle in enemy.particles_list:
            if pygame.sprite.collide_mask(self, particle) and not invincibility:
                health -= enemy.damage
                hud.hp = health
                self.invincibility = True

    # функция атаки противника
    def attack(self):
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
        if self.do_damage:
            self.pause += 1
            if self.pause == 150:
                player.image.fill(pygame.Color('orange'))
                all_sprites.remove(skillcheck)
                swap = not swap
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
        # Частица в формате кадр: изображение, x, y, скорость по x, скорость по y, ускорение по x, ускорение по y
        # всё сразу переделывается в нужные типы
        if len(part) == 9:
            res[int(part[0])] = [load_image(part[1], colorkey=part[-1]),
                                 *[int(x) for x in part[2:6]], *[float(x) for x in part[6:8]]]
        if len(part) == 8:
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
    def __init__(self, sheet, columns, rows, s):
        self.rect = get_rect_from_sheet(sheet, columns, rows)
        self.images = cut_sheet(sheet, self.rect, columns, rows)
        self.s, self.st, self.cur_frame = s, 0, 0

    def get_frame(self):
        return self.images[self.cur_frame]

    def update(self):
        self.st += 1
        if self.st == self.s:
            self.st = 0
            self.cur_frame += 1
            if self.cur_frame == len(self.images):
                self.cur_frame = 0

    def set_back(self):
        self.cur_frame, self.st = 0, 0

    def get_rect(self):
        return self.rect

    def get_frames_num(self):
        return len(self.images) * self.s

    def get_last_frame(self):
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
        self.ending_frames_sum = self.dying_sheet.get_frames_num() + 180
        self.dying_sheet_frames_num = self.dying_sheet.get_frames_num()
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
        global skillcheck
        self.status = 0
        skillcheck = SkillCheck()
        skillcheck.swap_sides(swap)

    def die(self):
        self.status = 2

    def is_attacking(self):
        return True if self.status == 1 else False

    def dying_animation(self):
        if self.status == 2:
            self.ending_frames += 1
            if self.ending_frames == self.dying_sheet.get_frames_num():
                self.dying_sheet = SpriteSheet(self.dying_sheet.get_last_frame(), 1, 1, 180)
                font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
                ending_text = font.render('you won!', 1, pygame.Color('white'))
                sprite = pygame.sprite.Sprite(all_sprites)
                sprite.image = ending_text
                sprite.rect = ending_text.get_rect()
                sprite.rect.x, sprite.rect.y = 400 - (sprite.rect.width // 2), (250 - sprite.rect.height) // 2
            if self.ending_frames == self.ending_frames_sum:
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
            from random import choice
            attack = choice([int(x) for x in range(1, 9) if x != self.past_attack])
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
            from random import choice
            attack = choice([int(x) for x in range(1, 3) if x != self.past_attack])
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


class SkillCheck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((20, 200))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = -15
        self.rect.y = 262
        self.left_to_right = True

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
    font = pygame.font.Font('data/MonsterFriend2Fore.otf', 40)
    escaping_text = font.render('you ran away...', 1, pygame.Color('white'))
    rect = escaping_text.get_rect()
    rect.x, rect.y = 400 - (rect.width // 2), 300 - (rect.height // 2)
    sc = 300
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill('black')
        screen.blit(escaping_text, rect)
        if sc == 0:
            running = False
        sc -= 1
        pygame.display.flip()
        clock.tick(fps)


def player_lost_screen():
    font = pygame.font.Font('data/MonsterFriend2Fore.otf', 40)
    loosing_text = font.render('you died...', 1, pygame.Color('red'))
    rect = loosing_text.get_rect()
    rect.x, rect.y = 400 - (rect.width // 2), 300 - (rect.height // 2)
    sc = 300
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill('black')
        screen.blit(loosing_text, rect)
        if sc == 0:
            running = False
        sc -= 1
        pygame.display.flip()
        clock.tick(fps)


def unlocking_new_enemy_screen():
    font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
    unlock_text = font.render('you unlocked new enemy!', 1, pygame.Color('yellow'))
    rect = unlock_text.get_rect()
    rect.x, rect.y = 400 - (rect.width // 2), 300 - (rect.height // 2)
    sc = 300
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill('black')
        screen.blit(unlock_text, rect)
        if sc == 0:
            running = False
        sc -= 1
        pygame.display.flip()
        clock.tick(fps)


def game_completed_screen():
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
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill('black')
        screen.blit(complete_text, rect_c)
        screen.blit(thanks_text, rect_t)
        if sc == 0:
            running = False
        sc -= 1
        pygame.display.flip()
        clock.tick(fps)


def battle_screen():
    result = False
    key_a = False
    key_d = False
    key_w = False
    key_s = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    key_a = True
                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    key_d = True
                if event.key in (pygame.K_w, pygame.K_UP):
                    key_w = True
                if event.key in (pygame.K_s, pygame.K_DOWN):
                    key_s = True
                if event.key == pygame.K_SPACE and enemy.status == 0:
                    player.attack()
                if event.key == pygame.K_ESCAPE:
                    result = 'escaped'
                    running = False
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    key_a = False
                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    key_d = False
                if event.key in (pygame.K_w, pygame.K_UP):
                    key_w = False
                if event.key in (pygame.K_s, pygame.K_DOWN):
                    key_s = False
        screen.fill((0, 0, 0))
        if enemy.is_attacking():
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
            result = 'died'
            running = False
        if enemy.hp <= 0:
            skillcheck.kill()
            enemy.die()
            if enemy.dying_animation():
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
                    file1.close()
                running = False
        if enemy.status == 0:
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
        pygame.display.flip()
        clock.tick(fps)
    return result


WAITING_FROG = SpriteSheet(load_image('waiting_frog.png', colorkey=-1), 14, 1, 10)
ATTACKING_FROG = SpriteSheet(load_image('attacking_frog.png', colorkey=-1), 14, 1, 10)
DYING_FROG = SpriteSheet(load_image('dying_frog.png', colorkey=-1), 14, 1, 10)
WAITING_DEMON = SpriteSheet(load_image('waiting_demon.png', colorkey=-1), 6, 1, 6)
ATTACKING_DEMON = SpriteSheet(load_image('attacking_demon.png', colorkey=-1), 15, 1, 6)
DYING_DEMON = SpriteSheet(load_image('dying_demon.png', colorkey=-1), 22, 1, 6)
start_screen()
while True:
    chosen_enemy = fighting_menu()
    if chosen_enemy == 0:
        enemy = Frog([WAITING_FROG,
                      ATTACKING_FROG,
                      DYING_FROG], 320, 150, 160, 100)
    elif chosen_enemy == 1:
        enemy = Demon([WAITING_DEMON,
                       ATTACKING_DEMON,
                       DYING_DEMON], 200, 28, 400, 222)
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
    res = battle_screen()
    if res == 'escaped':
        escape_screen()
    elif res == 'died':
        player_lost_screen()
    elif res == 'won_un':
        unlocking_new_enemy_screen()
    elif res == 'completed':
        game_completed_screen()
    all_sprites = pygame.sprite.Group()
    WAITING_FROG.set_back()
    ATTACKING_FROG.set_back()
    DYING_FROG.set_back()
    WAITING_DEMON.set_back()
    ATTACKING_DEMON.set_back()
    DYING_DEMON.set_back()
