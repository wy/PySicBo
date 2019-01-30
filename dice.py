"""
Author: ~wy (https://github.com/wy)
Date: 25/01/2019
Description:
A simulator for the Three Dice game (Sic Bo) played in Macau casinos and elsewhere.
Important simplification is that all three dice are treated equally
which makes the maths a bit easier.
Key concepts:
Criteria - does a dice configuration match a bet type (e.g. smalls, or Total of 4)
Payoff - what is the pay off for a particular dice configuration
Probability - what is the probability a set of dice configurations will occur?
Odds - what is the expected outcome given the Probability and Payoffs
Gambler's ruin / paradise - a slight variant on the commonly referred to set-up
"""

import random

# small is 4-10 excluding triples
small = lambda x: (4 <= x[0] + x[1] + x[2] <= 10 and not (x[0] == x[1] and x[1] == x[2]))

# large is 11-17 excluding triples
large = lambda x: (11 <= x[0] + x[1] + x[2] <= 17 and not (x[0] == x[1] and x[1] == x[2]))

staticpayoffs = {
    4: 50,
    5: 30,
    6: 17,
    7: 12,
    8: 8,
    9: 6,
    10: 6
}


def payoff410(x):
    total = x[0] + x[1] + x[2]
    return (staticpayoffs[total] - 6) / 7.0


def payoff48(x):
    total = x[0] + x[1] + x[2]
    return (staticpayoffs[total] - 4) / 5.0


def payoffsmall14(x):
    total = x[0] + x[1] + x[2]
    if total < 11:
        return 0
    else:
        return 5.5


payoffs = {
    "small": lambda _: 1,
    "large": lambda _: 1,
    "4": lambda _: 60,
    "5": lambda _: 30,
    "6": lambda _: 17,
    "7": lambda _: 12,
    "8": lambda _: 8,
    "9": lambda _: 6,
    "10": lambda _: 6,
    "11": lambda _: 6,
    "12": lambda _: 6,
    "13": lambda _: 8,
    "14": lambda _: 12,
    "15": lambda _: 17,
    "16": lambda _: 30,
    "17": lambda _: 60,
    "one": lambda x: len(list(filter(lambda y: y == 1, list(x)))),
    "two": lambda x: len(list(filter(lambda y: y == 2, list(x)))),
    "three": lambda x: len(list(filter(lambda y: y == 3, list(x)))),
    "four": lambda x: len(list(filter(lambda y: y == 4, list(x)))),
    "five": lambda x: len(list(filter(lambda y: y == 5, list(x)))),
    "six": lambda x: len(list(filter(lambda y: y == 6, list(x)))),
    "4-10": lambda x: payoff410(x),
    "4-8": lambda x: payoff48(x),
    "small14": lambda x: payoffsmall14(x),
}

bet_types = {
    "small": small,
    "large": large,
    "4-10": lambda x: (4 <= x[0] + x[1] + x[2] <= 10),
    "4-8": lambda x: (4 <= x[0] + x[1] + x[2] <= 8),
    "small14": lambda x: ((x[0] + x[1] + x[2] == 14) or small(x)),
    "4": lambda x: (x[0] + x[1] + x[2] == 4),
    "5": lambda x: (x[0] + x[1] + x[2] == 5),
    "6": lambda x: (x[0] + x[1] + x[2] == 6),
    "7": lambda x: (x[0] + x[1] + x[2] == 7),
    "8": lambda x: (x[0] + x[1] + x[2] == 8),
    "9": lambda x: (x[0] + x[1] + x[2] == 9),
    "10": lambda x: (x[0] + x[1] + x[2] == 10),
    "11": lambda x: (x[0] + x[1] + x[2] == 11),
    "12": lambda x: (x[0] + x[1] + x[2] == 12),
    "13": lambda x: (x[0] + x[1] + x[2] == 13),
    "14": lambda x: (x[0] + x[1] + x[2] == 14),
    "15": lambda x: (x[0] + x[1] + x[2] == 15),
    "16": lambda x: (x[0] + x[1] + x[2] == 16),
    "17": lambda x: (x[0] + x[1] + x[2] == 17),
    "one": lambda x: (x[0] == 1 or x[1] == 1 or x[2] == 1),
    "two": lambda x: (x[0] == 2 or x[1] == 2 or x[2] == 2),
    "three": lambda x: (x[0] == 3 or x[1] == 3 or x[2] == 3),
    "four": lambda x: (x[0] == 4 or x[1] == 4 or x[2] == 4),
    "five": lambda x: (x[0] == 5 or x[1] == 5 or x[2] == 5),
    "six": lambda x: (x[0] == 6 or x[1] == 6 or x[2] == 6),

}


def rolldice():
    # Rolls dice simulation
    results = [random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)]
    results.sort()
    return tuple(results)


def calculateodds(bet_type, iterations=100000):
    criteria = bet_types[bet_type]
    payoff = payoffs[bet_type]
    sum_total = 0
    for i in range(iterations):
        r = rolldice()
        if criteria(r):
            sum_total += payoff(r)
        else:
            sum_total += -1
    return sum_total / float(iterations)


def calculateprobabilities(bet_type, iterations=1000000):
    criteria = bet_types[bet_type]
    sum_total = 0
    for i in range(iterations):
        r = rolldice()
        if criteria(r):
            sum_total += 1
    return sum_total / float(iterations)


def testOdds():
    for k in bet_types:
        print("{}: {}".format(k, calculateodds(k)))


def testProbabilities():
    for k in bet_types:
        print("{}: {}".format(k, calculateprobabilities(k)))


def gamblersruin(bet_type, startingcapital=1000, starting_bet_size=10,
                 win_above=1500, iterations=3000):
    # make successive bets of fixed size until either bankrupt or hit win threshold
    wins = 0
    criteria = bet_types[bet_type]
    payoff = payoffs[bet_type]
    for i in range(iterations):
        capital = startingcapital
        bet_size = starting_bet_size
        while 0 < capital < win_above:
            r = rolldice()
            if criteria(r):
                capital += payoff(r) * bet_size
                # print(capital, "win", bet_size)
                bet_size = starting_bet_size

            else:
                capital -= bet_size
                # print(capital, "loss", bet_size)
                bet_size = min(2 * bet_size, capital)
        if capital >= win_above:
            wins += 1
        # print(wins / float(i+1))
    return wins / float(iterations)


def gamblersparadise(bet_type, startingcapital=1000):
    for i in range(1000, 12000, 10):
        wp = gamblersruin(bet_type, startingcapital=startingcapital, win_above=i)
        er = (wp * (i - startingcapital)) - (startingcapital * (1 - wp))
        print(i, wp, er)


# gamblersparadise("small")

# Example tests
testOdds()
k = "4-10"
print("{}: {}".format(k, calculateodds(k)))
print("{}: {}".format(k, calculateprobabilities(k)))
