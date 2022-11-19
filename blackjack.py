import random
from time import sleep
from os import system



suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
          'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':1}
chips = (5, 10, 20, 50, 100)
player = ''

class Card:
    '''
    Define the card's suit (Hearts, Diamonds, Spades, Clubs)
    and rank, value is determined automatically via global dictionary
    '''

    def __init__(self,suit,rank):
        # Card class has suit, rank, and value
        self.suit = suit.capitalize()
        self.rank = rank.capitalize()
        self.value = values[rank.capitalize()]

    def __str__(self):
        # Print function
        return self.rank + " of " + self.suit

class Deck:
    '''
    Create the deck of cards, with suits and ranks
    '''

    def __init__(self):
        # Initialize an empty deck of cards as a list
        self.all_cards = []

        # Loop through all suits
        for suit in suits:
            # Loop through all ranks
            for rank in ranks:
                self.all_cards.append(Card(suit,rank))

    def shuffle(self):
        # Shuffle the deck of cards
        random.shuffle(self.all_cards)

    def deal_one(self):
        # Deal one card from the deck
        return self.all_cards.pop()

class Player():
    '''
    Create a player class consisting of the name, cards owned,
    and functions to remove and add cards, and print total amount of cards
    '''

    def __init__(self, name):
        # Player class has name money chips and all_cards list
        self.name = name.title()
        self.all_cards = []
        self.money = 10000
        self.chips = {5:0, 10:0, 20:0, 50:0, 100:0}

    def add_cards(self, new_cards):
        # Adding a card to the player's deck
        return self.all_cards.append(new_cards)

    def func_chips_value(self):
        # Find total value of chips with player
        chips_value = 0
        for chip in chips:
            chips_value += self.chips[chip] * chip
        return chips_value
    
    def money_to_chips(self, amount):
        print("Pending transaction, please wait...")
        sleep(3)
        AMOUNT = amount
        try:
            for chip in chips[::-1]:
                self.chips[chip] += int(amount / chip)
                amount = amount % chip
            self.money -= AMOUNT
            return(f"Success! You now have {self.chips[100]} 100s, {self.chips[50]} 50s, {self.chips[20]} 20s, {self.chips[10]} 10s, {self.chips[5]} 5s.\n${AMOUNT} has been deducted from your bank account. You have ${self.money} remaining.")
        except:
            print("Something went wrong with buying chips!")
            quit()
        
    def chips_to_money(self, amount, type):
        print("Pending transaction, please wait...")
        sleep(3)
        self.chips[type] -= int(amount)
        self.money += int(amount * type)
        return(f"Success! You have sold {amount} {type}s. You have {self.chips[type]} {type}s remaining. ${amount * type} has been returned to your bank account. You now have ${self.money}.")

    def chips_to_bet(self,bet):
        chips_value = self.func_chips_value()
        to_be_returned = chips_value - bet
        for chip in chips[::-1]:
            self.chips[chip] = int(to_be_returned / chip)
            to_be_returned %= chip
            if to_be_returned == 0:
                break
        print("Successfully submitted chips.")

    def win(self,bet):
        for chip in chips[::-1]:
            self.chips[chip] += int(bet / chip)
            bet %= chip

    def __str__(self):
        print("\nPending request, please wait...")
        sleep(3)
        print(f"You have the following chips:")
        for chip in chips[::-1]:
            print(f"{self.chips[chip]} {chip}s")
        return(f"You have ${self.money} in your bank account.")

