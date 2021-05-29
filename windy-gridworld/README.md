# Implementing SARSA, Q-Learning and Expected SARSA
##  Windy Gridworld
An RL agent attempts to navigate a windy gridworld and finds the shortest path from start to finish. Different algorithms are applied to solve this problem and their performance is compared.

#### Getting started
Navigate to the windy-gridworld folder and execute [solution.py](windy-gridworld\solution.py)
~~~
cd snake-game-rl\windy-gridworld
python solution.py
~~~
You will be asked to enter a variety of parameters for the RL agent

1) Type of moves
+ standard [up, down, left, right]
+ kings - also includes diagonal movement
+ kings with stay - in addition to kings allows the player to stay at the same place and only be affected by the wind (if any)

2) Wind Type
+ Stochastic wind - changes wind in a column by +1, 0 or -1 with equal probability. All changes are made with respect to a fixed set of values defined in [gridworld.py](windy-gridworld\gridworld.py)
+ Constant wind - wind in a column does not change - values defined in [gridworld.py](windy-gridworld\gridworld.py)

3) Mode of Learning
+ SARSA
+ Expected_SARSA
+ Q_learning

These are 3 different _Temporal Difference Learning_ methods

4) Annealing
+ If your chosen mode of learning is SARSA or Expected_SARSA, you will get an option to choose annealing
+ with annealing the agent reduces exploration over time and behaves most greedily
+ without annealing, the agent continues exploration with an epsilon-soft policy
+ Exploration is beneficial for dynamic environments (for instance, in the case of stochastic wind)

#### Some Results
The performance of different learning algorithms has been compared by plotting __episodes__ on the y-axis and corresponding __timesteps__ on the x-axis.

A larger slope corresponds to shorter time per episode and therefore, a more optimal solution. In the case of constant wind, once the slope settles on a constant value the optimal solution has been found.

Performance of Q-Learning:

![Q_learning_standard_moves_constant_wind](./windy-gridworld/results/Q_learning_standard_moves_constant_wind.png)

![Q_learning_standard_moves_stochastic_wind](./windy-gridworld/results/Q_learning_standard_moves_stochastic_wind.png)


#### References
For a complete description of windy gridworld refer to page 152, [_Reinforcement Learning_](http://incompleteideas.net/book/RLbook2020.pdf) by Barto and Sutton

Details of the task can be found [here](https://www.cse.iitb.ac.in/~shivaram/teaching/old/cs747-a2020/pa-3/programming-assignment-3.html)
