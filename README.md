# Title: BlackJack Simulation

## Team Member(s):
Yingyi Lai

# Monte Carlo Simulation Scenario & Purpose:
BlackJack Simulation

Purpose:
1. Validate the well-known strategy on "Hit" or "Stand"
2. Focus on the probability whether Players should surrender in advance or not if dealer's first card is Ace
3. Adding rules of Joker to see how does the strategy would 

## Simulation's variables of uncertainty
The strategy is based on the information: sum of the first two cards of the player and the first card of the dealer.
So the uncertainty here is dealer's second and probably the third and fourth card. So I simulate players' third card if they hit and dealer's remaining cards with randomly shuffled cards, taking away the dealt cards. And see the expecation of choosing hit and stand to decide which strategy is better under different situations.

## Hypothesis or hypotheses before running the simulation:
Hypothesis 1: The strategy matrix I found is valid and reasonable
Hypythesis 2：Players should surrender in advance if they get cards less than 17 


## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)

1. Validation of the traditional strategy
There is still great randomness on it. I intend to simulate another 100 time, but due to the long computational time, I just try 10 more times, which take shorter time but can improve the result in some extent.

The result is followed:
     2   3   4   5   6   7   8   9  10  Ace
7  ['H' 'H' 'H' 'H' 'H' 'H' 'H' 'H' 'H' 'H']
8  ['H' 'H' 'H' 'H' 'H' 'H' 'H' 'H' 'H' 'H']
9  ['H' 'H' 'H' 'H' 'H' 'H' 'H' 'H' 'H' 'H']
10 ['H' 'H' 'H' 'H' 'H' 'H' 'H' 'H' 'H' 'H']
11 ['H' 'H' 'H' 'H' 'H' 'H' 'H' 'H' 'H' 'H']
12 ['H' 'H' 'H' 'S' 'S' 'H' 'H' 'H' 'H' 'H']
13 ['S' 'S' 'S' 'S' 'S' 'H' 'H' 'H' 'H' 'H']
14 ['S' 'S' 'S' 'S' 'S' 'H' 'H' 'H' 'H' 'H']
15 ['S' 'S' 'S' 'S' 'S' 'H' 'H' 'H' 'H' 'H']
16 ['S' 'S' 'S' 'S' 'S' 'H' 'H' 'H' 'H' 'H']
17 ['S' 'S' 'S' 'S' 'S' 'S' 'S' 'S' 'S' 'S']
18 ['S' 'S' 'S' 'S' 'S' 'S' 'S' 'S' 'S' 'S']

This is quite the same as strategy I found online, except the one "12-4", which is supposed to be "s". 

2. In scenario that dealer's first card is Ace, I want to figure out whether surrender in advance could leviate loss of players or not.

I simulate two different situation,one is to surrender in advance, another is still choosing to hit to take a chance.
['Surr', 'Surr', 'Surr', 'Surr', 'Surr', 'Surr', 'Surr', 'Surr', 'Surr', 'Not', 'Not']
As the result shows, surrender in advance is the best way for players with cards sum from 10 to 18, to avoid further loss, since the probabilty of getting a 10 next is pretty high. While if your cards is greater than or equal to 19, the probability of win the game looks good. Hence the strategy in this case, is to surrender if the sum of cards less than 18 and stand if the sum greater than 18.

3. I add Jokers to the deck, and change the rule that Joker could be any number between 5-10. 
Here is the stategy I simulate in 10000 times in the case player luckily get a Joker in one of the first two cards.
                2   3   4   5   6   7   8   9  10  11
Joker with 2  ['H' 'H' 'H' 'H' 'H' 'H' 'H' 'H' 'H' 'H']
Joker with 3  ['H' 'H' 'H' 'H' 'H' 'H' 'H' 'H' 'H' 'H']
Joker with 4  ['S' 'H' 'H' 'H' 'H' 'H' 'H' 'H' 'H' 'S']
Joker with 5  ['S' 'S' 'S' 'H' 'H' 'S' 'S' 'S' 'H' 'H']
Joker with 6  ['H' 'H' 'S' 'H' 'S' 'H' 'S' 'H' 'H' 'S']
Joker with 7  ['S' 'S' 'H' 'H' 'H' 'H' 'H' 'S' 'H' 'S']
Joker with 8  ['S' 'H' 'H' 'S' 'S' 'S' 'S' 'S' 'H' 'S']
Joker with 9  ['H' 'H' 'S' 'S' 'H' 'S' 'S' 'H' 'S' 'H']
Joker with 10  ['H' 'S' 'S' 'H' 'H' 'S' 'S' 'H' 'S' 'S']


## Instructions on how to use the program:
As I comment above several chunk in the main function.

The output would be three different matrix. The first one is the traditional strategy matrix, and second is the further exploration in case dealer's first card is Ace. The last one is the new strategy for adding new rules for Joker.



## All Sources Used:
BalckJack stategy: https://wizardofodds.com/games/blackjack/strategy/4-decks/
