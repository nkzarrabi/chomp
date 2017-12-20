# chomp

[Chomp](http://www.papg.com/show?3AEA) is a pencil-and-paper territorial game for two players, conventionally played on a 3x4 grid representing a delicious chocolate bar. Players take it in turns to bite off rectangular regions from the lower right corner, aiming for the other player to eat the last square, which is tainted with a deadly neurotoxin.

![GIF of the game of chomp](chomp.gif)

With 3 rows and 4 columns, the game has a total of 34 states, which makes it a candidate for a simple machine-learning demonstration, in the same vein as the [MENACE](https://github.com/mscroggs/MENACE) machine.

The 50GamesHuman.pkl file contains the state of the machine after 50 games against a human, starting with 2 beads in each box. The 2000Games#.pkl files contain the machine state after facing a random opponent, or another 'intelligent' opponent using the same strategy.

![State transition probability diagram](ProbChooseSquareHuman.png)
This image shows the relative probability of choosing a square on a colour scale, after 50 training games against a human. White squares cannot be played (they are already eaten, or they are the poisoned top-left square). State 34 (lower right corner of the image) is the starting state of the game. The program has determined that playing in square number 8 (1st column, 3rd row) is the best first move.

This may turn into an NGCM outreach demonstration if it turns out to be successful.
