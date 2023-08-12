from oop import LetterGuesser


if __name__ == "__main__":
    word_list = ["kaimietis", "linas", "medis", "dramblys", "lietuva"]
    guesser = LetterGuesser(word_list)

    print("Welcome to the HANGMAN game!")
    while True:

        print("\nChoose an option:")
        print("1. Pick game level.")
        print("2. Player stats.")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nChoose a game lvl:")
            print("1. Child (Word with 5 letters)")
            print("2. Adult (Word with 8 letters)")
            print("3. Old Like Dust (Word with 10 letters)")
            print("0. Exit")

            choise = input("Enter your level choice: ")

            if choise == "0":
                break
            elif choise in ("1", "2", "3"):
                random_word = guesser.get_word()

                if choise == "1":
                    guesser.split_word(random_word)
                    underscore_str = guesser.display_word()
                    print("Word to guess:", underscore_str)

                while not guesser.check_win() and not guesser.check_loss():
                    guessed_letter = input("Guess a letter: ").lower()
                    if guessed_letter in guesser.guessed_letters:
                        print("You already guessed this letter. Try again.")
                    elif guessed_letter in guesser.letters:
                        guesser.guess_letter(guessed_letter)
                        print(f"Correct! '{guessed_letter}' is in the word.")
                        print("Current word:", guesser.display_word())
                    else:
                        remaining_attempts = guesser.count_left_attempts()
                        print(f"Sorry! '{guessed_letter}' is not in the word.")
                        print(f"You have {remaining_attempts} attempts left.")

                if guesser.check_win():
                    score = guesser.count_score()
                    print(
                        f"Congratulations! You guessed all the letters in the word. Your score: {score} of 100.")
                elif guesser.check_loss():
                    print(
                        "Sorry, you have used all your attempts. The word was:", random_word)

                guesser.guessed_letters.clear()
                guesser.attempts = 0

            else:
                print("\nInvalid level choice!")
        elif choice == "2":
            made_attempts = guesser.max_attempts - remaining_attempts
            if guesser.score is not None:
                print(
                    f"Score: {guesser.score}\nMade attempts: {made_attempts}")
            else:
                print("You haven't played any games yet.")

        elif choice == "0":
            break
        else:
            print("\nInvalid choice!")
