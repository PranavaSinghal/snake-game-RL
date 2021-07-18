import argparse
import sys
import numpy as np
parser = argparse.ArgumentParser()


def valid(i, j, y_size, x_size, maze):
    if 0 <= i and i < y_size:
        if 0 <= j and j < x_size:
            if maze[i][j] != 1:
                return True
    else:
        return False


def encoder(filename):
    printf = open(r'mdpfile.txt', mode='w')
    data = filename.readlines()
    i = 0
    y_size = len(data)
    x_size = len(data[0].split())
    numStates = x_size*y_size
    numActions = 4
    start = 0
    end = []
    maze = np.zeros(shape=[y_size, x_size])
    outcome = np.zeros(shape=[4, y_size, x_size, 4])
    '''
    outcome stores [i_final, j_final, reward, probability]
    initial state = (i,j), actions from W,N,E,S
    final state = (y,x), reward r (-infinity if not allowed)
    '''
    for line in data:
        words = line.split()
        maze[i] = [int(x) for x in words]
        i = i+1

    # actions {'W': 0, 'N': 1, 'E': 2, 'S': 3} move West, North, East and South
    for i in range(y_size):
        for j in range(x_size):
            gridval = maze[i][j]
            if gridval == 1:  # wall
                for action in range(4):
                    outcome[action][i][j] = [i, j, 0, 0]
            if gridval == 0 or gridval == 2:  # empty block/start
                for action in range(4):
                    if action == 0:  # west
                        if valid(i, j-1, y_size, x_size, maze):
                            outcome[action][i][j] = [i, j-1, -1, 1]
                        else:
                            outcome[action][i][j] = [i, j, 0, 0]
                    elif action == 1:  # north
                        if valid(i-1, j, y_size, x_size, maze):
                            outcome[action][i][j] = [i-1, j, -1, 1]
                        else:
                            outcome[action][i][j] = [i, j, 0, 0]
                    elif action == 2:  # east
                        if valid(i, j+1, y_size, x_size, maze):
                            outcome[action][i][j] = [i, j+1, -1, 1]
                        else:
                            outcome[action][i][j] = [i, j, 0, 0]
                    elif action == 3:  # south
                        if valid(i+1, j, y_size, x_size, maze):
                            outcome[action][i][j] = [i+1, j, -1, 1]
                        else:
                            outcome[action][i][j] = [i, j, 0, 0]
            if gridval == 3:  # end state
                end.append(i*x_size+j)
                for action in range(4):
                    outcome[action][i][j] = [i, j, 0, 1]
            if gridval == 2:  # start state
                start = i*x_size + j

    printf.write('numStates ' + str(numStates)+'\n')
    printf.write('numActions '+str(numActions)+'\n')
    printf.write('start '+str(start)+'\n')
    end_string = ''
    for x in end:
        end_string += str(x) + ' '
    printf.write('end ' + end_string+'\n')
    printf.write('mdptype episodic'+'\n')
    printf.write('discount 0.9'+'\n')

    for i in range(y_size):
        for j in range(x_size):
            for action in range(4):
                out = outcome[action][i][j]
                printf.write('transition '+str(x_size*i+j)+' '+str(action)+' ' +
                             str(out[0]*x_size+out[1])+' '+str(out[2])+' '+str(out[3])+'\n')


parser.add_argument('--grid', type=str)
args = parser.parse_args()
file = open(args.grid, 'r')
encoder(file)
