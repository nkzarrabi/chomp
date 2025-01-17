# chomp

[Chomp](http://www.papg.com/show?3AEA) is a pencil-and-paper territorial game for two players, conventionally played on a 3x4 grid representing a delicious chocolate bar. Players take it in turns to bite off rectangular regions from the lower right corner, aiming for the other player to eat the last, poisoned square.

![GIF of the game of chomp](Art/square/chomp.gif)

With 3 rows and 4 columns, the game has a total of 34 states, which makes it a candidate for a simple machine-learning demonstration, in the same vein as the [MENACE](https://github.com/mscroggs/MENACE) machine.

Clone the repository and run chomp.py to run a simulation of chomp.

The 50GamesHuman.pkl file contains the state of the machine after 50 games against a human, starting with 2 beads in each box. The 2000Games#.pkl files contain the machine state after facing a random opponent, or another 'intelligent' opponent using the same strategy. perfect.pkl is almost certain to win when playing first.

![State transition probability diagram](prob-diagrams/ProbChooseSquareIntelligent.png)
This image shows the relative probability of choosing a square on a colour scale, after 10000 games of self-play. White squares cannot be played (they are already eaten, or they are the poisoned top-left square). State 34 (lower right corner of the image) is the starting state of the game. The program has determined that playing in square number 6 (3rd column, 2nd row) is the best first move.

The physical version of Chomp, which uses plastic containers filled with coloured beads to represent game states, was premiered at a [Bringing Research to Life](https://www.southampton.ac.uk/per/university/roadshow.page)  roadshow event at a school in south-west england.

![Chomp at the Bringing Research to Life Roadshow](Art/THS.jpg)

Including a short training period for three demonstrators to learn how to host the game, 98 games were played, in sets of seven. The results were marked on the chart below, with human wins marked from the top of the diagram and chomp wins from the bottom. The plot shows that over time chomp learns how to play and win.  

![Chomp's win record](Results/Grid-V1.png)

Chomp was reset then taken to [Cheltenham Science Festival](https://www.cheltenhamfestivals.com/science) for two days. We played 143 games over this time and saw Chomp learning somewhat more erratically this time, representative of learning non-optimal strategies from its opponents, which it had to forget in order to progress.
![Chomp at Cheltenham Science Festival](Results/Grid-CSF.png)
![James and Ed teach the machine](Art/Conversation.png)
![Pepper takes a look at Chomp](Art/Pepper.png)

Chomp's next outing was at the [Southampton Science and Engineering Day](http://www.sotsef.co.uk/science_&_engineering_day/). Over the day, we played 86 games, learning steadily from a win-rate of 1/7 to 6/7 over the day.

![Chomp at Southampton Science and Engineering Day](Results/Grid_SOTSEF.png)

We were invited to [Winchester Science Centre](https://www.winchestersciencecentre.org/) and had a great time. This time we asked everyone who played to give us a one word review - we've compiled them into a Wordle.

![Wordle of Chomp reviews after Winchester Science Centre Visit](Art/wordle.png)

It's safe to say that Chomp is a winner!

![Chomp on the top step of the podium at Winchester Science Centre](Art/podium.jpg)
