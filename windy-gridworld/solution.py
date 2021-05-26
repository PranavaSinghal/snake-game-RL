import numpy as np
import matplotlib.pyplot as plt
import random
import copy
from gridworld import GridWorld


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
        self.state_list = []
        self.action_list = self.mdp.actions
        for i in range(self.mdp.rows):
            for j in range(self.mdp.columns):
                self.state_list.append(tuple([i, j]))
                # keys must be immutable (convert sate to tuple before access)
        action_dict = dict(zip(self.action_list, len(self.action_list)*[0]))
        list_action_dicts = [copy.deepcopy(action_dict) for i in range(len(self.state_list))]
        # initialising all Q(S,A) = 0, including terminal value
        self.Q = dict(zip(self.state_list, list_action_dicts))
        self.num_episodes = 1
        self.timesteps = 1
        self.time_for_episode = []
        self.annealing = False
        mode = input("Enter mode of solver:")
        self.solve(mode)

    def epsilon_greedy_policy(self, state):
        ''' computes epsilon-greedy policy(action|state) for given state using Q
            returns an action based on computed probabilities'''
        #print("evaluating policy")
        state = tuple(state)
        action_values = self.Q[state]
        num_actions = len(action_values)

        max_val = np.amax(np.array(list(action_values.values())))
        all_max_actions = [key for key, value in action_values.items() if value == max_val]
        max_value_action = random.choice(all_max_actions)

        self.policy = dict(zip(action_values.keys(), len(action_values.keys())*[0]))
        for key in action_values.keys():
            if key == max_value_action:
                self.policy[key] = 1 - self.epsilon + self.epsilon/num_actions
            else:
                self.policy[key] = self.epsilon/num_actions

        return random.choices(list(self.policy.keys()), weights=list(self.policy.values()), k=1)[0]

    def Q_learning_once(self, final_state):
        '''off-policy greedy update'''
        return max(list(self.Q[tuple(final_state)].values()))

    def SARSA_once(self, final_state, next_action):
        '''on-policy sample update'''
        return self.Q[tuple(final_state)][next_action]

    def Expected_SARSA_once(self, final_state):
        '''on-policy weighted average update'''
        q_sum = 0
        self.epsilon_greedy_policy(final_state)
        for action, probability in self.policy.items():
            q_sum += probability*self.Q[tuple(final_state)][action]
        return q_sum

    def one_episode(self, mode='SARSA'):
        ''' 1 episode of SARSA
        initial state = start state'''
        #print("starting episode =", self.num_episodes)
        self.mdp.current_state = self.mdp.start
        action = self.epsilon_greedy_policy(self.mdp.current_state)
        # loop over time steps till end of episode
        #input("paused outside")
        while list(self.mdp.current_state) != list(self.mdp.goal):
            initial_state = self.mdp.current_state
            initial_action = action
            self.mdp.standard_move(self.mdp.current_state, action)
            reward = self.mdp.reward
            final_state = self.mdp.current_state
            next_action = self.epsilon_greedy_policy(final_state)
            if mode == 'SARSA':
                self.Q[tuple(initial_state)][action] += self.alpha*(reward + self.mdp.gamma *
                                                                    self.SARSA_once(final_state, next_action) - self.Q[tuple(initial_state)][action])
                if self.annealing:
                    self.epsilon = 0.1/self.num_episodes  # reduce epsilon for convergence
            elif mode == 'Q_learning':
                self.Q[tuple(initial_state)][action] += self.alpha*(reward + self.mdp.gamma *
                                                                    self.Q_learning_once(final_state) - self.Q[tuple(initial_state)][action])
            elif mode == 'Expected_SARSA':
                self.Q[tuple(initial_state)][action] += self.alpha*(reward + self.mdp.gamma *
                                                                    self.Expected_SARSA_once(final_state) - self.Q[tuple(initial_state)][action])
                if self.annealing:
                    self.epsilon = 0.1/self.num_episodes  # reduce epsilon for convergence

            action = next_action
            self.timesteps += 1
            # test code
            '''
            if self.timesteps < 8025 and self.timesteps > 8000:
                input("paused inside")
                print("episode =", self.num_episodes, ", timestep =", self.timesteps, "\ntime for episodes =", self.time_for_episode, "\nInitial state =", initial_state, ", final state =", final_state, ", action =", initial_action,
                      "\npolicy = ", self.policy, ", next action = ", next_action, " \nQ(state,.) = ", self.Q[tuple(final_state)], '\n')
                for i in range(self.mdp.rows):
                    for j in range(self.mdp.columns):
                        state_tuple = (i, j)
                        if state_tuple == tuple(self.mdp.start):
                            state_tuple = '*S*'
                        elif state_tuple == tuple(self.mdp.goal):
                            state_tuple = '*G*'
                        elif tuple(initial_state) == state_tuple:
                            state_tuple = '*i*'
                        elif tuple(final_state) == state_tuple:
                            state_tuple = '*f*'
                        print(state_tuple, end='\t')
                    print('\n')
            '''

    def solve(self, mode='SARSA'):
        '''solve the GridWorld MDP usig chosen solver (mode)'''
        if mode in ['SARSA', 'Expected_SARSA', 'Q_learning']:
            self.timesteps = 0
            self.num_episodes = 1
            episode_points = [0]
            timestep_points = [0]
            while self.timesteps < 11000:  # needs a condition for convergence
                start_time = self.timesteps
                self.one_episode(mode)
                end_time = self.timesteps
                self.time_for_episode.append((end_time-start_time))
                episode_points.append(self.num_episodes)
                timestep_points.append(self.timesteps)
                self.num_episodes += 1
            plt.plot(timestep_points, episode_points, 'ro')
            plt.title('Performance of '+mode)
            plt.show()
        else:
            print("Invalid solver (Try 'SARSA','Expected_SARSA' or 'Q_learning')")
            return

        self.epsilon = 0
        # for state in self.state_list:
        # self.epsilon_greedy_policy(state)
        #print("state =", state, ", policy =", self.policy)
        # test code
        self.mdp.current_state = self.mdp.start
        path = [tuple(self.mdp.current_state)]
        while list(self.mdp.current_state) != list(self.mdp.goal):
            self.mdp.standard_move(
                self.mdp.current_state, self.epsilon_greedy_policy(self.mdp.current_state))
            path.append(tuple(self.mdp.current_state))

        for i in range(self.mdp.rows):
            for j in range(self.mdp.columns):
                state_tuple = (i, j)
                if state_tuple in path:
                    state_tuple = '***'
                print(state_tuple, end='\t')
            print('\n')


if __name__ == '__main__':
    agent = Agent()
