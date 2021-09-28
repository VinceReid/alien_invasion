import pygame
from pygame.locals import *

def name():
    pygame.init()
    intro_screen = pygame.display.set_mode((480, 360))
    pygame.display.set_caption("Take me to your leader!")
    q1 = "What is your name?"
    name = ""
    font = pygame.font.Font(None, 50)
    while True:
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.unicode and evt.key != K_BACKSPACE and evt.key != K_RETURN:
                    name += evt.unicode
                elif evt.key == K_BACKSPACE:
                    name = name[:-1]
                elif evt.key == K_RETURN:
                    name = ""
            elif evt.type == QUIT:
                return

            intro_screen.fill((0, 0, 0))
            block1 = font.render(q1, True, (255, 255, 255))
            rect1 = block1.get_rect()
            rect1.center = intro_screen.get_rect().center
            rect1.y -= rect1.y /4
            intro_screen.blit(block1, rect1)
            block2 = font.render(name, True, (255, 255, 255))
            rect2 = block2.get_rect()
            rect2.center = intro_screen.get_rect().center 
            rect2.y += rect2.y /4
            intro_screen.blit(block2, rect2)
            pygame.display.flip()

if __name__ == "__main__":
    name()
    pygame.quit()