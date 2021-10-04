import pygame

class TextBlit:
    """A class to blit text to screen"""

    def __init__(self, ai_game, text, text_color = (255, 255, 255)):
        """takes text input, creates image and rect and blit"""
        self.intro_screen = ai_game.intro_screen
        self.intro_screen_rect = self.intro_screen.get_rect()

        self.font = pygame.font.Font(None, 50)
        self.text_color = text_color

        self.image = self.font.render(text, True, self.text_color)
        self.rect = self.image.get_rect()
        self.rect.center = self.intro_screen_rect.center


    def blit(self):
        """Blit image to screen"""
        self.intro_screen.blit(self.image, self.rect)

    def flip(self):
        """Flips screen to display blit text"""
        pygame.display.flip()
