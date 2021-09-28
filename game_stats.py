import json

class GameStats:
    """Track statistics for Alien Invasion."""
    
    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start game in an inactive state.
        self.game_active = False

        self.name = ai_game.name

        self.hsdict = self.high_score_dict()

        # High score should never be reset.
        self.high_score = self.read_high_score()

        top_ten = self.top_ten()
        
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def read_high_score(self):
        """read the high score to initialise the current high score"""
        dict_len = len(self.high_score_dict())
        high_score = 0
        for key in range(dict_len):
            if int(self.high_score_dict_value(key)) >= high_score:
                high_score = int(self.high_score_dict_value(key))
        return high_score


    def save_high_score(self):
        """Save high score when ending a game"""
        with open("high_score.txt", 'w') as file:
            if self.name in self.hsdict.keys():
                if int(self.hsdict[self.name]) < self.high_score:
                    self.hsdict[self.name] = self.score
                    json.dump(self.hsdict, file, indent=4)
            else:
                self.hsdict[self.name] = self.score
                json.dump(self.hsdict, file, indent=4)

    def high_score_dict(self):
        """Loads the high score from previous save"""
        with open("high_score.txt") as file:
            try:
                high_score_dict = json.load(file)
                return high_score_dict
            except:
                return {}

    def high_score_dict_value(self,score_entry):
        """Create a list from the dict and return the value of entry"""
        key_list = []
        score_list = self.high_score_dict()
        try:
            for key in score_list.keys():
                key_list.append(key)
            score_key = key_list[score_entry]
            score_value = score_list[score_key]
            return score_value
        except:
            return 0

    def top_ten(self):
        """Sort high scores into order then append the 10 highest scores to 
        a list of dicts """
        score_dict = self.high_score_dict()
        sorted_dict = dict(sorted(score_dict.items(), 
                    key=lambda item: item[1]))

        high_score_roll = []

        sorted_dict_len = len(sorted_dict.keys())
        if sorted_dict_len <= 10:
            top = sorted_dict_len
        else:
            top = 10

        name_key = []
        for key in sorted_dict.keys():
            name_key.append(key)

        # The range of keys to be used for the top 10
        range_key = sorted_dict_len - top
            
        while top >= 1: 
            # append formated scores for top 10 list
            for name in name_key[range_key:]:
                high_score_roll.append(f"{top}: {name}: {sorted_dict[name]}")
                top -= 1

        return high_score_roll


