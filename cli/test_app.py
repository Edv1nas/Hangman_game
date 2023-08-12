import random


class WordSelector:
    def __init__(self, word_list):
        self.word_list = word_list

    def get_random_word(self):
        return random.choice(self.word_list)


class WordProcessor:
    def __init__(self, word):
        self.word = word.lower()
        self.letters = list(self.word)
        self.guessed_letters = set()

    def guess_letter(self, letter):
        self.guessed_letters.add(letter.lower())
        return letter.lower() in self.word

    def display_word(self):
        displayed_word = ""
        for letter in self.word:
            if letter in self.guessed_letters:
                displayed_word += letter + " "
            else:
                displayed_word += "_ "
        return displayed_word.strip()

    def check_win(self, guessed_letters):
        return all(letter in guessed_letters for letter in self.letters)

    def check_loss(self, attempts, max_attempts):
        return attempts >= max_attempts


class ScoreCalculator:
    def __init__(self, attempts, max_attempts):
        self.attempts = attempts
        self.max_attempts = max_attempts

    def count_made_attempts(self):
        self.attempts += 1
        return self.attempts

    def count_left_attempts(self):
        remain_attempts = self.max_attempts - self.attempts
        return remain_attempts

    def count_score(self):
        attempts_left = self.count_left_attempts()
        score = attempts_left * 10
        return score


class HangmanGame:
    def __init__(self, word_list, max_attempts=10):
        self.word_selector = WordSelector(word_list)
        self.max_attempts = max_attempts
        self.attempts = 0
        self.score_calculator = None
        self.word_processor = None
        self.guessed_letters = set()

        self.total_games_played = 0
        self.total_wins = 0
        self.total_losses = 0

    def start_game(self):
        word = self.word_selector.get_random_word()
        self.word_processor = WordProcessor(word)
        self.score_calculator = ScoreCalculator(
            self.attempts, self.max_attempts)

    def guess_letter(self, letter):
        if self.word_processor is None:
            raise Exception("Game has not started. Call start_game() first.")

        if letter in self.guessed_letters:
            return "Letter '{}' was already used.".format(letter)

        self.guessed_letters.add(letter)

        result = self.word_processor.guess_letter(letter)

        if not result:
            self.attempts = self.score_calculator.count_made_attempts()

        if self.word_processor.check_win(self.guessed_letters):
            return "win"

        if self.word_processor.check_loss(self.attempts, self.max_attempts):
            return "lose"

        return result

    def display_word(self):
        if self.word_processor is None:
            raise Exception("Game has not started. Call start_game() first.")
        return self.word_processor.display_word()

    def get_word(self):
        if self.word_processor is None:
            raise Exception("Game has not started. Call start_game() first.")
        return self.word_processor.word

    def get_total_games_played(self):
        return self.total_games_played

    def get_total_wins(self):
        return self.total_wins

    def get_total_losses(self):
        return self.total_losses

    def get_win_rate(self):
        if self.total_games_played == 0:
            return 0.0
        return (self.total_wins / self.total_games_played) * 100.0

    def get_score(self):
        if self.score_calculator is None:
            raise Exception("Game has not started. Call start_game() first.")
        return self.score_calculator.count_score()


def main():
    word_list = ["kaimietis", "medis", "dramblys"]
    hangman_game = HangmanGame(word_list)

    print("Welcome to Hangman!")

    while True:
        print("\nSelect an option:")
        print("1. Start a new game")
        print("2. User game stats")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            hangman_game.start_game()

            while True:
                if hangman_game.word_processor.check_win(hangman_game.guessed_letters):
                    print(
                        f"You win! The word was '{hangman_game.get_word()}'.")
                    break

                if hangman_game.word_processor.check_loss(hangman_game.attempts, hangman_game.max_attempts):
                    print(
                        f"You lose! The word was '{hangman_game.get_word()}'.")
                    break

                print("Current word:", hangman_game.display_word())
                print("Attempts left:", hangman_game.get_score() // 10)
                guess = input("Guess a letter: ").strip().lower()

                if len(guess) != 1 or not guess.isalpha():
                    print("Please enter a single letter.")
                    continue

                result = hangman_game.guess_letter(guess)

                if result == "Letter '{}' was already used.".format(guess):
                    print("You already guessed that letter. Try again.")
                elif result == "win":
                    print(
                        f"You win! The word was '{hangman_game.get_word()}'.")
                    break
                elif result == "lose":
                    print(
                        f"You lose! The word was '{hangman_game.get_word()}'.")
                    break
                else:
                    print(result)

        elif choice == "2":
            print(
                f"Total games played: {hangman_game.get_total_games_played()}")
            print(f"Total wins: {hangman_game.get_total_wins()}")
            print(f"Total losses: {hangman_game.get_total_losses()}")
            print(f"Win rate: {hangman_game.get_win_rate():.2f}%")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
