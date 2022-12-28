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
        self.x, self.y = x, y  # позиция
        self.vx, self.vy = vx, vy  # скорость по обеим осям
        self.ax, self.ay = ax, ay  # ускорение по обеим осям

    def update(self, t):
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

    def update(self, t):
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
        self.attacking_count = 0  # подсчёт кадров, чтобы создавать частицы по счёту
        self.tactic = None  # тактика атаки

    def move(self):
        """Функция выбирает случайную тактику из возможных и использует ее для атаки"""
        if self.attacking_count == 0:  # если это первый кадр, то выбирается случайная тактика
            from random import randint
            # пока тактика только одна, поэтому randint выбирает между 1 и 1 :)
            self.tactic = load_tactic(self.enemy_name + '_attack_' + str(randint(1, 1)) + '.txt')
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
