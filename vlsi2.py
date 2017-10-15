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

def get_inter_cost(paths, cost_mat):
    inter_cost=0
    last_point= -1
    first_point= -1
    for idx in range(len(paths)-1):
        if len(paths[idx])!= 0:
            last_point= paths[idx][-1]-1
        if len(paths[idx+1])!= 0:
            first_point= paths[idx+1][0]-1
        if last_point!= -1 and first_point!= -1:
            inter_cost+= cost_mat[first_point][last_point]
            last_point= -1
            first_point= -1
    return inter_cost

def gen_trial_path_3opt(path, cost_mat):

    best_path= path[0:]
    best_score= 99999999999999999999999

    for i in range(500):
        idxs= sample(range(len(best_path)), 3)
        idxs.sort()
        idx1= idxs[0]
        idx2 = idxs[1]
        idx3 = idxs[2]

        sub_path1 = best_path[0:idx1]
        sub_path2 = best_path[idx1:idx2]
        sub_path3 = best_path[idx2:idx3]
        sub_path4 = best_path[idx3:]

        sub_path1_cost= calc_score(sub_path1, cost_mat)
        sub_path2_cost = calc_score(sub_path2, cost_mat)
        sub_path3_cost = calc_score(sub_path3, cost_mat)
        sub_path4_cost = calc_score(sub_path4, cost_mat)


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

        scores=[]

        part_cost_sum= sub_path1_cost+sub_path2_cost+sub_path3_cost+sub_path4_cost
        scores.append(part_cost_sum+ get_inter_cost([
            sub_path1,
            rev_sub_path2,
            sub_path3,
            sub_path4
        ], cost_mat))
        scores.append(part_cost_sum+ get_inter_cost([
            sub_path1,
            sub_path2,
            rev_sub_path3,
            sub_path4
        ], cost_mat))
        scores.append(part_cost_sum+ get_inter_cost([
            sub_path1,
            rev_sub_path2,
            rev_sub_path3,
            sub_path4
        ], cost_mat))
        scores.append(part_cost_sum+ get_inter_cost([
            sub_path1,
            sub_path3,
            sub_path2,
            sub_path4
        ], cost_mat))
        scores.append(part_cost_sum+ get_inter_cost([
            sub_path1,
            rev_sub_path3,
            sub_path2,
            sub_path4
        ], cost_mat))
        scores.append(part_cost_sum+ get_inter_cost([
            sub_path1,
            sub_path3,
            rev_sub_path2,
            sub_path4
        ], cost_mat))
        scores.append(part_cost_sum+ get_inter_cost([
            sub_path1,
            rev_sub_path3,
            rev_sub_path2,
            sub_path4
        ], cost_mat))

        #scores= list(map(lambda x: calc_score(x, cost_mat), new_paths))

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
    delta_temperature = 0.97

    cur_path = list(map(lambda x: x[0], data))
    cur_score = calc_score(cur_path, cost_mat)

    best_path = cur_path
    best_score = cur_score

    counter = 0
    while temperature > 1:
        # trial_path= gen_trial_path_2opt(cur_path, cost_mat)
        trial_path = [cur_path[0]]+gen_trial_path_3opt(cur_path[1:-1], cost_mat)+[cur_path[-1]]
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
    chunk_size = 200
    chunk_num = math.ceil(math.sqrt(len(data) / chunk_size))

    x_min = min(map(lambda x: x[1], data))
    y_min = min(map(lambda x: x[2], data))
    chunk_x_size = (max(map(lambda x: x[1], data)) + 1 - min(map(lambda x: x[1], data))) / chunk_num
    chunk_y_size = (max(map(lambda x: x[2], data)) + 1 - min(map(lambda x: x[2], data))) / chunk_num

    chunks = [[[] for i in range(chunk_num)] for j in range(chunk_num)]

    cost_mat = calc_cost_mat(data)

    for datum in data:
        chunks[math.floor((datum[2] - y_min) / chunk_y_size)][math.floor((datum[1] - x_min) / chunk_x_size)].append(
            datum)

    for row in range(len(chunks)):
        if row % 2 == 0:
            for col in range(len(chunks[0])):
                if col==0:
                    sorted_chunk = sorted(chunks[row][col], key=lambda x: ((x[1]-chunk_x_size*col) ** 2 + (x[2]- chunk_y_size*row) ** 2))
                    chunks[row][col]= sorted_chunk
                    last= sorted_chunk[-1]
                    first= sorted_chunk[0]
                else:
                    sorted_chunk = sorted(chunks[row][col], key= lambda x:((x[1]-chunk_x_size*col) ** 2 + (x[2]- chunk_y_size*row) **2))
                    chunks[row][col] = sorted_chunk
                    last= sorted_chunk[-1]
                    sorted_chunk = sorted(chunks[row][col], key=lambda x: ((chunk_x_size*(col+1)-x[1]) ** 2 + (x[2]- chunk_y_size*row) ** 2))
                    first= sorted_chunk[-1]
                chunks[row][col].remove(last)
                chunks[row][col].remove(first)
                chunks[row][col] = [first] + chunks[row][col] + [last]
        else:
            for col in reversed(range(len(chunks[0]))):
                if col==len(chunks[0])-1:
                    sorted_chunk = sorted(chunks[row][col], key=lambda x: ((chunk_x_size*(col+1)-x[1]) ** 2 + (x[2]- chunk_y_size*row) ** 2))
                    chunks[row][col] = sorted_chunk
                    last= sorted_chunk[-1]
                    first= sorted_chunk[0]
                else:
                    sorted_chunk = sorted(chunks[row][col], key= lambda x:((x[1]-chunk_x_size*col)**2+ (x[2]- chunk_y_size*row) ** 2))
                    first= sorted_chunk[-1]
                    sorted_chunk = sorted(chunks[row][col], key=lambda x: ((chunk_x_size*(col+1)-x[1]) ** 2 + (x[2]- chunk_y_size*row) ** 2))
                    chunks[row][col] = sorted_chunk
                    last= sorted_chunk[-1]
                chunks[row][col].remove(last)
                chunks[row][col].remove(first)
                chunks[row][col] = [first] + chunks[row][col] + [last]

    paths = [[[] for i in range(chunk_num)] for j in range(chunk_num)]
    scores = [[[] for i in range(chunk_num)] for j in range(chunk_num)]
    for row in range(len(chunks)):
        for col in range(len(chunks[0])):
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            paths[row][col], scores[row][col] = simple_sa(chunks[row][col], cost_mat)
    path = []
    part_sum_score=0
    for row in range(len(chunks)):
        if row % 2 == 0:
            for col in range(len(chunks[0])):
                path += paths[row][col]
                part_sum_score+= scores[row][col]
        else:
            for col in reversed(range(len(chunks[0]))):
                path += paths[row][col]
                part_sum_score += scores[row][col]
    score= calc_score(path, cost_mat)
    print("part sum score: %s" % part_sum_score)
    print("total result score: %s" % score)

    return path, score


