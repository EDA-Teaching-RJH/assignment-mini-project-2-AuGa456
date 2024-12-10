import random
import re
import os

# Card class to represent individual cards
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        if rank in ['Jack', 'Queen', 'King']:
            self.value = 10
        elif rank == 'Ace':
            self.value = 11
        else:
            self.value = int(rank)

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Deck class to represent a deck of 52 cards
class Deck:
    def __init__(self):
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

# Blackjack game class
class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_winnings = 0
        self.load_winnings()

    def load_winnings(self):
        """Load the player's total winnings from a file."""
        if os.path.exists('winnings.txt'):
            with open('winnings.txt', 'r') as file:
                try:
                    self.player_winnings = int(file.read().strip())
                except ValueError:
                    self.player_winnings = 0
        else:
            self.player_winnings = 0

    def save_winnings(self):
        """Save the player's total winnings to a file."""
        with open('winnings.txt', 'w') as file:
            file.write(str(self.player_winnings))

    def deal_card(self, hand):
        """Deal a card to the specified hand."""
        card = self.deck.draw_card()
        hand.append(card)
        return card

    def calculate_hand_value(self, hand):
        """Calculate the total value of a hand."""
        value = sum(card.value for card in hand)
        # Adjust for Aces (Ace can be 1 or 11)
        aces = [card for card in hand if card.rank == 'Ace']
        while value > 21 and aces:
            value -= 10
            aces.pop()
        return value

    def display_hand(self, hand, player):
        """Display a player's or dealer's hand."""
        hand_value = self.calculate_hand_value(hand)
        hand_str = ', '.join([str(card) for card in hand])
        print(f"{player}'s hand: {hand_str} (Value: {hand_value})")
        return hand_value

    def player_turn(self):
        """Handle the player's turn (hit or stand)."""
        while True:
            print("\nYour hand:", [str(card) for card in self.player_hand])
            print(f"Your total hand value: {self.calculate_hand_value(self.player_hand)}")
            move = input("Do you want to [h]it or [s]tand? ").lower()
            
            if move == 'h':
                card = self.deal_card(self.player_hand)
                print(f"You drew: {card}")
                if self.calculate_hand_value(self.player_hand) > 21:
                    print(f"Your hand value is {self.calculate_hand_value(self.player_hand)}. You busted!")
                    return False
            elif move == 's':
                return True
            else:
                print("Invalid input. Please enter 'h' for hit or 's' for stand.")

    def dealer_turn(self):
        """Handle the dealer's turn (hit until hand value is 17 or more)."""
        while self.calculate_hand_value(self.dealer_hand) < 17:
            print("\nDealer's turn:")
            card = self.deal_card(self.dealer_hand)
            print(f"Dealer drew: {card}")
        return self.calculate_hand_value(self.dealer_hand)

    def play_round(self):
        """Play one round of Blackjack."""
        self.player_hand = [self.deal_card([]), self.deal_card([])]
        self.dealer_hand = [self.deal_card([]), self.deal_card([])]

        print("\nWelcome to Blackjack!")
        self.display_hand(self.dealer_hand[:1], "Dealer")  # Show dealer's one card
        self.display_hand(self.player_hand, "Player")  # Show player's cards

        # Player's turn
        if not self.player_turn():
            return -1  # Player busted

        # Dealer's turn
        dealer_value = self.dealer_turn()
        print(f"\nDealer's hand value: {dealer_value}")
        
        # Calculate final results
        player_value = self.calculate_hand_value(self.player_hand)
        if dealer_value > 21:
            print(f"Dealer busts! You win this round!")
            return 1
        elif player_value > dealer_value:
            print(f"You win this round!")
            return 1
        elif player_value < dealer_value:
            print(f"Dealer wins this round!")
            return -1
        else:
            print(f"It's a tie!")
            return 0

    def update_winnings(self, result):
        """Update the player's total winnings."""
        if result == 1:
            self.player_winnings += 10
        elif result == -1:
            self.player_winnings -= 10

    def play(self):
        """Start the game loop."""
        while True:
            result = self.play_round()
            self.update_winnings(result)

            print(f"\nYour total winnings: {self.player_winnings}")
            self.save_winnings()

            play_again = input("\nDo you want to play again? [y/n]: ").lower()
            if play_again != 'y':
                break

# Main game entry point
if __name__ == "__main__":
    game = BlackjackGame()
    game.play()
