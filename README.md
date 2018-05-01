# 6-Max-Mackerel: A poker bot

### Summary

	An attempt at a poker bot to use machine modeling to make optimal decisions when playing against other poker players. 2 card poker hands are converted to raw numbers in terms of strength and the features used by the machine model are bets and decisions made by opponent players, and various statistics of these opponent players. A strength of a hand is predicted and a list of all possible 2 card hands are compiled. From the prdicted strength, 2 card hands that are closer to the predicted value are assigned higher odds. This process is repeated throughout the various streets of poker play. A compiled total equity is estimated, and using this esitmated equity, our bot can make 'GTO' decsions. (for example, if our equity in a hand is .33, and an opponent bets 10 dollars into a 15 dollar pot, we need risk 10 dollars of our own money to win 25 dollars, so we need 10/25 equity to call, so if our predicted equity is .33. we can call profitably.)

### Data and EDA

The first step I took was to download the data I needed from a site called hhsmithy.com which datamines at poker tables logging each hand at a bunch of poker tables. I spent about 12 dollars on what they said was about 1 million hands. I extracted the data by reading each individual hand into separate strings (made easy because each hand starts with ‘started at’ and ends with ‘ended at’) and checked to see if a hand was revealed. If a hand was revealed, I used regular expressions to log the information I needed for the hand specific stats.. This was iterated through all one thousand and something files. I then went back through all the hands and recorded player specific stats, iterating through all the files again.
	One of the biggest problems I can see with this approach is that my sample is very biased, because I can only see hands that make it to showdown. Our data set will never see a successful bluff and probably skews towards much stronger hands than average. However, most hands that make it to showdown are fairly close in strength (you need at least two players to either to check and not bet because they are both fairly weak, or both players to bet and call each other because they both agree on that price for the strength of their hand) so our predictions should reflect what most players would assess their hand strength to be worth monetarily. The relationship between bets and hand strength was exponential, so I did some feature engineering by natural logging the bets.


### Metrics

The first step I had to make while trying to assess poker hands was to make a poker hand reader. Although there are 52c5 (2598960) unique 5 card poker hands, there are only 7462 unique ranks of poker hands, for example, all straight flushes (2s3s4s5s6s, 2c3c4c5c6c, 2h3h4h5h6h, 2d3d4d5d6d) can be lumped together as the same rank. I used java for speed for my heavy computational tasks, so most of this was done in a java project called Flounder. Any number of cards could be represented in a 52 long bitset in java, where 1 meant the card was there, and 0 for no card, and each bit represent a unique card, the first 4 bits being the 4 aces, and the last 4 bits being the 4 twos. The hand evaluator would start from the first (highest) card and try and find a straight flush. Then it would move on to the next highest card and find a straight flush until it got to the lowest card. If it didn’t find a straight flush, it would move on, starting from the highest card looking for a four of a kind, and so on. This ensured the first hand I found would be the best hand this particular 5 card hand could make. The evaluator would then return an integer 1-7462, 1 being a royal flush, AKQJT all suited and 7462 being 75432 offsuit. (This was fairly difficult)
	After I had a hand evaluator, assessing which hand would win was a simple inequality, comparing which number between 1-7462 was smaller, yielded the winning hand. From here I needed to make a few things. First I needed to evaluate the percentile of a hand which was as simple as iterating through every possible 2 card hand + board and comparing it to our hand + board, adding up all the hands our hand wins against and dividing by total number of hands. I also needed an effective hand percentile calculator, which iterates through all possible runouts to the river (all 2 card combinations if you are at the flop, all 1 card combinations if you are at the turn) then iterates through all possible 2 card combinations of hands for each. That’s a lot of iterating.

### Lookup Tables

I had moved to java because of speed, and it was still too slow for the amount of iterations I needed to do. The solution was to create lookup tables for the hand evaluator. Instead of evaluating the hand with the method above, we would give each 5 card, 6 card, and 7 card hand a semi-unique, quickly computable number, store that number and its number between 1-7462 in a hash table, and just look up what we need. Coming up with unique numbers for each hand was another challenge. I used a method I found on the internet, where we assign each card value a number, starting with A = 0, and K = 1. The biggest unique number we can make with a 7 card hand is KKKKAAA or unique number = 4. So our Q values should equal 4 + 1 = 5. If Q = 5, then the biggest unique number we can make with a 7 card hand is QQQQKKK which is 5*4 + 3*1 = 23. After adding 1, we get our J value of 24, and so on. This recursive relationship ensures that each unique combination of 7 cards will be accounted for. We also use a similar technique for straight flushes and flushes, and we only need to involve suits if those two categories of hands are involved, which can  be found quickly in our bitset representation with a loop and use of mod 4.
Every lookup table I made used this technique, adjusting the recursive relation for each different case.
	
### Modeling

I decided to use a gradient boost regression tree to make our predictions. We have a lot of weak almost uncorrelated features and gradient boost seemed like a good way to create a better ensemble model. The results of the gradient boost model was also superior to the neural net and elastic net regression models. I made 6 different models, a preflop model which only uses features that are available at preflop, a flop model (predicting hand strength) and a flop effective model (predicting effective hand strength, a turn model and turn effective model, and a river model. Because effective strength and actual hand strength are the same on the river, there was no need for a river effective. With these predictions I created a table that compared predicted hand strength to the actual hand strength. When entering a range of predictions of +- .025, the histogram distribution shows that our model got more accurate when it predicted higher hand strengths. This makes sense because people check and bet smaller than their hand is worth to try and keep people on the hook much more often than people wildly overvaluing their hands.
	
![](https://i.imgur.com/IZa2eEU.png)

The first histogram is the distribution of hand strengths when my model predicted a hand strength of about .4. The 2nd histogram is the distribution of hand strengths when my model predicted a hand strength of about .9. When my model makes a prediction, I fit a gamma distribution and use the gamma distribution to assign a gamma value to all possible 2 card hands, then normalize for a percentage. For each new street, new gamma values are multiplied with the old ones, as we go through more streets, our model narrows down which hands are the most likely throughout the hand.

##### Preflop
![](https://i.imgur.com/CxsJyQP.png)
##### Flop
![](https://i.imgur.com/ZFB833a.png)
##### Turn
![](https://i.imgur.com/NWY6BEd.png)
##### River
![](https://i.imgur.com/yiRKtgv.png)

As our model gets more information, it narrows down more and more possible hands. From these percentages at each street we can determine an estimated equity that we can use for our robot. Even though we can’t pinpoint a specific hand, This is how poker players play the game. Instead of guessing a players hand outright, they think of a range of possible hands and try and figure out their equity from there.

### Poker Table

In order to make a bot that could play, I had to simulate a poker game with poker rules in python. I started with a table object that could took a list populated by player objects. Players could be either human players or Mackerel bots. Player objects send commands to the poker table, and if the command is against the rules, will get an error and a prompt for a correct input.