if __name__=='__main__':
    tsp_file_name='pbd984.tsp'
    #tsp_file_name= list(filter(lambda x: 'tsp' == x[-3:], os.listdir()))[0]
    with open(tsp_file_name) as f:
        raw_data= f.read().split('\n')
    data= list(map(lambda row: list(map(lambda x: int(x), row.split())), raw_data))

    #best_path, best_score= dnc_sa(data)
    #best_path, best_score= simple_sa(data, calc_cost_mat(data))
    best_path=[20,102,77,35,3,40,41,9,10,11,86,85,84,83,82,81,115,167,166,136,134,163,195,216,202,205,206,207,208,209,210,211,170,139,116,138,169,168,137,87,88,89,45,44,43,42,12,13,46,14,15,16,17,18,52,51,50,49,48,47,91,92,93,94,53,54,19,55,56,95,96,57,21,22,97,112,125,149,180,239,238,237,236,235,196,179,148,124,111,123,147,178,122,146,177,176,145,121,120,143,144,175,212,174,119,142,173,172,141,118,110,90,109,117,140,171,194,231,232,233,234,268,282,290,301,314,312,300,289,281,267,266,280,288,299,311,349,350,351,352,353,354,355,356,357,358,315,302,291,283,269,271,284,292,303,316,360,359,404,403,402,433,434,435,458,473,493,492,491,490,489,488,487,486,485,472,457,428,429,430,431,432,401,399,398,397,396,395,427,394,456,471,470,390,391,392,393,348,347,346,345,344,343,342,319,309,297,286,278,298,310,287,279,265,253,244,274,270,313,330,333,337,400,466,505,511,514,522,523,507,508,509,510,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,979,732,710,692,676,660,731,709,691,675,659,730,708,690,674,658,729,707,689,673,657,688,672,656,639,647,733,727,706,728,746,752,768,769,770,771,772,773,774,775,776,777,778,779,780,818,849,817,816,848,815,814,813,812,811,810,809,808,807,913,801,858,851,916,946,951,957,975,976,965,874,914,865,875,892,915,958,977,978,943,944,945,947,966,967,948,931,919,918,917,893,894,876,895,877,854,853,825,824,823,822,852,850,821,820,819,781,782,783,784,785,755,756,757,735,712,694,678,642,641,640,662,734,711,693,677,661,581,588,600,617,616,615,614,613,599,587,598,597,624,612,611,608,618,606,594,585,572,549,555,556,557,558,559,560,561,562,563,564,565,566,567,568,569,570,547,546,545,512,513,515,516,517,518,519,520,521,506,482,483,484,476,469,468,467,455,465,481,480,479,478,477,504,503,502,460,475,501,500,499,498,497,496,544,543,494,495,474,459,436,437,438,439,440,441,442,443,448,450,451,461,452,445,417,416,444,415,414,413,412,411,410,409,408,407,406,405,361,362,363,331,320,317,304,293,272,215,214,213,181,150,182,151,152,183,184,153,126,99,98,58,23,59,60,100,101,127,154,185,186,155,128,103,64,63,62,61,24,25,65,104,66,26,67,68,69,27,70,71,28,29,30,72,108,73,31,32,74,132,161,198,191,160,131,130,107,106,105,129,156,187,157,188,189,158,159,190,197,217,218,240,241,219,242,223,199,200,220,224,225,226,227,228,229,221,222,203,201,192,162,133,113,164,135,114,75,34,33,2,36,4,5,37,76,78,6,38,39,7,8,80,79,165,193,204,230,264,263,262,252,251,250,249,248,247,246,245,243,255,256,257,258,259,260,261,285,295,306,327,326,325,324,323,322,341,340,321,305,294,254,277,276,275,273,332,364,365,366,367,368,334,369,370,335,371,372,373,374,336,375,338,339,379,378,377,376,419,418,446,462,453,463,464,454,449,447,420,380,381,382,421,383,384,385,422,423,386,387,388,389,424,425,426,329,318,308,296,307,328,1,984,983,982,981,980,968,969,953,952,932,924,900,882,899,923,881,867,880,898,922,879,897,950,949,920,896,921,878,866,856,855,826,827,828,829,830,857,831,832,833,834,835,859,868,883,901,925,933,902,926,970,971,954,955,956,934,972,973,974,940,939,938,937,964,963,962,961,960,959,936,935,907,887,929,908,888,872,842,802,843,844,864,873,889,909,910,890,891,911,912,930,941,942,847,846,845,806,805,804,803,767,766,765,764,763,762,761,760,759,744,723,703,685,669,702,722,701,668,684,721,749,750,758,800,799,798,797,796,839,838,837,862,840,841,863,871,870,886,906,905,885,928,904,903,927,884,869,861,860,836,795,794,793,792,791,754,790,789,788,787,786,753,747,738,714,713,737,736,643,644,645,663,679,695,664,680,696,715,739,716,740,748,741,717,697,681,665,646,633,632,631,630,629,628,627,626,625,607,601,589,582,577,571,578,583,590,602,573,579,584,591,603,604,592,574,575,576,593,605,621,620,619,648,666,682,698,718,742,743,719,699,720,700,683,667,649,634,650,635,636,637,638,651,652,670,686,704,724,653,671,687,705,725,726,745,751,655,654,622,623,609,610,596,554,553,552,551,550,580,586,595,548]

    from pylab import *
    from matplotlib.pyplot import figure, plot
    figure()
    x= list(map(lambda x: data[x-1][1], best_path))
    y= list(map(lambda x: data[x - 1][2], best_path))
    plot(x, y, 'ro')
    plot(x, y)
    show()