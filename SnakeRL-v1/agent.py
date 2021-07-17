import pygame
import sys
import random
import numpy as np
import pickle
import argparse
import matplotlib.pyplot as plt
from time import sleep
from pygame.math import Vector2
from itertools import permutations
from fruit import *
from snake import *
from game import *

left = Vector2(-1, 0)
right = Vector2(1, 0)
up = Vector2(0, -1)
down = Vector2(0, 1)
directions = [up, left, right, down]
# agent rewards
correct_direction_reward = 2
fruit_reward = 10
fail_reward = -10
step_reward = -1
# update time for screen
update_time = 20
# number of episodes
num_max_episodes = 10


class Agent:
    '''RL agent which learns to play Snake
    uses Q-learning'''

    def __init__(self, learning_type, compare='no', training='yes'):
        self.learning_type = learning_type
        print(self.learning_type)
        self.compare = compare
        self.game = Game(update_time)
        self.init_state_space()
        self.init_action_space()
        if training == 'yes':
            self.training = True
        elif training == 'no':
            self.training = False
        self.start_learning()
        if self.compare == 'no':
            self.save_progress()

    def check_learning(self):
        plt.plot(list(range(self.num_episodes)), (self.scores),
                 '-', label=self.learning_type)
        plt.xlabel('episodes')
        plt.ylabel('episode score')
        plt.legend()
        plt.grid(True)

    def init_state_space(self):
        # all possible fruit positions relative to head position
        fruit_positions = ['UL', 'U', 'UR', 'L', 'R', 'DL', 'D', 'DR']
        self.num_check_squares = 8  # number of surrounding squares checked for obstacles
        n = self.num_check_squares
        obstacles = []
        for i in range(2**n):
            b = bin(i)[2:]
            obstacle = str(0)*(n - len(b))+b
            obstacle = tuple([int(x) for x in list(obstacle)])
            obstacles += [obstacle]

        #zeros_n_ones = [0 for i in range(n)]+[1 for i in range(n)]
        #obstacles = list(set(permutations(zeros_n_ones, n)))
        self.states = []
        for fruit_position in fruit_positions:
            for obstacle in obstacles:
                self.states.append((fruit_position, obstacle))

    def init_action_space(self):
        self.actions = ['U', 'L', 'R', 'D']

    def start_learning(self):
        self.init_Q()
        self.alpha = 1
        self.epsilon = 0.1
        if not self.training:
            self.epsilon = 0
        self.gamma = 0.1
        self.num_episodes = 0
        self.max_score = 0
        self.scores = []
        while self.num_episodes < num_max_episodes:
            self.episode_return = 0
            self.start_episode()
            #self.epsilon = self.epsilon*0.95
            self.num_episodes += 1
            print(f"episode: {self.num_episodes}, score: {self.score}")
            self.scores.append(self.score)
            if self.score > self.max_score:
                self.max_score = self.score
        print("max score = ", self.max_score)

    def init_Q(self):
        # check if stored Q values exist
        if self.compare == 'no':
            try:
                filename = 'Q_'+str(self.num_check_squares)+'.txt'
                with open(filename, 'rb') as Q_file:
                    self.Q = pickle.load(Q_file)
                print('using previous training data...')
            except FileNotFoundError:
                # if not
                self.init_Q_blank()
        elif self.compare == 'yes':
            self.init_Q_blank()

    def init_Q_blank(self):
        self.Q = {}
        for state in self.states:
            for action in self.actions:
                self.Q[(state, action)] = 0

    def save_progress(self):
        print("saving progress...")
        filename = 'Q_'+str(self.num_check_squares)+'.txt'
        with open(filename, 'wb') as Q_file:
            pickle.dump(self.Q, Q_file)

    def start_episode(self):
        self.get_current_state()
        self.choose_action()
        self.timesteps = 0
        pre_reward_timestep = 0
        self.score = 0
        self.game.failed = False
        rewards = []  # test variable
        while self.game.failed == False:
            break_check = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == self.game.SCREEN_UPDATE:
                    initial_state = self.state
                    initial_action = self.action
                    self.next_state()
                    initial_score = self.score
                    self.score = len(self.game.snake.body) - 3
                    self.score_increased = True if self.score > initial_score else False
                    if self.score_increased:
                        pre_reward_timestep = self.timesteps
                    if self.score < initial_score:
                        self.score = initial_score
                    self.get_reward()
                    self.get_current_state()
                    self.choose_action()
                    self.Q[(initial_state, initial_action)] += self.alpha*(self.reward +
                                                                           self.gamma*self.Q_update() - self.Q[(initial_state, initial_action)])
                    rewards.append(self.reward)
                    #print("rewards = ", rewards, ",action = ", self.action,", fruit state = ", self.fruit_state, "Q(", initial_state, ", ", initial_action, ") = ", self.Q[(initial_state, initial_action)])

                    self.episode_return = self.reward+self.gamma*self.episode_return
                    self.timesteps += 1

                    if self.timesteps - pre_reward_timestep > 400:  # to avoid infinite loops without reward
                        break_check = True
                        self.game.snake.reset()

            if break_check:
                break

    def get_current_state(self):
        # get relative fruit position
        fruit_pos = self.game.fruit.pos
        head_pos = self.game.snake.body[0]
        rel_pos = fruit_pos - head_pos
        #print("rel_pos = ", rel_pos)
        if Vector2.dot(up, rel_pos) > 0:
            if Vector2.dot(left, rel_pos) > 0:
                self.fruit_state = 'UL'
            elif Vector2.dot(right, rel_pos) > 0:
                self.fruit_state = 'UR'
            else:
                self.fruit_state = 'U'
        elif Vector2.dot(down, rel_pos) > 0:
            if Vector2.dot(left, rel_pos) > 0:
                self.fruit_state = 'DL'
            elif Vector2.dot(right, rel_pos) > 0:
                self.fruit_state = 'DR'
            else:
                self.fruit_state = 'D'
        elif Vector2.dot(left, rel_pos) > 0:
            self.fruit_state = 'L'
        elif Vector2.dot(right, rel_pos) > 0:
            self.fruit_state = 'R'

        # check obstacles, neighbouring num_check_squares squares
        if self.num_check_squares >= 4:
            positions = [head_pos+up, head_pos+left, head_pos+right, head_pos+down]
        if self.num_check_squares >= 8:
            positions += [head_pos+up+left, head_pos+up+right,
                          head_pos+down+left, head_pos+down+right]
        if self.num_check_squares == 12:
            positions += [head_pos+2*up, head_pos+2*down, head_pos+2*left, head_pos+2*right]

        obstacle_state = [0 for i in range(self.num_check_squares)]
        for index, position in enumerate(positions):
            if position in self.game.snake.body[1:]:
                obstacle_state[index] = 1
            if not (0 <= position.x < self.game.cell_number) or not (0 <= position.y < self.game.cell_number):
                obstacle_state[index] = 1

        self.obstacle_state = tuple(obstacle_state)
        self.state = (self.fruit_state, self.obstacle_state)

    def choose_action(self):
        # epsilon greedy action selection
        Qvals = np.zeros([len(self.actions)])
        for index, action in enumerate(self.actions):
            Qvals[index] = self.Q[(self.state, action)]
        num_actions = len(self.actions)
        weights = np.zeros([len(self.actions)])
        max_Q = np.max(Qvals)
        max_indices = []
        for index, action in enumerate(self.actions):
            if Qvals[index] == max_Q:
                max_indices.append(index)

        max_index = random.choice(max_indices)
        for index, action in enumerate(self.actions):
            if index != max_index:
                weights[index] = self.epsilon/num_actions
            else:
                weights[index] = 1-self.epsilon + self.epsilon/num_actions

        self.policy = weights
        self.action = random.choices(self.actions, weights, k=1)[0]

    def next_state(self):
        # move to next state
        for index, action in enumerate(self.actions):
            if action == self.action and self.game.snake.direction != directions[3-index]:
                self.game.snake.direction = directions[index]
                break
        self.game.update()
        self.game.screen.fill((146, 239, 83))
        self.game.draw_elements()
        pygame.display.update()
        self.game.clock.tick(60)

    def get_reward(self):
        self.reward = 0
        if self.score_increased:
            self.reward += fruit_reward
        else:
            fruit_directions = list(self.fruit_state)
            for fruit_direction in fruit_directions:
                snake_direction = self.game.snake.direction
                if fruit_direction == 'U' and snake_direction == up:
                    self.reward += correct_direction_reward
                    break
                elif fruit_direction == 'R' and snake_direction == right:
                    self.reward += correct_direction_reward
                    break
                elif fruit_direction == 'L' and snake_direction == left:
                    self.reward += correct_direction_reward
                    break
                elif fruit_direction == 'D' and snake_direction == down:
                    self.reward += correct_direction_reward
                    break
            self.reward += step_reward

        if self.game.failed:
            self.reward = fail_reward

    def Q_update(self):
        if self.learning_type == 'Q_learning':
            Qvals = []
            for action in self.actions:
                Qvals.append(self.Q[(self.state, action)])
            return np.max(Qvals)
        elif self.learning_type == 'SARSA':
            return self.Q[(self.state, self.action)]
        elif self.learning_type == 'Expected_SARSA':
            q_sum = 0
            for index, probability in enumerate(self.policy):
                q_sum += probability*self.Q[(self.state, self.actions[index])]
            return q_sum


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare", type=str, default='no')
    parser.add_argument("--mode", type=str, default='Q_learning')
    parser.add_argument("--train", type=str, default='yes')
    args = parser.parse_args()
    learning_types = ['Q_learning', 'SARSA', 'Expected_SARSA']
    if args.compare == 'yes':
        for learning_type in learning_types:
            agent = Agent(learning_type, 'yes', args.train)
            agent.check_learning()
        plt.title('performance comparison')
        plt.show()
    elif args.compare == 'no':
        if args.mode in learning_types:
            agent = Agent(args.mode, training=args.train)
            agent.check_learning()
            plt.title('performance evaluation')
            plt.show()
        else:
            print("Invalid mode, try from 'Q_learning','SARSA','Expected_SARSA'")
    sys.exit()
