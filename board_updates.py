import pygame


class Update:
    def __init__(self):
        pass

    def move_update(self, screen, moves):
        screen.fill(pygame.Color('black'), (830, 115, 100, 40))
        font = pygame.font.Font(None, 50)
        string_rendered = font.render(moves, 1, pygame.Color('grey'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 830
        intro_rect.y = 115
        screen.blit(string_rendered, intro_rect)
        pygame.display.update()

    def time_update(self, screen, time):
        screen.fill(pygame.Color('black'), (840, 160, 40, 40))
        font = pygame.font.Font(None, 50)
        string_rendered = font.render(str(time), 1, pygame.Color('grey'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 840
        intro_rect.y = 160
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()

    def quota_update(self, screen, quota):
        screen.fill(pygame.Color('black'), (830, 205, 100, 40))
        font = pygame.font.Font(None, 50)
        string_rendered = font.render(quota, 1, pygame.Color('grey'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 830
        intro_rect.y = 205
        screen.blit(string_rendered, intro_rect)
        pygame.display.update()

    def multiplication_update(self, screen, points_multiplication):
        screen.fill(pygame.Color('black'), (920, 250, 100, 40))
        font = pygame.font.Font(None, 50)
        string_rendered = font.render(str(points_multiplication), 1, pygame.Color('grey'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 920
        intro_rect.y = 250
        screen.blit(string_rendered, intro_rect)
        pygame.display.update()

    def points_sum_update(self, screen, points_sum, num):
        screen.fill(pygame.Color('black'), (840, 295, 200, 40))
        font = pygame.font.Font(None, 50)
        next_points_sum = points_sum - (points_sum % num) + num
        string_rendered = font.render(f'{points_sum}/{next_points_sum, next_points_sum + num}',
                                      1, pygame.Color('grey'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 840
        intro_rect.y = 295
        screen.blit(string_rendered, intro_rect)
        pygame.display.update()

    def score_update(self, screen, score):
        screen.fill(pygame.Color('black'), (810, 340, 100, 40))
        font = pygame.font.Font(None, 50)
        string_rendered = font.render(str(score), 1, pygame.Color('grey'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 810
        intro_rect.y = 340
        screen.blit(string_rendered, intro_rect)
        pygame.display.update()
