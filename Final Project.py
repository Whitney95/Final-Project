import numpy as np
from collections import Counter

def make_deck(y, Joker = False):
    """simulation of an ordered cards

    :param y: number of deck
    :return: an array that store all the cards after shuffling several times
    """
    deck = np.array([x for x in range(2,15)]*4*y)
    for i in range(len(deck)):
        if deck[i] > 11:
            deck[i] = 10
    if Joker:
        deck = np.append(deck,[100]*2*y)
    np.random.shuffle(deck)
    return deck

def renew_deck(deck, num):
    """ renew the deck with known card

    :param deck: the initial deck
    :param num: the card that would be deleted from the deck
    :return: the renewed deck
    """
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
    for i in range(1,10):
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


def aceloss(first2sum) -> str:
    """explore the situation that when first card of the dealer is Ace, Shall players surrender in advance
    to cut the losses

    :param first2sum: sum of the number of the first two cards
    :return: "Surr" stand for surrender in advance, and "Not" stand for no need to surrender in advance
    """
    surr_results = []
    not_surr_results = []
    for match in range(10):
        deck = make_deck(5)
        player1 = Player(deck, 'Hit', first2sum=first2sum, dealer1card=11, hit=False, surrender=True)
        player2 = Player(deck, 'Stand', first2sum=first2sum, dealer1card=11, hit=False, surrender= False)
        dealer1 = Dealer(player1.deck, 11, hit=False)
        dealer2 = Dealer(player2.deck, 11, hit=False)
        #print(player1.sum,dealer1.sum)
        surr_results.append(player1.winorloss(dealer1))
        not_surr_results.append(player2.winorloss(dealer2))
    sur = np.mean(surr_results)
    not_sur = np.mean(not_surr_results)
    if sur>not_sur:
        return 'Surr'
    else:
        return 'Not'


def rules_of_wildcard1(player1card, dealer1card,deck):
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

    list = []
    for i in range(1,10):
        Jh_results = []
        Js_results = []
        for match in range(1000):
            player_Jh = Player(name='Winnie', deck = deck, first2sum=player1card, dealer1card = dealer1card, hit=True,
                                Joker=True)
            player_Js = Player(name='Winnie', deck=deck, first2sum=player1card, dealer1card=dealer1card, hit=True,
                              Joker=True)
            dealer_Jh= Dealer(deck=player_Jh.deck, firstcard=dealer1card)

            dealer_Js = Dealer(deck=player_Js.deck, firstcard=dealer1card, hit=False)
            Jh_results.append(player_Jh.winorloss(dealer_Jh))
            Js_results.append(player_Js.winorloss(dealer_Js))
            #print(player_J.sum, dealer_J.sum)
        jh = np.mean(Jh_results)
        js = np.mean(Js_results)
        if jh>js:
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
            self.surrender = surrender
            self.second = first2sum
            deck = renew_deck(deck, 100)
            deck = renew_deck(deck, self.second)
            deck = renew_deck(deck, dealer1card)
            self.deck = deck
            self.third = deck[1]
            if self.third != 100:
                if self.third + self.second + 10 <= 21:
                    self.sum = self.second + self.second + 10
                else:
                    diff = 21-self.second - self.third
                    if diff>5:
                        self.sum =21
                    else:
                        self.sum = self.second +self.third +5
            else:
                self.sum = 21

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


class Dealer:
    def __init__(self, deck=(), firstcard=2, hit=True, PlayJocker = False):
        n2 = deck[0]
        if firstcard == 11 and n2 == 11:
            n2 = 1
        if n2 == 100:
            n2=10

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


if __name__ == '__main__':
    h_results=[]
    s_results = []

# Here is to validate the strategy matrix

    # matrix_cal = []
    #
    # for i in range(7,19):
    #       for j in range(2, 12):
    #          matrix_cal.append(StandorHit(i, j, 3))
    #print(matrix_cal)

# explore more on situation when dealer's first card is Ace

    loss = []
    for i in range(10,21):
        loss.append(aceloss(i))

    print(loss)


#  Scenario of rule1 of playing with Jokers

    deck = make_deck(4, Joker=True)
    J_allresults = []
    for i in range(2, 11):
        for j in range(2, 12):
            J_allresults.append(rules_of_wildcard1(i, j, deck=deck))
    print(J_allresults)
    print(np.array(J_allresults).reshape(9, 10))

