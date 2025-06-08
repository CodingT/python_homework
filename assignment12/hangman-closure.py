def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter)

        displayed_word = []
        for char in secret_word:
            if char in guesses:
                displayed_word.append(char)
            else:
                displayed_word.append("_")

        print(f"Current word: {displayed_word}")
        print(f"Letters guessed: {', '.join(guesses)}")

        all_guessed = all(char in guesses for char in secret_word)
        return all_guessed

    return hangman_closure


def play_hangman():
    secret_word = input("Enter the secret word: ")

    game = make_hangman(secret_word)

    while True:
        guess = input("Guess a letter: ").lower()

        solved = game(guess)

        if solved:
            print(f"Congratulations! You guessed the word: {secret_word}")
            break


if __name__ == "__main__":
    play_hangman()
