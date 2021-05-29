import numpy as np
import random
import sys


class GridWorld():
    '''Formulation of Windy Gridworld as an undiscounted episodic MDP'''

    def __init__(self, moves):
        self.rows = 7
        self.columns = 10
        self.wind = np.array([0, 0, 0, 1, 1, 1, 2, 2, 1, 0])
        # 0-indexed positions on the gridworld
        self.start = np.array([3, 0])
        self.goal = np.array([3, 7])
        self.current_state = self.start
        self.reward = -1  # same reward at each time step
        self.gamma = 1  # undiscounted

        self.move_type = moves  # input("Enter move type ['standard','kings','kings with stay']:")
        if self.move_type not in ['standard', 'kings', 'kings with stay']:
            print("Invalid input")
            sys.exit(0)
        self.stochastic_wind = False
        if self.move_type == 'standard':
            self.actions = ['up', 'down', 'right', 'left']
        elif self.move_type == 'kings':
            self.actions = ['up', 'down', 'right', 'left',
                            'up-right', 'up-left', 'down-right', 'down-left']
        elif self.move_type == 'kings with stay':
            self.actions = ['up', 'down', 'right', 'left', 'up-right',
                            'up-left', 'down-right', 'down-left', 'stay']

    def is_valid(self, state):
        # checks if a state lies inside the gridworld
        i, j = state
        if i >= 0 and i < self.rows and j >= 0 and j < self.columns:
            return True
        else:
            return False

    def move(self, state, action):
        # evaluates next state and reward for given state-action pair

        up = np.array([-1, 0])
        down = np.array([1, 0])
        right = np.array([0, 1])
        left = np.array([0, -1])

        new_state = state
        # without accounting for wind
        if self.move_type in ['standard', 'kings', 'kings with stay']:
            if action == 'up':
                new_state = state + up
            elif action == 'down':
                new_state = state + down
            elif action == 'right':
                new_state = state + right
            elif action == 'left':
                new_state = state + left
        if self.move_type in ['kings', 'kings with stay']:
            if action == 'up-right':
                new_state = state+up+right
            elif action == 'up-left':
                new_state = state+up+left
            elif action == 'down-right':
                new_state = state+down+right
            elif action == 'down-left':
                new_state = state+down+left
        if self.move_type in ['kings with stay']:
            if action == 'stay':
                new_state = state
        # else invalid action

        # finding final state accounting for wind
        start_i, start_j = state
        i, j = new_state
        # wind from starting column is responsible for displacement
        shift = 0
        if self.stochastic_wind:
            # to implement stochastic wind variations
            shift = random.choice([-1, 0, 1])*bool(self.wind[start_j])
        # max displaced state accounting for wind
        max_state = new_state + up*(self.wind[start_j]+shift)
        if self.is_valid(max_state):
            self.current_state = max_state
        elif self.is_valid(new_state):  # if wind pushes it to the boundary
            self.current_state = np.array([0, j])
        # else invalid move
        self.reward = -1  # in every case


if __name__ == '__main__':
    # code to test effect of wind
    mdp = GridWorld()
    for i in range(6):
        print(mdp.current_state)
        mdp.move(mdp.current_state, 'right')
