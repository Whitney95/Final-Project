# Title: 

## Team Member(s):
Yingyi Lai

# Monte Carlo Simulation Scenario & Purpose:
BlackJack Simulation

Purpose:
1. Validate the well-known strategy on "Hit" or "Stand"
2. Focus on the probability whether Players should surrender in advance or not if dealer's first card is Ace
3. Adding rules of Joker to see how does the strategy would change

## Simulation's variables of uncertainty
List and describe your simulation's variables of uncertainty (where you're using pseudo-random number generation). For each such variable, how did you decide the range and probability distribution to use?  Do you think it's a good representation of reality?

The strategy is based on the informaiton: sum of the first two cards of the player and the first card of the dealer.
So the uncertainty here is dealer's second and probably the thrid and fourth card. So I simulate players' third card if they hit and dealer's remaining cards with randomly shuffled cards, taking away the dealt cards. And see the expecation of choosing hit and stand to decide which strategy is better under different situations.

## Hypothesis or hypotheses before running the simulation:
Hypothesis 1: The strategy matrix I found is valid and reasonable
Hypythesis 2：Players should surrender in advance if they get cards less than 17 


## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)
There is still great randomness on it. So I simulate them separately another 100 time, which take longer time but validate the strategy matrix well.


## Instructions on how to use the program:
Just run it. It would take a little long time. Please wait. Thank you！



## All Sources Used:
