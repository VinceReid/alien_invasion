
import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from sound_effects import SoundEffects
from text_blit import TextBlit


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.ipInfo()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")


        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")
        self.continue_button = Button(self, "Continue")
        self.quit_button = Button(self, "Quit")

        # Start the game music and initialise SFX
        self.sfx = SoundEffects()

        #Game pause is initially off
        pause = False

        self.mouse_pos = pygame.mouse.get_pos()

        # Game intro 
        self.intro = True
        self.name = ""

    def ipInfo(self, addr=''):
        from urllib.request import urlopen
        from json import load
        if addr == '':
            url = 'https://ipinfo.io/json'
        else:
            url = 'https://ipinfo.io/' + addr + '/json'
        res = urlopen(url)
        #response from url(if res==None then check connection)
        data = load(res)
        #will load the json response into data
        self.city_id = data['city']
        self.country = data['country']

    def game_intro(self):
        """ Game intro for name input and location identified by IP address.""" 
        self.intro_screen = self.screen
        self.intro_screen_rect = self.intro_screen.get_rect()

        letter_bullet = ""
        backspace_pressed = 0

        while self.intro:
            for evt in pygame.event.get():
                if evt.type == pygame.KEYDOWN:
                    if (evt.unicode 
                    and evt.key != pygame.K_BACKSPACE
                    and evt.key != pygame.K_RETURN 
                    and len(self.name) != 12):
                        self.name += evt.unicode
                        letter_bullet = Bullet(self)
                        letter_bullet.color = (0, 255, 0)

                    elif evt.key == pygame.K_BACKSPACE and backspace_pressed == 0:
                        backspace_pressed = 1
                        # remove one character if backspace is pressed
                        if backspace_pressed == 1:
                            letter_bullet = Bullet(self)
                            letter_bullet.color = (255, 0, 0)
                            self.name = self.name[:-1]
                            
                            if letter_bullet:
                                letter_bullet.rect.midtop = intro_ship_rect.midtop
                            while letter_bullet:
                                if letter_bullet.rect.top >= last_letter_block.rect.bottom:
                                    letter_bullet.draw_bullet()
                                    letter_bullet.update()
                                    pygame.display.flip()
                                else:
                                    letter_bullet = ""
                                    backspace_pressed += 1


                    elif evt.key == pygame.K_RETURN:
                        entry_message = f"Where on Earth are you {self.name.title()}?!"
                        self.intro_screen.fill((0, 0, 0))
                        self.intro_text_2 = TextBlit(self, entry_message, (0, 255, 0))
                        self.intro_text_2.blit()
                        pygame.display.flip()
                        pygame.time.delay(2000)

                        complete_locating_message = f"Locating {self.name.title()}! . . . ."
                        locating_message = f"Locating {self.name.title()}!"
                        while locating_message != complete_locating_message:
                            self.intro_screen.fill((0, 0, 0))
                            locating_block = TextBlit(self, locating_message, (255, 0, 0))
                            locating_block.blit()
                            pygame.display.flip()
                            locating_message += " ."
                            pygame.time.delay(1000)

                        located_message = f"{self.name.title()} has been located in {self.country} near {self.city_id}!"
                        self.intro_screen.fill((0, 0, 0))
                        located = TextBlit(self, located_message,(255, 0, 0))
                        located.blit()
                        pygame.display.flip()
                        pygame.time.delay(2500)

                        self.intro = False
                        # Create an instance to store game statistics,
                        #   and create a scoreboard.
                        self.stats = GameStats(self)
                        self.sb = Scoreboard(self)
                        self.sb.prep_name(self.name)
                        self.run_game()

                elif evt.type == pygame.KEYUP:
                    backspace_pressed = 0


                elif evt.type == pygame.QUIT:
                    sys.exit()

                self.intro_screen.fill((0, 0, 0))
                intro_text_1 = TextBlit(self, "What is your name?")
                intro_text_1.rect.y -= intro_text_1.rect.height *2
                intro_text_1.blit()

                name_block = TextBlit(self, self.name)
                name_block.rect.center = self.intro_screen_rect.center 
                name_block.rect.y += name_block.rect.y /4

                if self.name:
                    last_letter = self.name[-1]
                else:
                    last_letter = self.name
                last_letter_block = TextBlit(self, last_letter)
                last_letter_block.rect.right = name_block.rect.right
                last_letter_block.rect.bottom = name_block.rect.bottom

                intro_ship = self.ship
                intro_ship_rect = intro_ship.rect
                intro_ship_rect.centerx = last_letter_block.rect.centerx
                intro_ship_rect.y = name_block.rect.y + 100

                self.intro_screen.blit(intro_ship.blackship, intro_ship_rect)
                if letter_bullet:
                    letter_bullet.rect.midtop = intro_ship_rect.midtop
                while letter_bullet:
                    if letter_bullet.rect.top >= last_letter_block.rect.bottom:
                        letter_bullet.draw_bullet()
                        letter_bullet.update()
                        pygame.display.flip()
                    else:
                        letter_bullet = ""

                name_block.blit()

                pygame.display.flip()

    def run_game(self):
        """Start the main loop for the game."""
        # Set_intro
        if self.intro:
            self.game_intro()

        else:
            while True:
                
                self._check_events()

                if self.stats.game_active:
                    self.ship.update()
                    self._update_bullets()
                    self._update_aliens()

                self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_play_button(mouse_pos)
            

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.stats.save_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_m:
            self.sfx.music_on *= -1
            self.sfx.music_paused()
        elif self.stats.game_active:
            if event.key == pygame.K_p:
                self._pause_game()
        self.sfx.check_combo(event.key)

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            self.sfx.bullet_sound()
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                 self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            self.sfx.alien_hit_sound()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.sfx.levelup_sound()
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
          then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard and play sound.
            self.sfx.crash_sound()
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            
            # Pause.
            sleep(0.5)
        else:
            self.sfx.game_over_sound()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _pause_game(self):

        self.pause = True
        largeText = pygame.font.SysFont(None,115)
        paused_image = largeText.render("Paused", True,
            self.sb.text_color, self.settings.bg_color)
        self.paused_rect = paused_image.get_rect()
        self.paused_rect.center = ((self.settings.screen_width/2),(self.settings.screen_height/4))
        self.screen.blit(paused_image, self.paused_rect)


        # Show the mouse cursor.
        pygame.mouse.set_visible(True)



        while self.pause:

            self.font = pygame.font.SysFont(None, 48)
            self.top_ten_list = self.stats.top_ten()
            self.top_ten_list_reversed = [ele for ele in reversed(self.top_ten_list)]
            position_y = 1
            for entry in self.top_ten_list_reversed:

                self.entry_image = self.font.render(entry, True, (0, 0, 0), self.settings.bg_color)
                
                # Position the level below the score.
                self.entry_rect = self.entry_image.get_rect()
                self.entry_rect.top = self.sb.ship.rect.bottom 
                self.entry_rect.y = self.entry_rect.y * position_y
                self.entry_rect.x = 10

                # Blit to screen
                self.screen.blit(self.entry_image, self.entry_rect)
                position_y += 1

            mouse_pos = pygame.mouse.get_pos()
            self.check_button_hover(self.continue_button)
            self.check_button_hover(self.quit_button)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stats.save_high_score()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.stats.save_high_score()
                        sys.exit()
                    elif event.key == pygame.K_p:
                        self.pause = False
                    elif event.key == pygame.K_m:
                        self.sfx.music_on *= -1
                        self.sfx.music_paused()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._check_pause_buttons(mouse_pos)
           
            pygame.display.update()

    def _check_pause_buttons(self, mouse_pos):
        """Un-Pause game when the player clicks Continue."""
        continue_button_clicked = self.continue_button.rect.collidepoint(mouse_pos)
        if continue_button_clicked:
            # Un-pause the game.
            self.pause = False
        quit_button_clicked = self.quit_button.rect.collidepoint(mouse_pos)
        if quit_button_clicked:
            # Quit the game
            self.stats.save_high_score()
            sys.exit()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)
 
    def check_button_hover(self, button):
        """Check if mouse is hovering button and change color of button"""
        mouse_pos = pygame.mouse.get_pos()
        button_hover = button.rect.collidepoint(mouse_pos)
        if button_hover:
            button.button_color = (20, 20, 200)
        elif button_hover == False:
            button.button_color = button.init_button_color
        button.draw_button()
            
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.sb.control_image, self.sb.control_rect)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.check_button_hover(self.play_button)

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
