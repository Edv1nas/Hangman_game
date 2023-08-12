import random


class LetterGuesser:
    def __init__(self, word_list):
        self.word_list = word_list
        self.random_word = None
        self.letters = None
        self.guessed_letters = set()
        self.attempts = 0
        self.max_attempts = 10
        self.score = None

    def count_made_attempts(self):
        self.attempts += 1
        return self.attempts

    def count_left_attempts(self):
        remain_attempts = self.max_attempts - self.count_made_attempts()
        return remain_attempts

    def get_word(self):
        self.random_word = random.choice(self.word_list)
        return self.random_word

    def split_word(self, word):
        self.letters = list(word)
        return self.letters

    def guess_letter(self, guessed_letter):
        self.guessed_letters.add(guessed_letter)
        return guessed_letter in self.letters

    def display_word(self):
        if self.letters is None:
            return ""
        displayed_word = ""
        for letter in self.letters:
            if letter in self.guessed_letters:
                displayed_word += letter + " "
            else:
                displayed_word += "_ "
        return displayed_word.strip()

    def check_win(self):
        return set(self.random_word.lower()) == self.guessed_letters

    def check_loss(self):
        return self.attempts >= self.max_attempts

    def count_score(self):
        attempts_left = self.count_left_attempts()
        self.score = attempts_left * 10
        return self.score
