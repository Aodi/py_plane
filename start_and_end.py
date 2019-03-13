import pygame
from pygame.locals import *


class start_and_end():
    @staticmethod
    def start():
        pygame.init()
        #pygame.mixer.music.load("./sound/game_music.wav")
        pygame.mixer.music.load(r".\sound\game_music.wav")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1, 0.0)
        font = pygame.font.Font(None, 48)

    @staticmethod
    def end(screen, result, score):
        font = pygame.font.Font(None, 48)
        endimage = ''
        if result == 'win':
            text1 = font.render('you win', True, (255, 0, 0))
            endimage = r'.\images\gameover.png'
        else :
            text1 = font.render(
                'you lose\nyour score is ' + str(score), True, (255, 0, 0))
            endimage = r'.\images\gameover2.png'
        text2 = font.render('your score is ' + str(score), True, (255, 0, 0))

        text_rect = text1.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery + 140
        text_rect2 = text2.get_rect()
        text_rect2.centerx = text_rect.centerx
        text_rect2.centery = text_rect.centery + 30
        gameover = pygame.image.load(endimage)
        screen.blit(gameover, (0, 0))
        screen.blit(text1, text_rect)
        screen.blit(text2, text_rect2)

        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.display.update()
            clock.tick(100)


