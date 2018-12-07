from random import randint
import numpy as np
from collections import Counter

def make_deck(y):
    """simulation of an ordered cards

    :param y: number of deck
    :return: an array that store all the cards after shuffling several times
    """
    deck = np.array([x for x in range(2,15)]*4*y)
    for i in range(len(deck)):
        if deck[i] > 11:
            deck[i] = 10
    np.random.shuffle(deck)
    return deck

def renew_deck(deck, num):
    ind = list(deck).index(num)
    deck = np.delete(deck, [ind])
    np.random.shuffle(deck)
    return deck


def StandorHit(first2sum, dealer1card,numofdeck)->str:
    """Comparing the expectation of stand and hit and decide which is a better strategy

    :param first2sum: the sum of the number of the first two cards of the player
    :param dealer1card: number of the dealer's first card
    :param numofdeck: number of the decks we used in this game
    :return: player's best choice of stand or hit
    """

    list = []
    for i in range(1,100):
        h_results = []
        s_results = []
        for match in range(1000):
            deck = make_deck(numofdeck)
            player1 = Player(deck, 'Hit', first2sum, dealer1card, hit=True)
            dealer1 = Dealer(player1.deck, dealer1card)
            player2 = Player(deck, 'Stand', first2sum, dealer1card, hit=False)
            dealer2 = Dealer(player2.deck, dealer1card, hit=False)
            h_results.append(player1.winorloss(dealer1))
            s_results.append(player2.winorloss(dealer2))
        h = np.mean(h_results)
        s = np.mean(s_results)
        # print(h_results)
        # print(s_results)
        # print([h,s])
        if h>s:
            list.append('H')
        else:
            list.append('S')
    a = Counter(list)
    if a['H'] > a['S']:
        return 'H'
    else:
        return 'S'

# define Player and Dealer:

class Player:
    """A player in a BlackJack game.
    Players would have 2 cards known.
"""
    player_count = 0  # Initialize count of all players.
    all_players = []  # automatically track all players

    def __init__(self, deck=(), name=None, first2sum=0, dealer1card = 0, hit=True, surrender=False, Joker = False):
        Player.player_count += 1
        Player.all_players.append(self)

        # assign player's name:
        if name is None:
            self.name = 'Player {:02}'.format(Player.player_count)
        else:
            self.name = name
        if Joker:
            self.second = first2sum
            deck = np.append(deck,14)
            deck = renew_deck(deck, self.second)
            deck = renew_deck(deck, dealer1card)
            self.deck = deck
            self.third = deck[1]
            if self.third > 10 - self.second:
                self.sum = 21
            else: self.sum = 10 + self.second + self.third

        else:
            self.first2sum = first2sum
            d1 = deck[deck < first2sum]
            n1 = d1[d1 >= first2sum-11][0]
            self.first = n1
            self.second = self.first2sum - self.first
            q = 1
            while self.second == 1:
                self.first = d1[d1>=first2sum-11][q]
                self.second = self.first2sum - self.first
                q += 1
            deck = renew_deck(deck, self.first)
            # print(d1)
            deck = renew_deck(deck, self.second)
            deck = renew_deck(deck, dealer1card)
            self.third = 0

            self.surrender = surrender
            if surrender:
                hit = False

            if hit:
                n3 = deck[1]
                if first2sum + n3 > 21 and n3 == 11:
                    self.third = 1
                else:
                    self.third = n3
            self.sum = first2sum + self.third
            self.deck = deck

        # print(self.deck)
        # print(self.sum)
        # print(self.first, self.second, self.third)

    def winorloss(self, d: 'Dealer'):
        """ The player would win the dealer or not

        :param d: the object of class 'Dealer'
        :return: if player win the game, return 1
                 if dealer win the game, return -1
                 if tie, return 0
        """
        if self.sum > 21:
            return -1
        if (self.sum < 22 and d.sum < 22 and self.sum < d.sum):
            if self.surrender == True:
                return -0.5
            else: return -1
        if self.sum == d.sum:
            return 0
        else:
            return 1



