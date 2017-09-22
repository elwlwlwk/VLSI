import os
from math import sqrt, e
from random import sample, random

def calc_cost_mat(data):
    cost_mat=[[0]*len(data) for i in range(len(data))]
    for i in range(len(data)):
        for j in range(len(data)):
            p1= data[i]
            p2= data[j]
            distance= sqrt((p1[1]-p2[1])**2+(p1[2]-p2[2])**2)
            cost_mat[p1[0]-1][p2[0]-1]= cost_mat[p2[0]-1][p1[0]-1]= distance
    return cost_mat

def calc_score(path, cost_mat):
    cost=0
    for i in range(len(path)-1):
        cost+= cost_mat[path[i]-1][path[i+1]-1]
    return cost

def gen_random_path(data):
    return list(map(lambda x: x[0], sample(data, len(data))))

def calc_prob(best_score, trial_score, temperature):
    if best_score> trial_score:
        return 1
    else:
        #print(e**((best_score-trial_score)/temperature))
        return e**((best_score-trial_score)/temperature)

def gen_trial_path_3opt(path, cost_mat):
    ori= path[0:]
    idxs= sample(range(len(ori)), 3 )
    idxs.sort()
    idx1= idxs[0]
    idx2 = idxs[1]
    idx3 = idxs[2]

    new_paths=[]
    new_paths.append(ori[0:idx1] + list(reversed(ori[idx1:idx2])) + ori[idx2:idx3] + ori[idx3:])
    new_paths.append(ori[0:idx1] + list(reversed(ori[idx1:idx2])) + list(reversed(ori[idx2:idx3])) + ori[idx3:])
    new_paths.append(ori[0:idx1] + ori[idx1:idx2] + list(reversed(ori[idx2:idx3])) + ori[idx3:])
    new_paths.append(ori[0:idx1] + ori[idx2:idx3] + ori[idx1:idx2] + ori[idx3:])
    new_paths.append(ori[0:idx1] + list(reversed(ori[idx2:idx3])) + ori[idx1:idx2] + ori[idx3:])
    new_paths.append(ori[0:idx1] + ori[idx2:idx3] + list(reversed(ori[idx1:idx2])) + ori[idx3:])
    new_paths.append(ori[0:idx1] + list(reversed(ori[idx2:idx3])) + list(reversed(ori[idx1:idx2])) + ori[idx3:])

    scores= list(map(lambda x: calc_score(x, cost_mat), new_paths))
    return new_paths[scores.index(min(scores))]

def gen_trial_path_2opt(path, cost_mat):
    ori= path[0:]
    idxs= sample(range(len(ori)), 2 )
    idxs.sort()
    idx1= idxs[0]
    idx2 = idxs[1]
    new_path = ori[0:idx1]+ list(reversed(ori[idx1:idx2]))+ ori[idx2:]
    return new_path



if __name__=='__main__':

    temperature = 5
    delta_temperature = 0.99995

    tsp_file_name= list(filter(lambda x: 'tsp' == x[-3:], os.listdir()))[0]
    with open(tsp_file_name) as f:
        raw_data= f.read().split('\n')[8:-2]
    data= list(map(lambda row: list(map(lambda x: int(x), row.split())), raw_data))
    cost_mat = calc_cost_mat(data)

    cur_path= gen_random_path(data)
    cur_score= calc_score(cur_path, cost_mat)

    best_path= cur_path
    best_score= cur_score

    counter=0
    while temperature > 1:
        #trial_path= gen_trial_path_2opt(cur_path, cost_mat)
        trial_path = gen_trial_path_3opt(cur_path, cost_mat)
        trial_score= calc_score(trial_path, cost_mat)
        if random() < calc_prob(cur_score, trial_score, temperature):
            cur_path= trial_path
            cur_score= trial_score
        temperature*=delta_temperature
        if cur_score < best_score:
            best_score= cur_score
            best_path= cur_path

        if counter % 10000 == 0:
            print(cur_score, temperature)

        counter+=1
    print("result score: %s" % best_score)

    from pylab import *
    from matplotlib.pyplot import figure, plot
    figure()
    x= list(map(lambda x: data[x-1][1], best_path))
    y= list(map(lambda x: data[x - 1][2], best_path))
    plot(x, y, 'ro')
    plot(x, y)
show()