def bet_amount(player):
    # Ask for bet amount
    while True:
        if player.chips[100] == 0 and player.chips[50] == 0 and player.chips[20] == 0 and player.chips[10] == 0 and player.chips[5] == 0:
            print("Buy some chips before playing!")
            return main()
        try:
            print(f"You have the following chips:")
            for chip in chips[::-1]:
                print(f"{player.chips[chip]} {chip}s")
            bet = int(input(f"How much do you want to bet? $"))
        except ValueError:
            print("Please enter a valid integer multiple of 5.")
            continue
        if bet > player.func_chips_value():
            print("You don't have enough chips! Buy more chips or select a smaller amount.")
            continue
        elif bet == 0:
            print("You cannot bet nothing.")
        elif bet < 0:
            print("You cannot bet a negative amount.")
        else:
            print(f"Withdrawing ${bet} from your chip balance, please wait...")
            player.chips_to_bet(bet)
            sleep(3)
            print(f"{player}\nBeginning new game in 3 seconds.")
            sleep(3)
            system('clear')
            game(player, bet)

def game(player, bet):
# Game function

    # Initialize my_deck and shuffle it
    my_deck = Deck()
    my_deck.shuffle()
    
    # Set round to 0
    round = 0

    # Initialize player's cards and dealer's cards
    player_cards = []
    dealer_cards = []

    # Deal two cards to both
    for x in range(2):
        player_cards.append(my_deck.deal_one())
        dealer_cards.append(my_deck.deal_one())

    # Infinite loop to represent rounds
    while True:
        
        # List round number
        round += 1
        print(f"\nRound {round}:")

        # List all current info to player
        print("You have the following cards:",end='')
        for card in player_cards:
            print(f" {card} |",end='')
        print(f"\nYou have ${player.money} in the bank.")
        print(f"The dealer has two cards, one of which is {dealer_cards[0]}.")
        
        # Check if player wants to hit or stay
        while True:
            response = input("Would you like to hit (receive a card) or stay (stop receiving cards)? ").lower()
            if response == "hit" or response == "stay" or response == "h" or response == "s":
                break
            print("Invalid response! Try again.\n")
        
        # Player has chosen to end the game
        if response == "stay" or response == "s":
            break

        # Add one card to player's deck
        player_cards.append(my_deck.deal_one())

        value = 0
        for card in range(len(player_cards)):
            value += player_cards[card].value
        if value > 21:
            print("\nYou have the following cards:",end='')
            for card in player_cards:
                print(f" {card} |",end='')
            print(f"\nTHE VALUE OF YOUR CARDS IS {value}, WHICH IS MORE THAN 21. YOU LOSE!")
            sleep(2)
            return main()
        
    player_total_value = 0
    print("\nYou have ended the round! Calculating total value...")
    sleep(3)
    for card in range(len(player_cards)):
        if player_cards[card].value == 1:
            while True:
                try:
                    response = int(input("Hold on! We found an Ace card in your deck! Would you like it to be counted as 1 or 11? "))
                    if response == 1 or response == 11:
                        break
                except:
                    print("Invalid response! Try again.")
            player_total_value += response
        else:
            player_total_value += player_cards[card].value
    print(f"The total value of your cards is {player_total_value}! Beginning the dealer's game...")
    sleep(3)

    round = 0

    # Infinite loop to represent rounds
    while True:
        
        # List round number
        round += 1
        print(f"\nRound {round}:")

        # List all current info to player
        print(f"{player.name}'s cards have a total value of {player_total_value}.")
        print("The dealer has the following cards:",end='')
        for card in dealer_cards:
            print(f" {card} |",end='')
        
        # If random number is > 5, the dealer "stays"
        value = random.randint(0, 10)
        sleep(2)
        if value > 5:
            print("\nThe dealer has decided to stay!")
            break
        sleep(2)
        print("\nThe dealer has decided to hit! Drawing one card.")

        # Add one card to dealer's deck
        dealer_cards.append(my_deck.deal_one())

        total_value = 0
        for card in range(len(dealer_cards)):
            total_value += dealer_cards[card].value
        if total_value > 21:
            print("\nThe dealer has the following cards:",end='')
            for card in dealer_cards:
                print(f" {card} |",end='')
            print(f"\nTHE VALUE OF THE DEALER'S CARDS IS {total_value}, WHICH IS MORE THAN 21. YOU WIN!")
            player.win(bet*2)
            print(f"Chips with the value of ${bet*2} have been deposited in your chip balance.\n")
            sleep(2)
            return main()

    dealer_total_value = 0
    print("\nThe dealer has ended the round! Calculating total value...")
    sleep(3)
    for card in range(len(dealer_cards)):
        if dealer_cards[card].value == 1:
            while True:
                try:
                    response = int(input("Hold on! We found an Ace card in the dealer's deck! Would you like it to be counted as 1 or 11? "))
                    break
                except:
                    print("Invalid response! Try again.")
            dealer_total_value += response
            break
        dealer_total_value += dealer_cards[card].value
    print(f"The total value of the dealer's cards is {dealer_total_value}!")

    print("\nNow that both games have ended, let's see who's closer to 21...")
    sleep(3)

    print(f"Your cards have a value of {player_total_value}...")
    sleep(2)
    print(f"Dealer's cards have a value of {dealer_total_value}...")
    sleep(2)
    if dealer_total_value > player_total_value:
        print("You LOSE! :(")
        sleep(2)
        return main()
    elif dealer_total_value < player_total_value:
        player.win(bet*2)
        print(f"Chips with the value of ${bet*2} have been deposited in your chip balance.\n")
        sleep(2)
        return main()
    else:
        player.win(bet)
        print(f"It's a tie! ${bet} has been returned to your chip balance.")
        sleep(2)
        return main()

