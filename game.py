import random
import re
from datetime import date

class Player:
    def __init__(self):
        self.player_name = ""

    def validate_name(self, name):
        if not re.search(r"^[a-zA-ZåäöÅÄÖ]+ [a-zA-ZåäöÅÄÖ]+$", name):
            return False, "Name can only contain letters, å, ä, ö and one space between first and last name."
        self.player_name = name
        return True, ""

class Game:
    def __init__(self):
        self.lucky_list = []
        self.lucky_number = 0
        self.shorter_lucky_list = []
        self.tries_count = 0
        self.full_lucky_list = []

    def generate_lucky_list(self):
        return [random.randint(0, 100) for _ in range(9)]

    def generate_lucky_number(self):
        return random.randint(0, 100)

    def generate_shorter_list(self, lucky_number, lucky_list):
        min_val = lucky_number - 10
        max_val = lucky_number + 10
        return [x for x in lucky_list if min_val <= x <= max_val]

    def check_length_list(self, a_list):
        return len(a_list) <= 2

    def initialize_game(self):
        self.tries_count = 0
        self.lucky_list = self.generate_lucky_list()
        self.lucky_number = self.generate_lucky_number()
        self.lucky_list.append(self.lucky_number)
        random.shuffle(self.lucky_list)
        self.full_lucky_list = list(self.lucky_list) # Store the original full list
        self.shorter_lucky_list = self.generate_shorter_list(self.lucky_number, self.lucky_list)