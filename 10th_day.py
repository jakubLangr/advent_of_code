import pandas as pd
import numpy as np
import string
import matplotlib.pylab as plt
from scipy import sparse

TESTING = True
REAL = not TESTING

test_input = [
"position=< 9,  1> velocity=< 0,  2>",
"position=< 7,  0> velocity=<-1,  0>",
"position=< 3, -2> velocity=<-1,  1>",
"position=< 6, 10> velocity=<-2, -1>",
"position=< 2, -4> velocity=< 2,  2>",
"position=<-6, 10> velocity=< 2, -2>",
"position=< 1,  8> velocity=< 1, -1>",
"position=< 1,  7> velocity=< 1,  0>",
"position=<-3, 11> velocity=< 1, -2>",
"position=< 7,  6> velocity=<-1, -1>",
"position=<-2,  3> velocity=< 1,  0>",
"position=<-4,  3> velocity=< 2,  0>",
"position=<10, -3> velocity=<-1,  1>",
"position=< 5, 11> velocity=< 1, -2>",
"position=< 4,  7> velocity=< 0, -1>",
"position=< 8, -2> velocity=< 0,  1>",
"position=<15,  0> velocity=<-2,  0>",
"position=< 1,  6> velocity=< 1,  0>",
"position=< 8,  9> velocity=< 0, -1>",
"position=< 3,  3> velocity=<-1,  1>",
"position=< 0,  5> velocity=< 0, -1>",
"position=<-2,  2> velocity=< 2,  0>",
"position=< 5, -2> velocity=< 1,  2>",
"position=< 1,  4> velocity=< 2,  1>",
"position=<-2,  7> velocity=< 2, -2>",
"position=< 3,  6> velocity=<-1, -1>",
"position=< 5,  0> velocity=< 1,  0>",
"position=<-6,  0> velocity=< 2,  0>",
"position=< 5,  9> velocity=< 1, -2>",
"position=<14,  7> velocity=<-2,  0>",
"position=<-3,  6> velocity=< 2, -1>"
        ]


def parse_file(inputs: list):
    update_dict = {}
    list1 = string.ascii_uppercase
    list2 = string.ascii_lowercase
    ids = [ str(p1 + p2) for p1 in list1 for p2 in list2]
    max_n = min_n = 0
    for i in range(len(inputs)):
        p, v  = inputs[i].split("> ")
        p = p.split('=')[1][1:].strip()
        v = v.split("=")[1][1:-1].strip()
        
        x, y = p.split(', ')
        d_x, d_y = v.split(', ')
        
        if int(x) > max_n:
            max_n = int(x)
        if int(x) < min_n:
            min_n = int(x)
        
        update_dict[ids[i]] = int(x), int(y), int(d_x), int(d_y)
        
        
        target_range = max_n - min_n
    return update_dict, target_range



def construct_mat(ud, target_range):
    msg_matrix = np.zeros((target_range, target_range), dtype='object')
    for k in ud.keys():
        x,y,d_x,d_y = ud[k]
        msg_matrix[x,y] = k
    return msg_matrix



def plot_matrix(mat): 
    to_int = lambda x: 1 if isinstance(x, str) else x
    vto_int = np.vectorize(to_int)
    num_array = vto_int(mat)
    plt.imshow(num_array)
    plt.show()
    return num_array
    


# print(msg_matrix)

def update_matrix(msg_matrix, ud, target_range):
    for k in ud.keys():
        x,y,d_x,d_y = ud[k]
        new_x = x + d_x
        new_y = y + d_y
        ud[k] = new_x, new_y, d_x, d_y
        msg_matrix = construct_mat(ud, target_range)
    return msg_matrix, ud
    

def find_msg(curr_epoch, ud, target_range, num_iter=5):
    for i in range(num_iter):
        curr_epoch, ud = update_matrix(curr_epoch, ud, target_range)
        curr_n = plot_matrix(curr_epoch)

if TESTING:
    ud, target_range = parse_file(test_input)
    msg_matrix = construct_mat(ud, target_range)
    find_msg(msg_matrix, ud, target_range)

if REAL:
    real_input = open('day10_input.txt','r').read().split('\n')
    ud, target_range = parse_file(real_input)
    curr_epoch = construct_mat(ud, target_range)
    # find_msg(msg_matrix, ud, target_range)
    
    num_iter = 1
    curr_epoch, ud = update_matrix(curr_epoch, ud, target_range)
    curr_n = plot_matrix(curr_epoch)
