# Reinforcement Learning on the Snake Game

This is the solution to the original problem statement, to use reinforcement learning to make a snake reach high scores in the snake game.

The structure and objective of the snake game is similar to what was described in __basic-snake-game__. I have only made a few style improvements to the code of the game and divided it into 3 files - __fruit.py, snake.py, game.py__. These contain all of the game functionality along with some additional variables to extract information for the snake to use during learning. __agent.py__ implements reinforcement learning on top of this game. The files __Q_4.txt,Q_8.txt and Q_12.txt__ are stored/pickled Q values of previous training experience. You can use these files to continue on top is this training or delete/move them to start training from scratch. The remaining folders contain essential game files just like __basic-snake-game__.

### Brief Overview of the Solution
The agent uses tabular methods like SARSA, Expected_SARSA and Q_learning to learn how to optimise rewards. Tabular methods store Q-values for each state-action pair and therefore a smaller number of state-action pairs allows faster and efficient training.

We reduced the size of the state space by making the snake only check its neighbouring squares for obstacles. By default it only checks the 4 squares immediately next to its head. It only knows the relative position of the fruit from 8 directions up, down, left and right and the four diagonal regions between them. The snake is not aware of the exact position of the fruit on the board, only its relative position with respect to its head. This means that the state space now consists of 8*(2^4) = 128 states, 8 for relative fruit positions and 2^4 for the presence or absence of obstacles in the neighbouring squares.

Every state has 4 actions up, down, left and right. Therefore there is a total of 128*4 = 512 state-action pairs that the snake has to learn about. This is a considerably reduced representation of the state-action space which still contains most of the essential information that the snake needs to avoid death and get fruit.


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

 For testing how well it has learnt it is a good idea to set a low value for num_max_episodes, maybe around 10 to 30. The snake gets better scores during testing since it makes fewer mistakes by exploring. Run the following code to test.
 ~~~
 python agent.py --mode [algorithm] --train no
 ~~~
 --train is also an optional argument which is set to 'yes' by default. Selecting 'no' explicitly lets the program know that you are not training and are testing instead.

- #### Comparing different learning algorithms
 You can also compare SARSA, Expected_SARSA and Q_learning by seeing how the snakes reward varies with episodes for different algorithms. Run the following
 ~~~
 python agent.py --compare yes
 ~~~
 This runs the snake game thrice for num_max_episodes number of episodes each. At the end it generates a graph comapring scores in each episode using different algorithms.

 The argument --train set to no compares these algorithms under greedy policy. --mode has no effect.

 Note: This method always trains from scratch and does not leverage previous training data. This design choice is to avoid unfair comparisons where previous knowledge gained by training over one algorithm supersedes that of the other algorithms.

 For an example of such a comparison (300 episodes each, so its about 2 hours worth of learning in total) watch [this](https://drive.google.com/file/d/1JjylKlK8kachEsdyanH9KO7Az1WJMub8/view?usp=sharing) video.

The most general call to agent.py therefore is
~~~
python agent.py --compare [yes/no] --train [yes/no] --mode [SARSA/Expected_SARSA/Q_learning]
~~~

### Limitations
While this approach performs quite well (with a maximum score of 58 fruits on one of my trials) there are still some limitations such as the snake's inability to detect that it is entering a closed loop and trapping itself. This is due to the choice of a reduced state representation in order to keep the number of states low and allow faster, more efficient training. However this representation does not capture all the details of the state and can lead to the snake making bad decisions at times. The fluctuation in training score can also be attributed to this to a large extent in addition to the need for more training episodes.
