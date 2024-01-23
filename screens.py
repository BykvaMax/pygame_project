import random

import pygame
import os
import sys


class Screen:
    def __init__(self):
        pass

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
        return image

    def start_screen(self, screen, width, height):
        fon = pygame.transform.scale(self.load_image('fon3.webp'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 100)
        string_rendered = font.render('Stone Breaker', 1, pygame.Color('grey'))
        intro_rect = string_rendered.get_rect()
        intro_rect.left = 275
        intro_rect.top = 50
        screen.blit(string_rendered, intro_rect)

        font = pygame.font.Font(None, 70)
        string_rendered = font.render('Чтобы начать игру нажмите "Space"', 1, pygame.Color('grey'))
        intro_rect = string_rendered.get_rect()
        intro_rect.left = 70
        intro_rect.top = 470
        screen.blit(string_rendered, intro_rect)

        font = pygame.font.Font(None, 70)
        string_rendered = font.render('Чтобы посмотреть правила нажмите "R"', 1, pygame.Color('grey'))
        intro_rect = string_rendered.get_rect()
        intro_rect.left = 20
        intro_rect.top = 550
        screen.blit(string_rendered, intro_rect)

        font = pygame.font.Font(None, 70)
        string_rendered = font.render('Чтобы выйти нажмите "Esc"', 1, pygame.Color('grey'))
        intro_rect = string_rendered.get_rect()
        intro_rect.left = 165
        intro_rect.top = 630
        screen.blit(string_rendered, intro_rect)

    def show_rules(self, screen, width, height):
        rules = ['sadf', 'asfd', 'asgag', 'adfag']
        rules_fon = pygame.transform.scale(self.load_image('fon2.webp'), (width, height))
        screen.blit(rules_fon, (0, 0))

        font = pygame.font.Font(None, 60)
        string_rendered = font.render('Правила', 1, pygame.Color('grey'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 400
        intro_rect.y = 20
        screen.blit(string_rendered, intro_rect)

        text_coord = 70
        for line in rules:
            font = pygame.font.Font(None, 30)
            string_rendered = font.render(line, 1, pygame.Color('grey'))
            intro_rect = string_rendered.get_rect()
            text_coord += 25
            intro_rect.top = text_coord
            intro_rect.x = 10
            screen.blit(string_rendered, intro_rect)

    # def show_game_board(self, screen, time, score, level):
    #     screen.fill(pygame.Color('black'))
    #     stat = [f'Время: {time}', f'Сумма: {time}', f'Число: {random.randint(2, 10)}', f'Счёт: {score}',
    #             f'Уровень: {level}']
    #
    #     font = pygame.font.Font(None, 60)
    #     string_rendered = font.render('Статистика', 1, pygame.Color('grey'))
    #     intro_rect = string_rendered.get_rect()
    #     intro_rect.x = 650
    #     intro_rect.y = 20
    #     screen.blit(string_rendered, intro_rect)
    #
    #     text_coord = 70
    #     for line in stat:
    #         font = pygame.font.Font(None, 50)
    #         string_rendered = font.render(line, 1, pygame.Color('grey'))
    #         intro_rect = string_rendered.get_rect()
    #         text_coord += 45
    #         intro_rect.top = text_coord
    #         intro_rect.x = 650
    #         screen.blit(string_rendered, intro_rect)

    def lose_screen(self, screen, width, height, score, level):
        stat = [f'Счёт: {score}', f'Уровень: {level}']
        rules_fon = pygame.transform.scale(self.load_image('fon2.webp'), (width, height))
        screen.blit(rules_fon, (0, 0))

        font = pygame.font.Font(None, 100)
        string_rendered = font.render('ВЫ ПРОИГРАЛИ', 1, pygame.Color('dark grey'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 250
        intro_rect.y = 20
        screen.blit(string_rendered, intro_rect)

        text_coord = 100
        for line in stat:
            font = pygame.font.Font(None, 80)
            string_rendered = font.render(line, 1, pygame.Color('dark grey'))
            intro_rect = string_rendered.get_rect()
            text_coord += 75
            intro_rect.top = text_coord
            intro_rect.x = 250
            screen.blit(string_rendered, intro_rect)
