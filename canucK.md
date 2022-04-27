# Tokens


there is a file in this repo now called `canucK.py` that you can take a look at, it will explain how the exchange mechanism works for okayballs -> okaymon

it starts with a method on the Player class that generates what are called `tokens` in the context of the okayballs belonging to an instance of that class. 

## Balls
imagine we have a player with 100 balls lol
```python

player = Player()

# make some random okayballs
okayballs = [Okayball(random.randint(0,4)) for i in range(100)]

# put them in the player's pocket
for ball in okayballs:
  player.purchase_okayball(ball)

```

The `tokens` method on the player class will look at the player's okayballs and generate a list of subsets of that player's list of okayballs, but only subsets that are meaningful for exchange

```python
    def tokens(self):
        tokens = []
        # gen takes values 0 through 5, only when a ball of that gen belongs to the player
        for gen in {b.gen for b in self.okayballs}:
            # gen balls are all balls of the particular gen value in that block
            gen_balls = list(filter(lambda b: b.gen == gen, self.okayballs))
            # i will run to however many okayballs of that gen this player's got
            for i in range(len(gen_balls)):
                # on each iteration of i, take the first N balls of the list of balls
                # n will never be more than gen+1 though, because 
                # no collection balls of type gen, of length > gen+1 are meaningful for exchange
                # for example, 
                  # in no situation can you exchange 2 gen-1 okayballs for any single okaymon
                  # you cannot exchange 3 gen-2 okayballs for anything either!
                to_append = gen_balls[:min(i+1, gen+1)]
                if to_append not in tokens:
                    tokens.append(to_append)
        return tokens
```

## Tokens

Let's take a look at the tokens of a player with 100 balls:

```python
player.tokens()
```

```python
[[(0)'],
 [(1)'],
 [(1)', (1)'],
 [(2)'],
 [(2)', (2)'],
 [(2)', (2)', (2)'],
 [(3)'],
 [(3)', (3)'],
 [(3)', (3)', (3)'],
 [(3)', (3)', (3)', (3)'],
 [(4)'],
 [(4)', (4)'],
 [(4)', (4)', (4)'],
 [(4)', (4)', (4)', (4)'],
 [(4)', (4)', (4)', (4)', (4)']]
```

Even if this fucking guy had *a million* balls, these are the only tokens he would have to choose from in any one particular okaymon exchange event.  

Since tokens are computed whenever they are needed, if this guy had two of some token in this list, and then whent to exchange one these tokens (say our guy exhanged  `[(4)', (4)', (4)']` for a `gen-3 okaymon` (which by the way is the *only thing he could exchange 3 gen-5 okayballs for*)), then a call to tokens would still include that as they are built with the okayballs they have in their pocket.



# Exchanging Tokens for Okaymon

The logic for exchanging a player's token for an okaymon belongs *to the game class* because when that happens, the game state has to be updated for the following reasons:
  1. that okaymon has to be made unavailable to other players in the game
  2. that is all (maybe)

on the `Game` class, there is a method called `exchange_token` that takes in a particular `token` (say this one: `[(3)', (3)', (3)']`).  It get's all the information about the user from the balls themselves (each of the `(3)'` objects have `.player` attributes), and each token uniquely defines which gen okaymon it can be exchanged for. these (`[(3)', (3)', (3)']`) three ***gen-4 okayballs*** (okayballs are zero-indexed) can only be exchanged for ***one gen-2 okaymon!***

```python
def exchange_token(self, token):
        # this is where we find out which gen of okaymon we can buy with our token
        gen = token[0].gen - (len(token)-1)
        # self is game, so available_okaymon is all available okaymon this token has a chance to be exchanged with
        available_okaymon = self.available_okaymon(gen)
        # if the pool's not empty,
        if len(available_okaymon) > 0:
            # pick a random okaymon from that pool
            okaymon = available_okaymon[random.randint(0,len(available_okaymon)-1)]
            # reach into the player who owns this token, and assign this okaymon to them (and take their balls lol)
            self.find_player(token[0].player).exchange_token(token, okaymon)
```

This is it!