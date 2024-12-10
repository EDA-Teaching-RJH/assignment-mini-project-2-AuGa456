import random
import re
import os

# Define the class for the number guessing game
class NumberGuessGame:
    def __init__(self):
        self.target_number = random.randint(1, 100)
        self.max_attempts = 5
        self.attempts = 0
        self.score = 0
        self.load_score()

    def load_score(self):
        """Load the score from a file."""
        if os.path.exists('score.txt'):
            with open('score.txt', 'r') as f:
                try:
                    self.score = int(f.read().strip())
                except ValueError:
                    self.score = 0
        else:
            self.score = 0

    def save_score(self):
        """Save the current score to a file."""
        with open('score.txt', 'w') as f:
            f.write(str(self.score))

    def is_valid_guess(self, guess):
        """Check if the guess is a valid integer using regular expressions."""
        return re.match(r'^\d+$', guess) is not None

    def play(self):
        """Start the game loop."""
        print(f"Welcome to the Number Guessing Game!")
        print(f"Guess the number between 1 and 100. You have {self.max_attempts} attempts.")
        while self.attempts < self.max_attempts:
            guess = input(f"Attempt {self.attempts + 1}/{self.max_attempts} - Your guess: ")

            # Check if the guess is valid
            if not self.is_valid_guess(guess):
                print("Invalid guess! Please enter a positive integer.")
                continue

            guess = int(guess)
            self.attempts += 1

            if guess < self.target_number:
                print("Too low!")
            elif guess > self.target_number:
                print("Too high!")
            else:
                print(f"Congratulations! You've guessed the correct number {self.target_number}!")
                self.score += 1
                break

        if self.attempts == self.max_attempts and guess != self.target_number:
            print(f"Sorry, you've used all your attempts. The correct number was {self.target_number}.")

        print(f"Your score: {self.score}")
        self.save_score()

# Main function to run the game
if __name__ == "__main__":
    game = NumberGuessGame()
    game.play()
