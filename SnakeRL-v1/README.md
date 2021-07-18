# Reinforcement Learning on the Snake Game

This is the solution to the original problem statement.

The structure and objective of the snake game is similar to what was described in __basic-snake-game__. I have only made a few style improvements to the code of the game and divided it into 3 files - __fruit.py, snake.py, game.py__. These contain all of the game functionality along with some additional variables to extract information for the snake to use during learning. __agent.py__ implements reinforcement learning on top of this game.

### Getting Started

1) In order to simply play the snake game, run the following code.
~~~
python game.py
~~~
More details about the game are available under __basic-snake-game__.

2) In order to explore reinforcement learning for the snake agent, you can do the following:

- ##### Training the snake
Initially the snake agent does not know how to behave in its environment and all actions are equivalent for it. It learns to move towards the fruit through trial and error improving its knowledge each time.

 The snake can be trained using either of the reinforcement learning algorithms SARSA, Expected SARSA and Q-Learning.

 By default the snake trains for 10 episodes. For the default game update time of 0.2 seconds this takes roughly a minute to run. You can visualise this training on the pygame window that opens up. Simultaneously, the score for each episode is printed to console.

 To start training, run
 ~~~
 python agent.py --mode [algorithm]
 ~~~
 --mode is an optional argument which takes either of the values 'Q_learning', 'SARSA', 'Expected_SARSA'. If it is not specified the default choice is 'Q_learning'

 #### Customising training settings
 There are several variables in the game that can be modified to achieve the desired behaviour. The important ones are:

 1) agent rewards <br>
 These are available from line 21 to 24. agent rewards are different values that affect how Q-values of each state-action pair are updated, which are estimates of how good or bad an action is. Negative rewards represent undesirable actions such as the _snake dies_ or _moves away from the fruit_.

 2) update_time <br>
 Available on line 26, this decides how fast you see the snake moving. It also corresponds to how fast the computation of Q values takes place. Increase the value to see the snake move a bit more slowly. While the agent uses and update_time = 20, an update_time of 150 is used in game.py by default (if you choose to play the snake game). Values lower than 20 caused my system to hang but you can experiment with this.

 3) num_max_episodes <br>
 Available on line 28, this is the maximum number of episodes for which the program runs. By default it is set to 10. However you might need larger values to do any significant training. A value of around 300 is a good place to start (taking around 5-10 minutes for training).

 4) self.num_check_squares <br>
 Available on line 61, this is the number of surrounding squares the snake uses to define its state space and scan for obstacles. It can take the values 4, 8 and 12. By default it is set to 4. This corresponds to the blocks above, below, left and right of the snake's head.

 5) Other training hyperparameters <br>
 Line 82, 83 and 86
 alpha, epsilon and gamma used for Q value updates can be tuned. These are values that worked well for me though I may not have explored all possible options.

 Note: This folder also contains files Q_4.txt, Q_8.txt and Q_12.txt. These represent Q values stored on training for different values of self.num_check_squares. On training these files are updated. In the absence of these files new files are created every time you start training from scratch. Moreover these values are used to initialise the Q values so that the snake can leverage previous experiences.

 A graph demonstrating score for each episode is generated at the end of all episodes.

- ##### Testing the snake
 Once the snake has been trained we can evaluate its performance. While the snake employs an epsilon-soft (exploratory) policy while choosing actions during training, it follows a greedy policy while testing (always choosing the best actions according to its knowledge).

 For testing how well it has learnt it is a good idea to set a low value for num_max_episodes, maybe around 10 to 30. Run the following
 ~~~
 python agent.py --mode [algorithm] --train no
 ~~~
 --train is also an optional argument which is set to 'yes' by default. Selecting 'no' explicitly lets the program know that you are not training and are testing instead.
