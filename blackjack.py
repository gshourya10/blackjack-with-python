# BLACKJACK WITH A FEW CHANGES IN RULES
# ------------------------
# created by Shourya Gupta
# -------4/28/2020--------
# ------------------------
# DOES NOT HAVE FEATURES LIKE INSURANCE, SPLIT ETC. YET
# AN OPTIONAL FEATURE IS MENTIONED IN THE BLOCK OF THE GAME EXECUTION CODE

import random
from time import sleep

card_group = {1: "clubs", 2: "hearts", 3: "spades", 4: "diamonds"}


class CardGroupError(Exception):
    pass


class FaceValueError(Exception):
    pass


# creating a card object which has two attributes: face value and card_group
# face value represents the true value of the card in game
# card_group represents the set a card belongs to

class Card:
    def __init__(self, face_value, group):
        # face value represents the the actual value of the card in integer
        if face_value > 10:
            raise FaceValueError("Face value cannot be greater than 10")
        self.face_value = face_value
        # group represents spades, hearts, diamonds and clubs in string
        if group != "spades" and group != "clubs" and group != "diamonds" and group != "hearts":
            raise CardGroupError("Card group is invalid")
        self.group = group.lower()

    def __str__(self):
        return f"Card: {self.face_value} of {self.group}"


class FaceCard(Card):
    def __init__(self, group, face):
        super().__init__(10, group)
        # face represents J for joker, Q for king, K for king
        self.face = face.upper()

    def __str__(self):
        return f"Card: {self.face} of {self.group}"


# creates a deck of 52 cards as seen in the real world
class Deck(list):
    def __init__(self):
        self.deck = []
        for i in range(1, 5):
            for j in range(1, 11):
                temp = Card(j, card_group[i])
                self.deck.append(temp)

            self.deck.append(FaceCard(card_group[i], "J"))
            self.deck.append(FaceCard(card_group[i], "Q"))
            self.deck.append(FaceCard(card_group[i], "K"))

    def __len__(self):
        return len(self.deck)

    def __getitem__(self, item):
        return self.deck[item]


# creates a player object which in this will be the human player
# bet method is used to bet in the game where the betting amount is returned
# bet_lost is the method which is called when the player loses the game
class Player:
    def __init__(self, amount, name):
        self.name = name
        self.amount = amount

    def bet(self):
        while True:
            bet_amt = int(input(f"\n{self.name} enter your bet: "))
            if bet_amt > self.amount:
                print(f"\nEnter an amount within {self.amount}")
            else:
                return bet_amt

    def bet_lost(self, bet_amount):
        if self.amount < bet_amount:
            print(f"{self.name} has gone bankrupt. Can't play further!")
        else:
            self.amount -= bet_amount

    def __str__(self):
        return f"Player Name: {self.name}\nAmount: {self.amount}"


# this function draws two random cards for the player and the dealer in the beginning of the game
# uses the random import
def draw_cards(deck_temp):
    random.seed()
    card1 = random.choice(deck_temp)
    random.seed()
    card2 = random.choice(deck_temp)
    cards = [card1, card2]
    return cards


class Dealer:
    def __init__(self):
        self.name = "Computer"

    def __str__(self):
        return "Computer Dealer"


# draws a random card from the deck
def hit(deck_temp):
    random.seed()
    return random.choice(deck_temp)


# print the deck which is taken as an argument
def show(deck2):
    for card in deck2:
        print(card)


# returns the total sum of the face value of the cards of the deck which is taken as an argument
# ace card can be treated as face value of 1 or 11 whichever is favourable
def total_sum(deck3):
    total = 0
    for card in deck3:
        total += card.face_value

    for card in deck3:
        if card.face_value == 1:
            if (21 - total > 11 - total) and 11 - total >= 0:
                total += 10

    return total


# determines which player wins the bet
# takes four arguments: the decks and instances of the two player and a rev variable
# rev variable shows the status of revelation of the face down card of the dealer
# if the card is not yet revealed, rev is false hence any calculation of win won't occur which requires the second card
# HP token stands for human player and is returned if the same wins
# CD token stands for computer dealer and is returned if the same wins
def win(player_1, player_1_cards, player_2, player_2_cards, rev):
    if not rev:
        if total_sum(player_1_cards) == 21:
            print(f"{player_1.name} wins the bet.")
            player_1.amount += bet_amount
            print(f"Updated amount for {player_1.name} is {player_1.amount}")
            return "HP"
        if total_sum(player_2_cards) == 21:
            print(f"{player_2.name} wins the bet.")
            player_1.bet_lost(bet_amount)
            print(f"Updated amount for {player_1.name} is {player_1.amount}")
            return "CD"
    elif total_sum(player_1_cards) == 21 or \
            21 - total_sum(player_1_cards) < 21 - total_sum(player_2_cards) \
            or total_sum(player_2_cards) > 21:
        print(f"{player_1.name} wins the bet.")
        player_1.amount += bet_amount
        print(f"Updated amount for {player_1.name} is {player_1.amount}")
        return "HP"
    elif total_sum(player_2_cards) == 21 or \
            21 - total_sum(player_2_cards) < 21 - total_sum(player_1_cards) \
            or total_sum(player_1_cards) > 21:
        print(f"{player_2.name} wins the bet.")
        player_1.bet_lost(bet_amount)
        print(f"Updated amount for {player_1.name} is {player_1.amount}")
        return "CD"
    else:
        return None