# class Dealer:
#     """The Dealer in a BlackJack game.
#     Players can only see the first card of the dealer."""
#
#     def __init__(self, deck=(), first=0):
#         self.cards_count = 2
#         #print(deck)
#         self.first = first
#         #np.random.shuffle(deck)
#         n2 = deck[0]
#         deck = pop(deck)
#         self.third = 0
#
#         if n2==1 & self.first < 11:
#             self.second = 11
#         self.second = n2
#
#         self.sum = self.first + self.second + self.third
#         flag =0
#         while self.sum < 17:
#             n3 = deck[0]
#             deck = pop(deck)
#             if self.first + self.second + self.third < 11 and n3 ==1:
#                 n3 = 11
#             if flag == 0:
#                 self.third = n3
#                 flag +=1
#             if flag == 1:
#                 self.four = n3
#                 flag +=1
#
#             self.cards_count += 1
#             self.sum += n3
#
#
#         #print(self.sum)
#         #print(self.cards_count)
#         #print(self.second, self.third)
#         #print("--")



class Dealer:
    def __init__(self, deck=(), firstcard=2, hit=True, PlayJocker = False):
        n2 = deck[0]
        if firstcard == 11 and n2 == 11:
            n2 = 1

        k = [firstcard, n2]

        if hit == True:
            count = 2
        else:
            count = 1

        while sum(k) < 17:
            k.append(deck[count])
            count +=1
            if 11 in k and sum(k) > 21:
                ind = k.index(11)
                k[ind] = 1

        self.cards = k
        self.sum = sum(k)

        # print(self.sum)
        # print(self.cards)
        # print("--")




if __name__ == '__main__':
    h_results=[]
    s_results = []

# Here is to validate the strategy matrix

matrix_cal = []

for i in range(7,19):
      for j in range(2, 12):
         #print(i,j)
         matrix_cal.append(StandorHit(i, j, 3))

print(np.array(matrix_cal).reshape(12,10))

#print(StandorHit(12, 3, 4))

def aceloss(first2sum):
    surr_results = []
    for match in range(1000):
        deck = make_deck(1)
        player1 = Player(deck, 'Hit', first2sum, hit=True)
        dealer1 = Dealer(player1.deck, 11)
        #print(player1.sum,dealer1.sum,deck, player1.deck)
        surr_results.append(player1.winorloss(dealer1))
    return np.mean(surr_results)

su = np.mean(surr_results)

loss = []
for i in range(10,17):
    loss.append(aceloss(i))

print(loss)


def rules_of_wildcard1(player1card, dealer1card,numofdeck):
    """Adding rules of Joker, to be a wild card. Assuming the first card of player is Joker and calculate a best
    strategy matrix when facing different situations of dealer's first card

    scenario:
    we assume joker and ace is also black jack, which is an overwhelming victory
    produce the expectation matrix of winning the game when you have the Joker
    the columns are the other card from player, ranged from 2-9
    the row are dealer's first card ranged from 2-11

    :param player1card: player's card other than Joker
    :param dealer1card: dealer's faced up card
    :param numofdeck: the number of decks used in the game
    :return: the expectation of winning the game
    """

    J_results=[]
    for match in range(1000):
        player_J = Player(name='Winnie', first2sum=player1card, hit=True, Joker = True, numofdeck=numofdeck)
        dealer_J = Dealer_J(deck=player_J.deck, firstcard=dealer1card)
        J_results.append(player_J.winorloss(dealer_J))
    return np.mean(J_results)


#################  Scenario of rule1 of playing with Jokers
J_allresults=[]
for i in range(2,10):
    for j in range(2,12):
        J_allresults.append(rules_of_wildcard(i, j, 2))
print(J_allresults)
print(np.array(J_allresults).reshape(8,10))

