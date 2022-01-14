![OKAYMON](img/okaymon.png)

# A python library for playing the Okaymon Gamified Drop without spending thousands of dollars
  
You must have two files to play this game, 
  
1. in/colors.txt
   - a 10-line file containing color names in _increasing order_ of value
2. in/natures.txt
   - a file containing 2000 _unique_ natures
  
## To run
  
```bash
python3 -m pip install -r requirements.txt
python3 game.py
```

You should see pickle files appear in data/ which will hold the state of the game.