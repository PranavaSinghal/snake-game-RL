import argparse
import sys
import numpy as np
parser = argparse.ArgumentParser()


class MDP():
    def __init__(self, file):
        data = file.readlines()
        self.transition = np.array([[0, 0, 0, 0, 0]])
        for line in data:
            words = line[:-1].split()
            if words[0] == 'numStates':
                self.numStates = int(words[1])
            elif words[0] == 'numActions':
                self.numActions = int(words[1])
            elif words[0] == 'start':
                self.start = int(words[1])
            elif words[0] == 'end':
                self.end = [int(x) for x in np.array((words[1:]))]
            elif words[0] == 'mdptype':
                self.mdptype = words[1]
            elif words[0] == 'discount':
                self.gamma = float(words[1])
            elif words[0] == 'transition':
                tr = [float(x) for x in words[1:]]
                self.transition = np.append(self.transition, [np.array(tr)], axis=0)
            else:
                print("error in file")
                sys.exit(0)
        self.init_transition()

    def init_transition(self):
        '''
        initialises
        1) reward matrix r(s1,ac,s2)
        2) transition probability matrix p(s1,ac,s2)
        '''
        self.transition = self.transition[1:].T
        s1, ac, s2, r, p = self.transition
        self.S = np.unique(np.append(s1, s2))  # set of states
        self.A = np.unique(ac)  # set of actions
        reward = np.array([s1, ac, s2, r])  # r(s1,ac,s2)
        probability = np.array([s1, ac, s2, p])  # p(s1,ac,s2)
        self.pmatrix = [[[0 for x in range(len(self.S))]
                         for y in range(len(self.A))] for z in range(len(self.S))]
        self.rmatrix = [[[0 for x in range(len(self.S))]
                         for y in range(len(self.A))] for z in range(len(self.S))]
        for state1 in self.S:
            for action in self.A:
                for state2 in self.S:
                    for i in range(probability[0].size):
                        x, y, z = int(state1), int(action), int(state2)
                        if(state1 == probability[0][i] and
                           action == probability[1][i] and
                           state2 == probability[2][i]):
                            self.pmatrix[x][y][z] = probability[3][i]
                            self.rmatrix[x][y][z] = reward[3][i]
                            break
                        else:
                            self.pmatrix[x][y][z] = 0
                            self.rmatrix[x][y][z] = 0

        self.pmatrix = np.array(self.pmatrix)
        self.rmatrix = np.array(self.rmatrix)
        # self.test()

    def test(self):
        print("Testing input...")
        print(f"numStates = {self.numStates}")
        print(f"numActions = {self.numActions}")
        print(f"start = {self.start}")
        print(f"end = {self.end}")
        print(f"transition = {self.transition} with dimensions = {self.transition.shape}")
        print(f"mdptype = {self.mdptype}")
        print(f"gamma = {self.gamma}")
        print(f"Set of states = {self.S}, Set of actions = {self.A}")
        print("pmatrix = ", self.pmatrix)
        print("rmatrix = ", self.rmatrix)


class ValueIteration():
    def __init__(self, infile, outfile):
        self.mdp = MDP(infile)
        self.v = np.linspace(0, 0, self.mdp.numStates)
        self.policy = np.linspace(0, 0, self.mdp.numStates)
        self.probability = self.mdp.pmatrix
        self.reward = self.mdp.rmatrix
        self.discount = self.mdp.gamma
        self.update()
        length = len(self.v)
        for i in range(length):
            outfile.write(str(self.v[i])+' '+str(self.policy[i])+'\n')

    def update_once(self):
        for state1 in self.mdp.S:
            state1 = int(state1)
            val_array = []
            for action in self.mdp.A:
                action = int(action)
                new_v = 0
                flag = False  # stays false if (state1, action) is an invalid pair
                for state2 in self.mdp.S:
                    state2 = int(state2)
                    if self.probability[state1][action][state2] != 0:
                        flag = True
                    new_v += (self.reward[state1][action][state2] + self.discount *
                              self.v[state2])*self.probability[state1][action][state2]

                if flag:
                    val_array.append([new_v, action])

            if(val_array == []):
                pass
            else:
                self.policy[state1] = val_array[0][1]
                self.v[state1] = val_array[0][0]
                for new_value, action in val_array:
                    if new_value > self.v[state1]:  # approximation to optimal value function and policy
                        self.policy[state1] = action
                        self.v[state1] = new_value

    def update(self, epsilon=0.001):
        while True:
            oldv = np.array(self.v)
            self.update_once()
            #print("current value =", self.v)
            if max(abs(self.v - oldv)) < epsilon:
                break


parser.add_argument('--mdp', type=str)
parser.add_argument('--algorithm', type=str)
parser.add_argument('--outf', type=str)
args = parser.parse_args()
if not args.algorithm == 'vi':
    print("algorithm should be \'vi\'")
    sys.exit(0)
infile = open(args.mdp, 'r')
outfile = open(args.outf, 'w')
vi = ValueIteration(infile, outfile)
