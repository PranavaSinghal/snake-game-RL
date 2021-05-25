from gridworld import GridWorld
import numpy as np


class Agent():
    '''
    RL Agent - navigates GridWorld
    3 solution methods:
    1)SARSA
    2)Q-Learning
    3)Expected SARSA
    '''

    def __init__(self):
        self.mdp = GridWorld()
        self.alpha = 0.5  # learning rate parameter
        self.epsilon = 0.1  # building epsilon-soft policy for exploration
        self.Q = dict()  # Q(S,A) state-action values
        state_list = []
        action_list = self.mdp.actions
        for i in range(self.mdp.rows):
            for j in range(self.mdp.columns):
                state_list.append(tuple([i, j]))
                # keys must be immutable (convert sate to tuple before access)
        action_dict = dict(zip(action_list, len(action_list)*[0]))
        self.Q = dict(zip(state_list, len(state_list)*[action_dict]))
        print(self.Q)


if __name__ == '__main__':
    agent = Agent()
