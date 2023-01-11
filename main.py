import sys
import os
import pygame

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Путь к славе')
invincibility_color = [pygame.Color('orange'), pygame.Color('purple')]


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
    enemy1.image = load_image('first_enemy.png')  # фото первого врага
    enemy1.rect = enemy1.image.get_rect()
    if not com1:
        rect = enemy1.image.get_rect()
        image = pygame.Surface([rect.width, rect.height])
        image.set_alpha(230)
        enemy1.image.blit(image, (0, 0))
    enemy1.image = pygame.transform.scale(enemy1.image, (400, 400))
    enemy2 = pygame.sprite.Sprite()
    enemy2.image = load_image('second_enemy.png')  # фото второго врага
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
    def __init__(self, name, lvl, hp):
        super().__init__()
        self.name = name
        self.lvl = lvl
        self.hp = hp
        self.screen = pygame.Surface((800, 600))
        self.font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
        self.check_turn = False
        # установка цвета для отрисовки кнопок, чтобы игрок понял, на какой кнопке находится(во время своего хода)
        self.color = 'orange'

    def draw_name(self):  # отрисовка имени
        string_rendered = self.font.render(self.name, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 490
        intro_rect.x = 0
        screen.blit(string_rendered, intro_rect)

    def draw_lvl(self):  # отрисовка уровня
        string_rendered = self.font.render('LV ' + self.lvl, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 490
        intro_rect.x = 120
        screen.blit(string_rendered, intro_rect)

    def draw_hp(self):  # отрисовка хп
        font = pygame.font.Font('data/MonsterFriend2Fore.otf', 25)
        string_rendered = font.render('HP', 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 492
        intro_rect.x = 250
        screen.blit(string_rendered, intro_rect)
        pygame.draw.rect(self.screen, pygame.Color('yellow'), (310, 485, self.hp * 2, 35))
        pygame.draw.rect(self.screen, pygame.Color('red'),
                         (510 - abs(self.hp - 100) * 2, 485, abs(self.hp - 100) * 2, 35))

    def draw_fight_button(self):  # отрисовка кнопки файт
        pygame.draw.rect(self.screen, pygame.Color(self.color), (0, 530, 150, 70), 5)
        font = pygame.font.Font('data/MonsterFriend2Fore.otf', 30)
        string_rendered = font.render('FIGHT', 1, pygame.Color(self.color))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 553
        intro_rect.x = 7
        screen.blit(string_rendered, intro_rect)

    def draw_escape_button(self):  # отрисовка кнопки сбежать
        pygame.draw.rect(self.screen, pygame.Color(self.color), (640, 530, 160, 70), 5)
        font = pygame.font.Font('data/MonsterFriend2Fore.otf', 25)
        string_rendered = font.render('ESCAPE', 1, pygame.Color(self.color))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 553
        intro_rect.x = 647
        screen.blit(string_rendered, intro_rect)

    def draw_all(self):  # отрисовка всего, что будет на экране
        screen.blit(self.screen, (0, 0))
        self.draw_name()
        self.draw_lvl()
        self.draw_hp()
        self.draw_fight_button()
        self.draw_escape_button()


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

    def update_field(self, x1, y1, x2, y2):
        # изменение значений поля
        if x1 == x2:
            self.image = pygame.Surface((5, y2 - y1))
            self.image.fill((255, 255, 255))
            self.rect = pygame.Rect(x1, y1, 5, y2 - y1)
        else:
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
        self.rect.x = 380
        self.rect.y = 427
        self.invincibility = False
        # таймер для неуязвимости игрока после получения урона
        self.timer = 0
        # переменная, чтобы узнать прошло ли время, чтобы сменить цвет игрока во время неуязвимости
        self.change_color = 0

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
        for particle in frog.particles_list:
            if pygame.sprite.collide_mask(self, particle) and not invincibility:
                health -= 5
                hud.hp = health
                self.invincibility = True

    def update(self):
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
        res[int(part[0])] = [load_image(part[1], colorkey=-1),
                             *[int(x) for x in part[2:6]], *[float(x) for x in part[6:]]]
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


class AnimatedEnemy(pygame.sprite.Sprite):
    """Базовый класс для всех врагов"""

    def __init__(self, sheets, columns, rows, x, y, s, width, height):
        """На вход принимаются sprite sheets, его ширина, его высота,
         х, y, количество кадров для изменения изображения, высота врага, ширина врага"""
        super().__init__(all_sprites)
        self.particles = pygame.sprite.Group()  # тут будут храниться частицы, создающиеся для атаки врага
        # создаем рект и sprite sheet для каждого состояния врага
        self.waiting_rect = get_rect_from_sheet(sheets[0], columns, rows)
        self.waiting_sheet = cut_sheet(sheets[0], self.waiting_rect, columns, rows)
        self.attacking_rect = get_rect_from_sheet(sheets[1], columns, rows)
        self.attacking_sheet = cut_sheet(sheets[1], self.attacking_rect, columns, rows)
        self.dying_rect = get_rect_from_sheet(sheets[2], columns, rows)
        self.dying_sheet = cut_sheet(sheets[2], self.dying_rect, columns, rows)
        self.frames = self.waiting_sheet[:]  # изначально враг ожидает
        self.cur_frame = 0  # отрисовывающийся кадр
        self.statuses = ['waiting', 'attacking', 'dying']  # статусы
        self.status = 0  # изначально враг ожидает
        self.st = 0  # подсчет кадров, для корректирования частоты кадров
        self.s = s  # количество кадров для изменения изображения
        self.x, self.y = x, y  # расположение
        self.width, self.height = width, height
        self.image = self.frames[self.cur_frame]  # задаем изображение
        self.image = pygame.transform.scale(self.image, (self.width, self.height))  # подстраиваем размер
        self.rect = self.waiting_rect  # задаем рект
        self.rect = self.rect.move(x, y)

    def update(self):
        t = 60
        self.st += 1
        # обновляем все значения для атакующей анимации, если это требуется
        if self.statuses[self.status] == 'attacking':
            if self.frames != self.attacking_sheet:
                self.cur_frame = 0
                self.frames = self.attacking_sheet[:]
                self.st = 0
                self.rect = self.attacking_rect
                self.rect = self.rect.move(self.x, self.y)
                self.image = self.frames[self.cur_frame]
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # обновляем все значения для умирающей анимации, если это требуется
        if self.statuses[self.status] == 'dying':
            if self.frames != self.dying_sheet:
                self.cur_frame = 0
                self.frames = self.dying_sheet[:]
                self.st = 0
                self.rect = self.dying_rect
                self.rect = self.rect.move(self.x, self.y)
                self.image = self.frames[self.cur_frame]
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # обновляем все значения для ожидающей анимации, если это требуется
        if self.statuses[self.status] == 'waiting':
            if self.frames != self.waiting_sheet:
                self.cur_frame = 0
                self.frames = self.waiting_sheet[:]
                self.st = 0
                self.rect = self.waiting_rect
                self.rect = self.rect.move(self.x, self.y)
                self.image = self.frames[self.cur_frame]
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # обновляем изображение
        if self.st == self.s:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.st = 0

    # функции ниже взаимодействуют со статусом врага
    def attack(self):
        self.status = 1

    def wait(self):
        self.status = 0

    def die(self):
        self.status = 2

    def is_attacking(self):
        return True if self.status == 1 else False


class Frog(AnimatedEnemy):
    """Класс первого врага - лягушки"""

    def __init__(self, sheets, columns, rows, x, y, s, width, height):
        """На вход принимаются sprite sheets, его ширина, его высота,
         х, y, количество кадров для изменения изображения, высота врага, ширина врага"""
        # все значения передаются в базовый класс
        super().__init__(sheets, columns, rows, x, y, s, width, height)
        self.particles_list = []  # список атакующих частиц
        self.enemy_name = 'frog'  # названия врага, для взаимодействия с файлами игры
        self.attacking_count = 0  # подсчёт кадров, чтобы создавать частицы по счёdту
        self.tactic = None  # тактика атаки
        self.past_attack = 0  # переменная, чтобы атаки не повторялись слишком часто

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


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    frog = Frog([load_image('waiting_frog.png', colorkey=-1),
                 load_image('attacking_frog.png', colorkey=-1),
                 load_image('dying_frog.png', colorkey=-1)], 14, 1, 320, 150, 10, 160, 100)
    hp = 100
    name = 'KIRA'
    lvl = '1'
    hud = HUD(name, lvl, hp)
    border_top = Border(0, 250, 800, 250)
    border_bottom = Border(0, 470, 800, 250)
    border_left = Border(0, 250, 0, 470)
    border_right = Border(795, 250, 795, 470)
    key_a = False
    key_d = False
    key_w = False
    key_s = False
    clock = pygame.time.Clock()
    fps = 60
    start_screen()
    fighting_menu()
    player = Player()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    frog.wait()
                if event.button == 2:
                    frog.attack()
                if event.button == 3:
                    frog.die()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    key_a = True
                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    key_d = True
                if event.key in (pygame.K_w, pygame.K_UP):
                    key_w = True
                if event.key in (pygame.K_s, pygame.K_DOWN):
                    key_s = True
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
        if frog.is_attacking():
            frog.move()
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
            terminate()
        hud.draw_all()
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(fps)
'''
деление на 2 нужно, чтобы квадрат был примерно по центру окна
((ширина окна - ширина кв.) // 2), (верхняя точка кв.), (ширина окна - ширина кв.) // 2 + ширина кв., верхняя точка кв.)
((ширина окна - ширина кв.) // 2, нижняя точка кв., (ширина окна - ширина кв.) // 2 + ширина кв., нижняя точка кв.)
((ширина окна - ширина кв.) // 2, верхняя точка кв., (ширина окна - ширина кв.) // 2, нижняя точка.кв)
((ширина окна - ширина кв) // 2 + (ширина кв. - толщина линий), верхняя точка кв., (ширина окна - ширина кв) // 2 + (ширина кв. - толщина линий), нижняя точка кв.)
border_top.update_field((width - 400) // 2, 250, (width - 400) // 2 + 400, 250)
border_bottom.update_field((width - 400) // 2, 470, (width - 400) // 2 + 400, 470)
border_left.update_field((width - 400) // 2, 250, (width - 400) // 2, 470)
border_right.update_field((width - 400) // 2 + (400 - 5), 250, (width - 400) // 2 + (400 - 5), 470)
можно применять мою формулу(только когда ширина кв. не равна ширине окна), или вручную подбирать размеры
'''
