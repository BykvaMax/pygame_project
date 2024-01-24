import os
import sys
import random

import pygame
from pygame import time

from screens import Screen
from board_updates import Update


all_sprites = pygame.sprite.Group()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Stone Breaker')
        size = self.width, self.height = 1000, 700
        self.screen = pygame.display.set_mode(size)
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.screens = Screen()
        self.updates = Update()

        self.all_sprites = pygame.sprite.Group()
        self.num = 0
        self.difficulty = 'Легко'
        self.moves = '15/15'
        self.remaining_time = 60
        self.quota = '0/20'
        self.points_sum = 0
        self.score = 0
        self.level = 0
        self.points_multiplication = 1
        self.last_move_stones = 0
        self.cur_move_stones = 0

    def load_image(self, name, colorkey=None):
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
            image = pygame.transform.scale(image, (600, 200))
        return image

    def terminate(self):
        pygame.quit()
        sys.exit()

    def show_game_board(self):
        if self.difficulty == 'Легко':
            self.moves = '15/15'
            self.remaining_time = 60
            self.quota = '0/20'
        elif self.difficulty == 'Средне':
            self.moves = '20/20'
            self.remaining_time = 45
            self.quota = '0/35'
        elif self.difficulty == 'Сложно':
            self.moves = '25/25'
            self.remaining_time = 30
            self.quota = '0/50'

        self.points_sum = 0
        self.stones_dct = {}
        self.crashed_stones = []
        self.used_big_stones = []
        self.big_stone_check = False
        self.num = random.randint(1, 9)
        self.level += 1
        self.screen.fill(pygame.Color('black'))
        small_stone_picture = pygame.transform.scale(self.load_image('stone2.png', -1), (225, 225))
        stone_coord = (-40, -40)
        for i in range(12):
            num = str(random.randint(1, 9))
            self.screen.blit(small_stone_picture, stone_coord)
            font = pygame.font.Font(None, 45)
            string_rendered = font.render(num, 1, pygame.Color('red'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = stone_coord[0] + 100
            intro_rect.y = stone_coord[1] + 100
            self.screen.blit(string_rendered, intro_rect)

            self.stones_dct[str(i + 1)] = (num, -1, (stone_coord[0] + 60, stone_coord[0] + 170,
                                                     stone_coord[1] + 80, stone_coord[1] + 150))

            if i < 3:
                stone_coord = (stone_coord[0] + 180, -40)
            elif i < 6:
                stone_coord = (500, stone_coord[1] + 160)
            elif i < 9:
                stone_coord = (stone_coord[0] - 180, 440)
            elif i < 11:
                stone_coord = (-40, stone_coord[1] - 160)

        medium_stone_picture = pygame.transform.scale(self.load_image('stone2.png', -1), (300, 300))
        stone_coord = (70, 50)
        num_lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(4):
            num = str(random.choice(num_lst))
            num_lst.remove(int(num))
            self.screen.blit(medium_stone_picture, stone_coord)
            font = pygame.font.Font(None, 60)
            string_rendered = font.render(num, 1, pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = stone_coord[0] + 135
            intro_rect.y = stone_coord[1] + 135
            self.screen.blit(string_rendered, intro_rect)

            self.stones_dct[str(i + 13)] = (num, (stone_coord[0] + 80, stone_coord[0] + 230,
                                                  stone_coord[1] + 100, stone_coord[1] + 200))

            if i == 0:
                stone_coord = (stone_coord[0] + 235, 50)
            elif i == 1:
                stone_coord = (305, stone_coord[1] + 235)
            elif i == 2:
                stone_coord = (stone_coord[0] - 235, 285)

        big_stone_picture = pygame.transform.scale(self.load_image('stone2.png', -1), (400, 400))
        self.screen.blit(big_stone_picture, (135, 115))
        font = pygame.font.Font(None, 80)
        string_rendered = font.render(str(self.num), 1, pygame.Color('light blue'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 315
        intro_rect.y = 295
        self.screen.blit(string_rendered, intro_rect)

        # c1 = (10, 0)
        # c2 = (0, 10)
        # for i in range(70):
        #     self.screen.fill(pygame.Color('grey'), (c1[0], c1[1], 1, 700))
        #     self.screen.fill(pygame.Color('grey'), (c2[0], c2[1], 700, 1))
        #     c1 = (c1[0] + 10, 0)
        #     c2 = (0, c2[1] + 10)

        self.screen.fill(pygame.Color('grey'), (15, 20, 670, 1))
        self.screen.fill(pygame.Color('grey'), (685, 20, 1, 590))
        self.screen.fill(pygame.Color('grey'), (15, 20, 1, 590))
        self.screen.fill(pygame.Color('grey'), (15, 610, 670, 1))

        stat = [f'Ходы: {self.moves}', 'Время: ', f'Квота: {self.quota}', f'Сумма: {self.points_sum}',
                f'Счёт: {self.score}', f'Уровень: {self.level}', f'Сложность:', self.difficulty]

        font = pygame.font.Font(None, 60)
        string_rendered = font.render('Статистика', 1, pygame.Color('grey'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 710
        intro_rect.y = 20
        self.screen.blit(string_rendered, intro_rect)

        text_coord = 70
        for line in stat:
            font = pygame.font.Font(None, 50)
            string_rendered = font.render(line, 1, pygame.Color('grey'))
            intro_rect = string_rendered.get_rect()
            text_coord += 45
            intro_rect.top = text_coord
            intro_rect.x = 710
            self.screen.blit(string_rendered, intro_rect)

    def stone_click(self, mouse_pos):
        for key, value in self.stones_dct.items():
            if key not in self.crashed_stones and value[-1][0] < mouse_pos[0] < value[-1][1] and value[-1][2] < mouse_pos[1] < value[-1][3]:
                if int(key) > 12:
                    self.big_stone_check = True
                if int(key) < 13 and self.big_stone_check:
                    self.quota = f'{int(self.quota.split("/")[0]) + 1 * self.points_multiplication}/{self.quota.split("/")[1]}'
                    self.updates.quota_update(self.screen, self.quota)

                    self.screen.fill(pygame.Color('black'), (int(value[-1][0]), int(value[-1][2]),
                                                             int(value[-1][1]) - int(value[-1][0]),
                                                             int(value[-1][3]) - int(value[-1][2])))
                    pygame.display.update()
                    self.stones_dct[key] = (value[0], 1, value[-1])
                    self.crashed_stones.append(key)
                    self.explosion = AnimatedSprite(self.load_image('stone_explosion2.png'), 5, 2, int(value[-1][0]) - 2, int(value[-1][2]) - 12)
                    self.explosion_sound.play()
                    for i in range(9):
                        self.screen.fill(pygame.Color('black'), (int(value[-1][0]), int(value[-1][2]),
                                                                 int(value[-1][1]) - int(value[-1][0]),
                                                                 int(value[-1][3]) - int(value[-1][2]) + 5))
                        self.explosion.update()
                        all_sprites.draw(self.screen)
                        pygame.display.update()
                        pygame.display.update()
                        time.delay(100)

                if self.big_stone_check and key not in self.used_big_stones:
                    self.points_sum += int(value[0])
                    self.updates.points_sum_update(self.screen, self.points_sum)
                    self.cur_move_stones += 1
                    if int(key) > 12:
                        self.stone_hit_sound.play()

                if int(key) > 12:
                    self.used_big_stones.append(key)

    def main(self):
        start = False
        pause = False
        mine_sound = pygame.mixer.Sound('mine_sound.mp3')
        self.explosion_sound = pygame.mixer.Sound('explosion_sound.mp3')
        self.stone_hit_sound = pygame.mixer.Sound('stone_hit_sound.mp3')
        # dragon = AnimatedSprite(self.load_image("dragon.png"), 8, 2, 50, 50)

        self.screens.start_screen(self.screen, self.width, self.height, self.difficulty)

        rules_or_fon = 1
        sound = True
        mine_sound.play()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.terminate()
                    if event.key == pygame.K_h:
                        start = False
                        self.score = 0
                        self.level = 0
                        self.screens.start_screen(self.screen, self.width, self.height, self.difficulty)
                    if event.key == pygame.K_l:
                        start = False
                        self.screens.lose_screen(self.screen, self.width, self.height, self.score, self.level, self.difficulty)
                    if event.key == pygame.K_m:
                        if not sound:
                            sound = True
                            mine_sound.play()
                        else:
                            sound = False
                            mine_sound.stop()
                    if event.key == pygame.K_SPACE and pause:
                        self.moves = f'{self.moves.split("/")[1]}/{self.moves.split("/")[1]}'
                        self.quota = f'0/{self.quota.split("/")[1]}'
                        self.show_game_board()
                        start_ticks = pygame.time.get_ticks()
                        last_seconds = 0
                        pause = False
                    if not start:
                        if event.key == pygame.K_d and rules_or_fon % 2 == 1:
                            if self.difficulty == 'Легко':
                                self.difficulty = 'Средне'
                            elif self.difficulty == 'Средне':
                                self.difficulty = 'Сложно'
                            elif self.difficulty == 'Сложно':
                                self.difficulty = 'Легко'
                            self.screens.start_screen(self.screen, self.width, self.height, self.difficulty)
                            pygame.display.update()

                        if event.key == pygame.K_SPACE and rules_or_fon % 2 == 1:
                            start = True
                            self.score = 0
                            self.level = 0
                            self.show_game_board()
                            start_ticks = pygame.time.get_ticks()
                            last_seconds = 0

                        if event.key == pygame.K_r:
                            if rules_or_fon % 2 == 1:
                                rules_or_fon += 1
                                self.screens.show_rules(self.screen, self.width, self.height)
                            else:
                                rules_or_fon += 1
                                self.screens.start_screen(self.screen, self.width, self.height, self.difficulty)
                    else:
                        pass

                elif event.type == pygame.MOUSEBUTTONDOWN and start and not pause:
                    if 15 < pygame.mouse.get_pos()[0] < 685 and 20 < pygame.mouse.get_pos()[1] < 610:
                        self.stone_click(pygame.mouse.get_pos())

            if not pause:
                if start and (pygame.time.get_ticks() - start_ticks) / 1000 > last_seconds:
                    self.updates.time_update(self.screen, self.remaining_time)
                    self.remaining_time -= 1
                    last_seconds += 1
                    pygame.display.update()

                if start and self.remaining_time == 0:
                    start = False
                    self.screens.lose_screen(self.screen, self.width, self.height, self.score, self.level, self.difficulty)

                if start and len(self.crashed_stones) == 12 and len(self.used_big_stones) == 4 and self.points_sum % self.num != 0:
                    time.delay(1000)
                    start = False
                    self.screens.lose_screen(self.screen, self.width, self.height, self.score, self.level, self.difficulty)

                if start and self.points_sum != 0 and self.points_sum % self.num == 0:
                    if self.difficulty == 'Легко':
                        self.score += self.remaining_time
                    elif self.difficulty == 'Средне':
                        self.score += self.remaining_time * 2
                    elif self.difficulty == 'Сложно':
                        self.score += self.remaining_time * 3
                    self.updates.score_update(self.screen, self.score)
                    self.moves = f'{int(self.moves.split("/")[0]) - 1}/{self.moves.split("/")[1]}'
                    self.updates.move_update(self.screen, self.moves)
                    if self.difficulty == 'Легко':
                        self.remaining_time = 60
                    elif self.difficulty == 'Средне':
                        self.remaining_time = 45
                    elif self.difficulty == 'Сложно':
                        self.remaining_time = 30
                    start_ticks = pygame.time.get_ticks()
                    last_seconds = 0
                    self.used_big_stones.clear()
                    self.big_stone_check = False
                    if self.last_move_stones == self.cur_move_stones:
                        self.points_multiplication += 1
                    elif self.last_move_stones == self.cur_move_stones and self.last_move_stones != 0:
                        self.points_multiplication = 1
                    self.last_move_stones = self.cur_move_stones
                    self.cur_move_stones = 0
                    self.points_sum = 0
                    self.updates.points_sum_update(self.screen, self.points_sum)
                    for key, value in self.stones_dct.items():
                        if int(key) < 13 and value[1] > -1:
                            self.stones_dct[key] = (value[0], value[1] - 1, value[-1])
                        if value[1] == -1 and key in self.crashed_stones:
                            small_stone_picture = pygame.transform.scale(self.load_image('stone2.png', -1), (225, 225))
                            num = str(random.randint(1, 9))
                            self.screen.blit(small_stone_picture, (value[-1][0] - 60, value[-1][2] - 80))
                            font = pygame.font.Font(None, 45)
                            string_rendered = font.render(num, 1, pygame.Color('red'))
                            intro_rect = string_rendered.get_rect()
                            intro_rect.x = value[-1][0] - 60 + 100
                            intro_rect.y = value[-1][2] - 80 + 100
                            self.screen.blit(string_rendered, intro_rect)
                            pygame.display.update()

                            self.stones_dct[key] = (num, -1, value[-1])
                            self.crashed_stones.remove(key)

                        elif int(key) < 13 and key not in self.crashed_stones:
                            self.stones_dct[key] = (str(int(value[0]) + 1), -1, value[-1])
                            if not int(value[0]) + 1 > 9:
                                small_stone_picture = pygame.transform.scale(self.load_image('stone2.png', -1), (225, 225))
                                self.screen.blit(small_stone_picture, (value[-1][0] - 60, value[-1][2] - 80))
                                font = pygame.font.Font(None, 45)
                                string_rendered = font.render(str(int(value[0]) + 1), 1, pygame.Color('red'))
                                intro_rect = string_rendered.get_rect()
                                intro_rect.x = value[-1][0] - 60 + 100
                                intro_rect.y = value[-1][2] - 80 + 100
                                self.screen.blit(string_rendered, intro_rect)
                                pygame.display.update()
                            else:
                                self.screen.fill(pygame.Color('black'), (int(value[-1][0]), int(value[-1][2]),
                                                                         int(value[-1][1]) - int(value[-1][0]),
                                                                         int(value[-1][3]) - int(value[-1][2])))
                                pygame.display.update()
                                self.stones_dct[key] = (random.randint(1, 9), 1, value[-1])
                                self.crashed_stones.append(key)

                    self.num = random.randint(1, 9)
                    big_stone_picture = pygame.transform.scale(self.load_image('stone2.png', -1), (400, 400))
                    self.screen.blit(big_stone_picture, (135, 115))
                    font = pygame.font.Font(None, 80)
                    string_rendered = font.render(str(self.num), 1, pygame.Color('light blue'))
                    intro_rect = string_rendered.get_rect()
                    intro_rect.x = 315
                    intro_rect.y = 295
                    self.screen.blit(string_rendered, intro_rect)

            if start and int(self.moves.split("/")[0]) == 0:
                if int(self.quota.split("/")[0]) >= int(self.quota.split("/")[1]):
                    pause = True
                    font = pygame.font.Font(None, 50)
                    string_rendered = font.render('Нажмите "Space" для следующего уровня', 1, pygame.Color('grey'))
                    intro_rect = string_rendered.get_rect()
                    intro_rect.x = 10
                    intro_rect.y = 630
                    self.screen.blit(string_rendered, intro_rect)
                    pygame.display.update()
                else:
                    time.delay(1000)
                    start = False
                    self.screens.lose_screen(self.screen, self.width, self.height, self.score, self.level, self.difficulty)

            pygame.display.update()
            self.clock.tick(10)


start_game = Main()
start_game.main()