def main():
    
    global player
    if player == '':
        system('cls||clear')
        print("\nWelcome to Blackjack! The purpose of the game is to bet on getting closer to a sum of 21 than the dealer. Good luck!\n")

        # Ask user for input on player's name
        player_name = input("What is your name? ")
        # Initialize first player
        player = Player(player_name)

    # Loop for asking player what they would like to do
    while True:
        try:
            print(f"\nHello {player.name}. What would you like to do: 1 Purchase chips | 2 Sell chips | 3 Begin a new game | 4 Balance Check | 5 Quit")
            response = int(input("Response: "))
        except:
            print("Please enter a valid number to respond: 1 / 2 / 3 / 4 / 5")
            continue
        if response == 1:
            while True:
                try:
                    print(f"You have ${player.money}.")
                    response_buy_chips = int(input("In multiples of 5 only, how many chips would you like to buy? "))
                except:
                    print("Please enter a valid integer amount in multiples of 5.")
                    continue
                if response_buy_chips > player.money:
                    print("You don't have enough money. Please try again.")
                    continue
                elif response_buy_chips % 5 == 0:
                    print(player.money_to_chips(response_buy_chips))
                    return main()
        elif response == 2:
            while True:
                try:
                    response_sell_type = int(input("Which type of chip would you like to sell: 100 / 50 / 20 / 10 / 5? "))
                except:
                    print("Please enter a valid integer amount.")
                    continue
                if response_sell_type == 100 or 50 or 20 or 10 or 5:
                    while True:
                        try:
                            response_sell_amount = int(input(f"You currenty have {player.chips[response_sell_type]} {response_sell_type}s. How many {response_sell_type}s chips would you like to sell? "))
                        except:
                            print("Please enter a valid integer amount.")
                            continue
                        if response_sell_amount < 1:
                            print("Please enter a positive amount.")
                            continue
                        elif player.chips[response_sell_type] < response_sell_amount:
                            response_continue_selling = input("You don't have enough chips! Would you like to try again (Y or N)? ").upper()
                            if response_continue_selling == 'Y':
                                continue
                            elif response_continue_selling == 'N':
                                return main()
                        elif player.chips[response_sell_type] >= response_sell_amount:
                            print(player.chips_to_money(response_sell_amount, response_sell_type))
                            return main()
        elif response == 3:
            bet_amount(player)
        elif response == 4:
            print(player)
            return main()
        elif response == 5:
            quit()
        else:
            print("Please enter a valid number to respond: 1 / 2 / 3 / 4 / 5")

main()
