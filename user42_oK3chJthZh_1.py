# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
result = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        ans = "Hand contains "
        for i in range(len(self.cards)):
            ans += str(self.cards[i]) + " "
        return ans

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        hand_value = 0
        ace = False
        for i in range(len(self.cards)):
            hand_value += VALUES[self.cards[i].get_rank()]
            if self.cards[i].get_rank() == 'A':
                ace = True
        if ace and hand_value + 10 <= 21:
            hand_value += 10
        return hand_value

    def draw(self, canvas, pos):
        for i in range(len(self.cards)):
            self.cards[i].draw(canvas, pos)
            pos[0] += CARD_SIZE[0] + 20
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def __str__(self):
        ans = "Deck contains "
        for i in range(len(self.cards)):
            ans += str(self.cards[i]) + " "
        return ans

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score, result
    if in_play:
        result = "You lost the round"
        score -= 1
    else:
        result = ""
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    for i in range(2):
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
    outcome = "Hit or stand?"
    in_play = True

def hit():
    global outcome, in_play, score, result
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            result = "You have busted"
            outcome = "New deal?"
            in_play = False
            score -= 1

def stand():
    global outcome, in_play, score, result
    if in_play:
        if player_hand.get_value() > 21:
            result = "You have busted"
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            result = "Dealer has busted"
            score += 1
        else:
            if player_hand.get_value() <= dealer_hand.get_value():
                result = "Dealer wins"
                score -= 1
            else:
                result = "You win"
                score += 1
        in_play = False
        outcome = "New deal?"

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    player_hand.draw(canvas, [80, 400])
    dealer_hand.draw(canvas, [80, 200])
    canvas.draw_text("Blackjack", (100, 100), 35, 'Aqua')
    canvas.draw_text("Dealer", (80, 180), 25, 'Black')
    canvas.draw_text("Player", (80, 380), 25, 'Black')
    canvas.draw_text(outcome, (300, 380), 25, 'Silver')
    canvas.draw_text(result, (300, 180), 25, 'Silver')
    canvas.draw_text("Score: " + str(score), (400, 100), 25, 'Black')
    if in_play:
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [80 + CARD_CENTER[0], 200 + CARD_CENTER[1]], CARD_SIZE)
    else:
        dealer_hand.draw(canvas, [80, 200])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric
