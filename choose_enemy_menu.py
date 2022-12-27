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
    pygame.init()
    size = WIDTH, HEIGHT = 800, 600
    font = pygame.font.Font('data/game_font.otf', 32)
    text = font.render("Выберите врага", True, 'white')
    text_x = 257
    text_y = 535
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Перемещение героя')
    running = True
    clock = pygame.time.Clock()
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
        clock.tick(60)
    return enemy_shown