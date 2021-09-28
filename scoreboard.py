import pygame
import pygame.font
from pygame.sprite import Group
 
from ship import Ship

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 20)

        # Prepare the initial score images.
        # self.prep_name()
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_controls()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(f"Score: {score_str}", True,
                self.text_color, self.settings.bg_color)
        
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(f"High Score: {high_score_str}", True,
                self.text_color, self.settings.bg_color)
            
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(f"Level: {level_str}", True,
                self.text_color, self.settings.bg_color)
    
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_name(self, name):
        """Turn the level into a rendered image."""
        self.name = name.title()
        name_string = str(self.name)
        self.name_image = self.font.render(f"Name: {name_string}", True,
                self.text_color, self.settings.bg_color)
    
        # Position the level below the score.
        self.name_rect = self.name_image.get_rect()
        self.name_rect.right = self.score_rect.right
        self.name_rect.top = self.level_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            self.ship = Ship(self.ai_game)
            self.ship.rect.x = 10 + ship_number * self.ship.rect.width
            self.ship.rect.y = 10
            self.ships.add(self.ship)


    def prep_controls(self):
        """Show what buttons to use in play"""
        control_str = "Q = 'QUIT'  P = 'Pause' M = 'Mute'"
        self.control_image = self.small_font.render(control_str, True, 
            self.text_color, self.settings.bg_color)

        # Position control info bottom right.
        self.control_rect = self.control_image.get_rect()
        self.control_rect.right = self.score_rect.right
        self.control_rect.bottom = self.screen_rect.bottom - 10

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Draw scores, level, and ships to the screen."""
        self.screen.blit(self.name_image, self.name_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
