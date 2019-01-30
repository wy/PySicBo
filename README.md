# PySicBo
Python simulator for Three Dice game called Sic Bo.

A simulator for the Three Dice game (Sic Bo) played in Macau casinos and elsewhere.
Important simplification is that all three dice are treated equally which makes the maths a bit easier.

## Key concepts ##
- Criteria - does a dice configuration match a bet type (e.g. smalls, or Total of 4)
- Payoff - what is the pay off for a particular dice configuration
- Probability - what is the probability a set of dice configurations will occur?
- Odds - what is the expected outcome given the Probability and Payoffs
- Gambler's ruin / paradise - a slight variant on the commonly referred to set-up

## How to use ##

Simply run dice.py which will execute a number of test scenarios. You can also call testOdds() and testProbabilities() to loop through all the configured Bet Types.
