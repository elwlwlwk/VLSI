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

    best_path= path[0:]
    best_score= 99999999999999999999999

    for i in range(100):
        idxs= sample(range(len(best_path)), 3)
        idxs.sort()
        idx1= idxs[0]
        idx2 = idxs[1]
        idx3 = idxs[2]

        sub_path1 = best_path[0:idx1]
        sub_path2 = best_path[idx1:idx2]
        sub_path3 = best_path[idx2:idx3]
        sub_path4 = best_path[idx3:]

        rev_sub_path2 = list(reversed(sub_path2))
        rev_sub_path3 = list(reversed(sub_path3))

        new_paths=[]
        new_paths.append(sub_path1 + rev_sub_path2 + sub_path3 + sub_path4)
        new_paths.append(sub_path1 + sub_path2 + rev_sub_path3 + sub_path4)
        new_paths.append(sub_path1 + rev_sub_path2 + rev_sub_path3 + sub_path4)
        new_paths.append(sub_path1 + sub_path3 + sub_path2 + sub_path4)
        new_paths.append(sub_path1 + rev_sub_path3 + sub_path2 + sub_path4)
        new_paths.append(sub_path1 + sub_path3 + rev_sub_path2 + sub_path4)
        new_paths.append(sub_path1 + rev_sub_path3 + rev_sub_path2 + sub_path4)

        scores= list(map(lambda x: calc_score(x, cost_mat), new_paths))
        cur_score = min(scores)
        if(cur_score< best_score):
            best_path = new_paths[scores.index(min(scores))][0:]
            best_score= cur_score
    return best_path

def gen_trial_path_2opt(path, cost_mat):
    ori= path[0:]
    idxs= sample(range(len(ori)), 2 )
    idxs.sort()
    idx1= idxs[0]
    idx2 = idxs[1]
    new_path = ori[0:idx1]+ list(reversed(ori[idx1:idx2]))+ ori[idx2:]
    return new_path

def simple_sa(data, cost_mat):
    temperature = 10
    delta_temperature = 0.95

    cur_path = gen_random_path(data)
    cur_score = calc_score(cur_path, cost_mat)

    best_path = cur_path
    best_score = cur_score

    counter = 0
    while temperature > 1:
        # trial_path= gen_trial_path_2opt(cur_path, cost_mat)
        trial_path = gen_trial_path_3opt(cur_path, cost_mat)
        trial_score = calc_score(trial_path, cost_mat)
        if random() < calc_prob(cur_score, trial_score, temperature):
            if (cur_score < trial_score):
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            cur_path = trial_path
            cur_score = trial_score
        temperature *= delta_temperature
        if cur_score < best_score:
            best_score = cur_score
            best_path = cur_path

        print(cur_score, temperature)

    print("result score: %s" % best_score)
    return best_path, best_score

def dnc_sa(data):
    import math
    chunk_size = 150
    chunk_num = math.ceil(math.sqrt(len(data) / chunk_size))

    x_min = min(map(lambda x: x[1], data))
    y_min = min(map(lambda x: x[2], data))
    chunk_x_size = (max(map(lambda x: x[1], data)) + 1 - min(map(lambda x: x[1], data))) / chunk_num
    chunk_y_size = (max(map(lambda x: x[2], data)) + 1 - min(map(lambda x: x[2], data))) / chunk_num

    chunks = [[[] for i in range(chunk_num)] for j in range(chunk_num)]

    cost_mat = calc_cost_mat(data)

    for datum in data:
        chunks[math.floor((datum[1] - x_min) / chunk_x_size)][math.floor((datum[2] - y_min) / chunk_y_size)].append(
            datum)
    paths = [[[] for i in range(chunk_num)] for j in range(chunk_num)]
    scores = [[[] for i in range(chunk_num)] for j in range(chunk_num)]
    for row in range(len(chunks)):
        for col in range(len(chunks[0])):
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            paths[row][col], scores[row][col] = simple_sa(chunks[row][col], cost_mat)
    path = []

    for row in range(len(chunks)):
        if row % 2 == 0:
            for col in range(len(chunks[0])):
                path += paths[row][col]
        else:
            for col in reversed(range(len(chunks[0]))):
                path += paths[row][col]
    score= calc_score(path, cost_mat)
    print("result score: %s" % score)

    return path, score


if __name__=='__main__':
    tsp_file_name='xqc2175.tsp'
    #tsp_file_name= list(filter(lambda x: 'tsp' == x[-3:], os.listdir()))[0]
    with open(tsp_file_name) as f:
        raw_data= f.read().split('\n')
    data= list(map(lambda row: list(map(lambda x: int(x), row.split())), raw_data))

    best_path, best_score= dnc_sa(data)

    from pylab import *
    from matplotlib.pyplot import figure, plot
    figure()
    x= list(map(lambda x: data[x-1][1], best_path))
    y= list(map(lambda x: data[x - 1][2], best_path))
    plot(x, y, 'ro')
    plot(x, y)
    show()