# checks if any player busts in the middle of the round
# HP token stands for human player and is returned if the same busts
# CD token stands for computer dealer and is returned if the same busts
def bust(plyr_1_cards, plyr_2_cards):
    if total_sum(plyr_1_cards) > 21:
        print(f"{player1.name} busts")
        player1.bet_lost(bet_amount)
        print(f"Updated amount of {player1.name} is {player1.amount}")
        return "HP"
    if total_sum(plyr_2_cards) > 21:
        print(f"{comp_dealer.name} busts")
        player1.amount += bet_amount
        print(f"Updated amount of {player1.name} is {player1.amount}")
        return "CD"
    else:
        return None


# this function is used to ask if the current player wants to hit or stay
# takes four arguments: current player, its deck, universal deck and the fourth optional argument
# the optional argument is used for the computer dealer to make decision whether to hit or stay
# by using the optional argument which is the human player deck when the function is called for computer dealer
# checks if the dealer is losing to the player in the round and takes the decision
def hit_or_stay(player, deck_of_player, game_deck, deck_of_player_2=None):
    if deck_of_player_2 is None:
        deck_of_player_2 = []
    while True:
        if isinstance(player, Player):
            if total_sum(deck_of_player) > 21:
                break
            choice_ = input("Enter H for hit and S for stay: ")
            choice_ = choice_.upper()
            if choice_ != "H" and choice_ != "S":
                print("Invalid choice!")
            elif choice_ == "H":
                print("Drawing another card from the deck...")
                deck_of_player.append(hit(game_deck))
                show(deck_of_player)
            else:
                break
        elif 21 - total_sum(deck_of_player) > 21 - total_sum(deck_of_player_2) or \
                total_sum(deck_of_player) == total_sum(deck_of_player_2):
            sleep(2)
            print("Dealer decides to hit.")
            deck_of_player.append(hit(game_deck))
            show(deck_of_player)
        elif 21 - total_sum(deck_of_player) > 5:
            sleep(2)
            print("Dealer decides to hit.")
            deck_of_player.append(hit(game_deck))
            show(deck_of_player)
        elif total_sum(deck_of_player) == 21 or total_sum(deck_of_player) > 21:
            break
        else:
            print("Dealers stays")
            break


# used to ask if the player wants to play another round
#  takes two decks as arguments and clears the existing data in them before starting the next round
def replay(p1_cards, p2_cards):
    rep = input("Do you want to replay?\n Enter Y/N: ")
    rep = rep.upper()
    if rep == "Y":
        p1_cards.clear()
        p2_cards.clear()
        return True
    else:
        return False


print("WELCOME TO THE ROYALE CASINO")
print("-----------------------------\n\n")
temp_name = input("Enter your name: ")
temp_name = temp_name.title()
temp_amount = int(input("Enter your total amount: "))
player1 = Player(temp_amount, temp_name)
comp_dealer = Dealer()
print("\nThe participants are: ")
print(player1)
print("\n")
print("Dealer:", comp_dealer)

while True:
    revelation = False
    deck1 = Deck()
    bet_amount = player1.bet()
    print("\nDrawing Cards")
    print("--------------")
    sleep(2)
    player1_cards = draw_cards(deck1)
    comp_dealer_cards = draw_cards(deck1)
    print(f"\n{player1.name} has: ")
    show(player1_cards)
    print(f"\nThe face up card of dealer is: {comp_dealer_cards[0]}")
    print("\nTHE GAME BEGINS")
    print("---------------\n")
    print(f"{player1.name.upper()}'s HAND: ")
    if win(player1, player1_cards, comp_dealer, comp_dealer_cards, revelation) == "HP":
        if not replay(player1_cards, comp_dealer_cards):
            break
        else:
            continue

    hit_or_stay(player1, player1_cards, deck1)
    if bust(player1_cards, comp_dealer_cards) == "HP":
        if not replay(player1_cards, comp_dealer_cards):
            break
        else:
            continue

    if win(player1, player1_cards, comp_dealer, comp_dealer_cards, revelation) == "HP":
        if not replay(player1_cards, comp_dealer_cards):
            break
        else:
            continue

    print(f"\n{player1.name} decides to stay. Revealing dealer's face down card...")
    sleep(2)
    print(f"Dealer's face down card is: {comp_dealer_cards[1]}")
    print("\nDealer has: ")
    show(comp_dealer_cards)
    print("\nDEALER'S HAND: ")
    # optional feature below
    # if total_sum(comp_dealer_cards) < 16:
    #     print(f"{player1.name} wins as total of dealer's cards is less than 16")
    #     player1.amount += bet_amount
    #     print(f"Updated amount for {player1.name} is {player1.amount}")
    #     if not replay(player1_cards, comp_dealer_cards):
    #         break
    #     else:
    #         continue

    if win(player1, player1_cards, comp_dealer, comp_dealer_cards, revelation) == "CD":
        if not replay(player1_cards, comp_dealer_cards):
            break
        else:
            continue
    sleep(2)
    hit_or_stay(comp_dealer, comp_dealer_cards, deck1, player1_cards)
    sleep(2)
    revelation = True
    if bust(player1_cards, comp_dealer_cards) == "CD":
        if not replay(player1_cards, comp_dealer_cards):
            break
        else:
            continue

    if win(player1, player1_cards, comp_dealer, comp_dealer_cards, revelation) == "CD" or \
            win(player1, player1_cards, comp_dealer, comp_dealer_cards, revelation) == "HP":
        if not replay(player1_cards, comp_dealer_cards):
            break
        else:
            continue
