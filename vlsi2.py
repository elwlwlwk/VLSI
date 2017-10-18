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
    tsp_file_name='frv4410.tsp'
    #tsp_file_name= list(filter(lambda x: 'tsp' == x[-3:], os.listdir()))[0]
    with open(tsp_file_name) as f:
        raw_data= f.read().split('\n')
    data= list(map(lambda row: list(map(lambda x: int(x), row.split())), raw_data))

    #best_path, best_score= dnc_sa(data)
    #best_path, best_score= simple_sa(data, calc_cost_mat(data))
    best_path=[7,86,85,65,64,61,80,13,18,32,35,36,37,38,39,40,41,169,168,123,167,166,165,152,151,145,134,87,88,96,110,132,135,136,137,149,150,164,177,178,179,180,181,182,183,246,247,248,275,276,277,279,289,309,332,336,337,338,355,356,385,389,390,391,392,393,394,395,432,396,397,406,412,413,364,363,358,357,383,232,189,196,210,213,214,215,216,217,218,219,220,221,222,223,224,225,376,375,374,373,372,371,370,369,368,367,366,365,414,415,416,448,447,446,495,525,494,491,521,517,487,444,438,434,460,534,485,513,551,553,556,558,526,527,496,559,560,573,574,621,627,631,632,633,634,635,636,641,579,529,497,422,421,420,419,418,417,449,528,561,578,577,576,575,637,638,639,640,681,731,762,761,804,803,802,801,800,799,798,797,796,795,794,793,781,746,717,666,606,692,778,792,811,895,964,979,998,999,1013,1016,1017,1018,1001,1002,980,943,917,871,828,833,836,837,838,839,883,884,840,885,886,841,842,843,888,887,930,961,931,962,991,990,989,988,987,1005,1004,1003,957,928,958,929,959,960,1006,1055,1092,1099,1105,1106,1107,1108,1109,1110,1178,1219,1220,1221,1180,1179,1111,1112,1113,1138,1148,1181,1222,1242,1263,1262,1261,1260,1218,1177,1217,1176,1175,1216,1215,1174,1173,1214,1172,1212,1204,1164,1201,1163,1128,1243,1270,1251,1252,1255,1256,1257,1258,1259,1303,1301,1290,1286,1376,1285,1284,1283,1282,1281,1275,1273,1272,1248,1247,1246,1241,1200,1162,1141,1137,1136,1135,1089,1088,1087,1022,1021,1020,1019,1023,1028,1041,1045,1046,1047,1048,1049,1050,1051,1052,1053,1054,1115,1114,1182,1223,1183,1224,1264,1278,1277,1309,1308,1307,1306,1305,1362,1361,1360,1304,1359,1356,1350,1343,1400,1429,1399,1426,1461,1484,1465,1470,1436,1406,1472,1473,1474,1497,1498,1499,1500,1501,1460,1440,1439,1407,1408,1441,1409,1391,1382,1383,1392,1410,1442,1443,1490,1491,1492,1493,1524,1559,1608,1634,1633,1684,1683,1682,1632,1607,1584,1576,1558,1575,1583,1606,1631,1647,1630,1605,1604,1629,1655,1656,1657,1680,1681,1714,1713,1758,1759,1801,1826,1825,1800,1757,1756,1712,1653,1654,1628,1603,1627,1602,1601,1626,1600,1625,1652,1651,1623,1597,1621,1595,1548,1550,1552,1553,1554,1555,1556,1557,1523,1522,1521,1520,1519,1517,1508,1504,1570,1648,1662,1650,1699,1753,1755,1780,1784,1799,1824,1846,1847,1883,1884,1853,1854,1855,1827,1828,1802,1760,1715,1716,1717,1763,1762,1761,1829,1803,1804,1830,1858,1857,1856,1909,1959,2007,1979,1982,2006,2037,2038,2076,2106,2105,2104,2103,2075,2074,2073,2072,2033,2002,2034,2003,2004,2035,2055,2036,2005,1981,1978,1958,1957,1956,1955,1908,1907,1906,1905,1904,1903,1952,1953,1954,2001,2032,2000,2031,2071,2070,2069,2068,2065,2064,2021,1992,1995,2024,2025,2029,1998,1996,2030,1999,1951,1948,1944,1943,1896,1899,1902,1881,1880,1852,1822,1845,1817,1795,1781,1779,1774,1767,1832,1859,1863,1891,1972,1966,2043,2085,2080,2113,2112,2100,2088,2087,2062,2061,2060,2053,2020,1991,1980,1977,1976,1975,1941,1940,1939,1890,2107,2147,2246,2244,2274,2238,2268,2262,2232,2200,2196,2114,2115,2116,2117,2118,2164,2165,2166,2205,2206,2207,2213,2231,2261,2296,2305,2306,2307,2288,2328,2329,2310,2278,2279,2247,2248,2280,2281,2249,2250,2282,2301,2283,2251,2222,2210,2187,2186,2185,2184,2183,2180,2173,2169,2119,2130,2138,2141,2142,2143,2144,2145,2146,2188,2189,2190,2191,2252,2285,2284,2302,2325,2326,2327,2399,2398,2453,2515,2554,2588,2587,2586,2600,2599,2585,2552,2553,2514,2452,2451,2450,2449,2551,2513,2482,2471,2448,2396,2397,2349,2348,2324,2323,2322,2321,2320,2319,2315,2411,2366,2434,2437,2374,2387,2393,2394,2395,2447,2446,2511,2548,2549,2512,2550,2574,2584,2583,2582,2581,2580,2578,2543,2507,2509,2546,2547,2510,2445,2444,2499,2535,2496,2532,2577,2595,2612,2603,2665,2743,2753,2744,2773,2797,2800,2804,2774,2722,2739,2715,2692,2716,2694,2678,2672,2644,2650,2651,2652,2618,2653,2675,2685,2701,2723,2702,2724,2741,2748,2775,2776,2777,2778,2779,2780,2781,2725,2703,2686,2676,2654,2619,2655,2704,2726,2782,2808,2807,2847,2928,2963,2948,2846,2806,2866,2873,2899,2927,2947,2962,2961,2960,2957,2956,2914,2887,2920,2893,2895,2923,2897,2925,2926,2898,2845,2805,2844,2843,2839,2837,2786,2858,2833,2864,2865,2949,2965,2992,3055,3056,3057,3105,3106,3107,3110,3124,3164,3209,3214,3215,3216,3253,3254,3261,3270,3246,3249,3220,3165,3125,3131,3171,3225,3230,3233,3179,3138,3183,3140,3141,3184,3234,3235,3236,3237,3266,3213,3238,3239,3190,3147,3189,3146,3084,3024,3023,3083,3082,3081,3109,3117,3145,3188,3212,3187,3144,3143,3186,3185,3142,3079,3080,3021,3022,2982,2981,3020,3019,3018,3078,3077,3017,3014,3074,3067,3061,3004,2993,3100,3093,3195,3267,3308,3461,3433,3405,3358,3357,3356,3432,3431,3404,3384,3379,3355,3378,3383,3403,3430,3448,3429,3402,3401,3428,3353,3354,3307,3306,3305,3296,3287,3277,3271,3272,3273,3274,3275,3276,3339,3342,3343,3376,3377,3371,3345,3346,3349,3352,3400,3427,3422,3395,3419,3421,3394,3392,3449,3470,3453,3454,3456,3458,3459,3460,3494,3495,3496,3497,3498,3529,3565,3564,3587,3596,3617,3647,3670,3684,3683,3646,3616,3615,3644,3636,3607,3562,3563,3528,3524,3503,3513,3555,3552,3579,3606,3635,3672,3695,3676,3678,3735,3722,3829,3945,3871,3916,3923,3878,3852,3841,3800,3807,3816,3887,3932,3962,3967,3973,3997,3998,3999,4000,4001,3938,3893,3855,3843,3755,3756,3757,3758,3712,3711,3648,3649,3566,3567,3530,3531,3532,3568,3588,3597,3650,3618,3598,3619,3685,3759,3760,3819,3818,3817,3857,3895,3856,3894,3939,4002,3940,3858,3896,3941,3964,3980,4004,4003,4050,4049,4048,4047,4046,4094,4093,4045,4092,4116,4138,4165,4182,4117,4139,4166,4219,4218,4217,4195,4234,4233,4232,4231,4194,4181,4164,4137,4115,4091,4044,4043,4042,4041,4040,4039,4031,4018,4007,4100,4105,4185,4183,4152,4125,4153,4126,4080,4081,4088,4130,4157,4114,4136,4163,4216,4215,4191,4187,4186,4201,4241,4245,4250,4295,4294,4318,4334,4358,4335,4359,4360,4336,4296,4254,4255,4299,4300,4321,4341,4340,4339,4364,4365,4366,4384,4367,4342,4322,4301,4256,4257,4258,4302,4259,4260,4261,4262,4263,4264,4265,4266,4267,4306,4327,4347,4372,4326,4346,4371,4370,4345,4325,4305,4304,4303,4324,4344,4369,4323,4343,4368,4392,4407,4391,4390,4388,4387,4386,4397,4385,4408,4373,4393,4409,4400,4375,4350,4330,4329,4349,4374,4348,4328,4309,4308,4307,4268,4269,4220,4221,4270,4271,4272,4273,4310,4274,4275,4276,4277,4278,4279,4280,4281,4282,4314,4313,4312,4311,4331,4351,4376,4377,4352,4378,4353,4354,4379,4394,4395,4380,4355,4332,4381,4396,4401,4402,4382,4357,4333,4356,4316,4285,4284,4283,4315,4317,4286,4287,4288,4289,4383,4290,4239,4238,4237,4236,4226,4225,4200,4199,4198,4197,4196,4224,4223,4235,4222,4167,4140,4118,4095,4060,4059,4058,4057,4056,4055,4054,4053,4052,4051,3944,3899,3898,3943,3942,3897,3859,3860,3861,3862,3900,3946,3863,3901,3947,3948,3902,3864,3865,3903,3949,3965,3950,3904,3951,3905,3982,3983,3992,3991,3981,4006,4005,4062,4061,4065,4066,4063,4064,4097,4096,4141,4168,4169,4119,4142,4120,4170,4143,4106,4107,4121,4171,4144,4172,4145,4098,4067,4068,4069,4099,4146,4173,4184,4174,4147,4122,4108,4101,4072,4071,4070,3984,3985,3955,3909,3867,3908,3954,3907,3953,3952,3906,3866,3830,3831,3832,3833,3784,3694,3696,3783,3782,3781,3780,3779,3778,3777,3776,3828,3827,3775,3774,3826,3825,3824,3773,3772,3771,3770,3769,3768,3767,3766,3823,3822,3821,3765,3764,3763,3762,3820,3761,3686,3651,3620,3621,3652,3671,3687,3713,3714,3715,3716,3717,3706,3719,3718,3688,3673,3655,3674,3690,3689,3656,3657,3691,3692,3693,3659,3660,3627,3626,3658,3625,3576,3577,3578,3580,3540,3539,3538,3575,3574,3573,3572,3537,3536,3535,3571,3591,3601,3624,3623,3654,3653,3622,3600,3590,3599,3589,3569,3533,3534,3570,3482,3483,3484,3435,3407,3385,3361,3360,3464,3463,3462,3434,3406,3359,3309,3310,3311,3312,3362,3313,3314,3315,3316,3317,3318,3319,3320,3321,3322,3323,3324,3325,3326,3327,3369,3368,3388,3414,3442,3450,3443,3415,3389,3370,3372,3380,3390,3416,3444,3451,3469,3501,3502,3500,3499,3441,3413,3387,3386,3412,3440,3468,3467,3466,3465,3436,3408,3409,3437,3438,3439,3411,3410,3363,3364,3365,3366,3367,3328,3259,2936,2906,2880,2937,2907,2881,2882,2908,2938,2951,2909,2939,2964,2988,2989,3047,3046,3045,3044,3043,3099,3123,3159,3160,3204,3258,3268,3248,3247,3203,3202,3158,3122,3157,3201,3121,3156,3200,3199,3155,3120,3119,3154,3198,3153,3197,3196,3245,3244,3243,3242,3241,3240,3191,3148,3192,3149,3150,3193,3194,3152,3151,3118,3088,3089,3090,3091,3092,3094,3095,3096,3097,3098,3042,3041,3040,3039,3038,3037,3036,3035,3034,3033,3032,3031,3030,3029,3028,3027,3026,3087,3086,3085,3025,2929,2900,2874,2901,2930,2931,2902,2932,2903,2877,2876,2875,2848,2809,2810,2811,2849,2812,2813,2814,2815,2850,2851,2852,2867,2878,2904,2933,2950,2983,2984,2985,2986,2987,2935,2934,2905,2879,2868,2853,2854,2817,2818,2855,2856,2857,2822,2821,2820,2819,2754,2752,2751,2733,2710,2709,2732,2750,2763,2762,2785,2816,2784,2783,2742,2729,2707,2689,2677,2688,2706,2728,2749,2727,2705,2687,2656,2620,2589,2590,2622,2621,2657,2658,2623,2624,2659,2625,2626,2627,2628,2660,2730,2731,2708,2690,2661,2662,2663,2664,2666,2634,2633,2632,2631,2630,2629,2602,2601,2575,2562,2523,2489,2472,2488,2522,2561,2487,2521,2560,2559,2486,2520,2485,2519,2558,2557,2518,2484,2483,2517,2556,2555,2516,2454,2455,2400,2401,2337,2336,2286,2253,2223,2192,2148,2149,2150,2151,2152,2153,2154,2155,2156,2157,2158,2195,2194,2193,2224,2254,2287,2289,2255,2225,2290,2256,2226,2211,2227,2257,2291,2303,2350,2351,2352,2353,2354,2412,2410,2409,2408,2407,2406,2405,2404,2403,2402,2456,2457,2458,2459,2460,2461,2413,2414,2462,2563,2524,2564,2565,2525,2491,2490,2463,2464,2420,2419,2418,2417,2416,2415,2338,2339,2355,2356,2330,2304,2295,2260,2230,2201,2162,2161,2199,2160,2159,2198,2229,2259,2294,2293,2292,2258,2228,2212,2197,2163,2095,1718,1719,1720,1721,1722,1723,1764,1765,1724,1725,1726,1727,1728,1729,1768,1730,1731,1732,1769,1790,1810,1837,1849,1789,1809,1836,1860,1886,1885,1876,1848,1835,1808,1788,1766,1787,1807,1834,1833,1806,1786,1785,1805,1831,1875,1874,1873,1872,1910,1911,1912,1913,1914,1915,1916,1964,1963,1962,1961,1960,1984,1983,2008,2039,2009,2040,2041,2010,1985,2011,2042,2044,2077,2078,2079,2081,2082,2108,2109,2110,2111,2092,2093,2094,2084,2083,2057,2048,2015,1987,1986,2014,2047,2056,2046,2013,2045,2012,1967,1965,1917,1918,1919,1968,1920,1921,1969,1970,1988,2016,2049,2050,2017,1971,1929,1928,1927,1926,1925,1924,1923,1922,1887,1888,1861,1862,1840,1841,1813,1792,1791,1812,1839,1838,1811,1770,1733,1771,1772,1773,1734,1735,1736,1686,1685,1671,1670,1660,1659,1641,1615,1640,1614,1590,1613,1589,1564,1563,1562,1586,1610,1611,1587,1588,1612,1639,1638,1637,1636,1669,1668,1658,1635,1609,1585,1561,1560,1525,1526,1527,1528,1529,1530,1531,1532,1533,1534,1535,1536,1565,1566,1567,1568,1616,1642,1661,1649,1643,1617,1591,1577,1571,1569,1545,1544,1543,1542,1541,1540,1539,1538,1537,1503,1502,1479,1478,1477,1476,1475,1445,1412,1444,1411,1363,1310,1311,1312,1364,1365,1413,1446,1447,1414,1366,1367,1313,1314,1315,1316,1368,1384,1393,1415,1448,1462,1494,1449,1416,1394,1417,1450,1480,1481,1482,1451,1418,1395,1396,1419,1452,1420,1453,1483,1485,1454,1422,1455,1421,1397,1377,1375,1374,1373,1372,1371,1370,1369,1317,1318,1319,1320,1321,1322,1323,1324,1325,1326,1327,1328,1236,1195,1157,1129,1073,1072,1071,1070,1069,1068,1126,1127,1156,1194,1235,1234,1193,1155,1154,1192,1233,1232,1191,1153,1125,1067,1066,1124,1065,1064,1123,1122,1121,1063,1062,1120,1119,1061,1060,1059,1058,1057,1056,1117,1116,1184,1225,1265,1266,1226,1185,1149,1118,1150,1186,1227,1187,1228,1244,1230,1189,1151,1139,1188,1229,1267,1268,1279,1280,1269,1231,1190,1152,1245,1074,1015,1007,1008,1009,1010,1011,992,993,994,1012,995,996,1014,978,969,968,935,936,911,912,937,970,971,972,938,913,860,859,858,896,894,902,893,892,934,967,966,933,965,963,932,889,890,851,850,849,848,847,846,845,844,787,788,763,732,707,733,764,765,734,708,735,766,789,779,767,736,709,697,768,737,710,698,711,738,769,739,770,740,771,791,790,809,808,807,806,805,891,852,853,854,855,856,857,810,772,741,712,691,654,773,742,713,655,598,597,596,595,653,652,690,689,651,650,649,688,648,687,686,647,646,685,684,683,682,642,643,644,645,590,591,592,593,594,548,565,564,563,562,530,498,499,531,532,500,533,501,478,467,468,454,453,452,451,450,423,424,425,377,378,379,380,381,382,346,322,323,347,348,349,350,351,386,387,431,430,461,459,429,428,427,426,455,456,457,458,505,539,538,504,503,536,479,502,535,537,566,567,568,569,570,540,506,541,507,469,480,508,542,549,550,543,509,481,470,462,463,352,335,334,326,327,304,286,278,268,267,266,303,302,325,324,301,265,264,263,231,230,229,228,227,226,170,171,172,173,124,95,62,42,3,43,44,45,46,63,47,48,49,50,51,4,52,53,78,106,126,125,176,158,157,156,175,174,233,234,235,236,269,270,328,305,287,237,161,160,159,144,127,79,54,55,5,6,112,98,90,89,97,111,131,109,108,130,147,148,244,245,184,185,249,186,187,250,281,291,311,310,290,280,274,243,242,241,240,239,273,272,271,238,162,163,146,129,128,107,56,57,58,81,82,83,84,59,60,8,66,9,10,11,67,91,99,113,114,100,92,69,68,12,14,15,16,17,70,71,19,1,72,101,115,133,138,139,197,256,255,254,195,194,193,192,191,190,188,251,252,253,283,294,314,313,293,282,292,312,339,315,295,296,316,340,341,399,398,436,435,433,466,474,486,514,515,516,584,583,582,581,580,605,604,603,602,545,511,483,472,464,546,512,484,473,465,388,384,308,288,331,354,353,329,306,307,330,471,482,510,544,599,600,601,658,694,657,656,693,714,743,774,775,744,715,695,659,660,661,662,607,608,609,610,664,699,718,747,776,745,716,696,663,700,719,748,777,780,749,720,701,750,721,702,668,667,665,611,612,613,614,615,616,669,670,703,723,752,722,751,782,820,821,822,907,922,948,947,921,906,872,873,819,818,817,816,815,814,813,812,869,870,905,920,946,904,919,945,944,918,903,868,867,866,865,900,901,916,942,977,915,941,976,975,940,974,997,973,939,914,897,898,899,864,863,862,861,1000,1030,1203,1202,1250,1249,1271,1240,1199,1161,1140,1134,1133,1132,1131,1159,1197,1160,1198,1239,1238,1237,1196,1158,1130,1075,1076,1077,1078,1079,1080,1081,1082,1083,1084,1085,1086,1024,1090,1025,1026,1027,1091,1093,1094,1095,1029,1096,1142,1165,1205,1291,1348,1430,1401,1386,1347,1346,1345,1344,1427,1459,1464,1466,1467,1428,1468,1469,1509,1507,1546,1506,1505,1549,1622,1596,1581,1574,1547,1463,1488,1487,1457,1424,1458,1425,1398,1385,1380,1381,1341,1342,1289,1288,1287,1340,1339,1338,1337,1336,1335,1334,1333,1332,1331,1330,1329,1378,1379,1423,1456,1486,1495,1496,1572,1579,1593,1619,1645,1573,1580,1594,1620,1646,1672,1673,1674,1675,1676,1663,1677,1664,1704,1703,1702,1701,1700,1698,1697,1749,1696,1695,1694,1748,1747,1746,1693,1692,1691,1690,1689,1688,1644,1578,1592,1618,1687,1738,1737,1775,1739,1740,1741,1742,1743,1744,1745,1776,1777,1778,1794,1844,1816,1793,1815,1843,1814,1842,1864,1889,1930,1931,1974,1932,1933,1934,1935,1936,1937,1938,1877,1865,1866,1878,1867,1868,1879,1869,1870,1895,1894,1893,1994,2023,2022,1993,1892,1942,1990,2019,2052,2059,2063,2102,2101,2099,2098,2097,2096,2086,2058,2051,2018,1989,1973,2089,2131,2208,2215,2209,2216,2236,2237,2267,2266,2235,2265,2311,2309,2297,2264,2234,2214,2233,2263,2308,2342,2343,2334,2335,2373,2375,2312,2313,2269,2239,2217,2170,2129,2128,2127,2126,2125,2124,2123,2122,2168,2121,2120,2167,2204,2203,2202,2331,2357,2358,2359,2360,2361,2332,2362,2363,2364,2365,2333,2341,2340,2430,2429,2428,2427,2426,2467,2425,2424,2423,2422,2421,2465,2466,2492,2526,2566,2567,2527,2493,2494,2528,2568,2591,2592,2533,2497,2473,2572,2571,2531,2530,2570,2569,2529,2495,2468,2469,2470,2431,2367,2368,2369,2370,2371,2372,2433,2432,2474,2498,2534,2573,2576,2594,2593,2597,2596,2642,2641,2640,2639,2638,2637,2668,2636,2635,2667,2691,2713,2736,2735,2712,2711,2734,2755,2756,2757,2738,2737,2714,2669,2670,2671,2604,2605,2643,2606,2607,2608,2609,2610,2475,2500,2536,2598,2611,2693,2761,2767,2760,2759,2766,2758,2765,2764,2829,2830,2831,2832,2787,2863,2834,2788,2789,2835,2836,2790,2791,2792,2793,2794,2795,2796,2798,2838,2870,2891,2918,2892,2919,2970,3000,3001,3002,3003,3005,3006,3132,3172,3255,3222,3170,3130,3113,3108,3063,2999,2998,3062,3060,2997,2996,2995,3059,3058,2994,3103,3054,3053,3052,3051,2972,2973,2974,2975,2968,2969,2955,2954,2953,2944,2915,2888,2889,2916,2917,2890,2869,2886,2913,2943,2885,2912,2942,2941,2911,2884,2860,2861,2862,2828,2827,2826,2825,2824,2823,2859,2883,2910,2940,2952,2966,2967,2991,2990,3048,3049,3050,3101,3102,3161,3205,3162,3206,3250,3251,3260,3269,3207,3163,3208,3252,3262,3263,3217,3210,3166,3126,3111,3104,3127,3167,3218,3219,3221,3169,3129,3112,3128,3168,3256,3288,3286,3285,3284,3283,3282,3281,3340,3280,3279,3278,3344,3375,3338,3337,3336,3335,3334,3333,3332,3331,3330,3329,3373,3374,3391,3417,3446,3445,3485,3486,3487,3488,3489,3471,3447,3418,3393,3420,3452,3472,3490,3473,3474,3491,3475,3476,3514,3512,3511,3510,3509,3508,3507,3550,3506,3505,3504,3551,3549,3548,3547,3546,3545,3544,3543,3542,3541,3581,3582,3583,3584,3585,3586,3605,3634,3667,3666,3633,3665,3632,3604,3631,3664,3699,3663,3630,3603,3629,3662,3602,3628,3661,3675,3697,3698,3721,3720,3785,3786,3787,3834,3835,3911,3868,3910,3956,3957,3986,3958,3912,3869,3913,3959,3914,3960,3987,3988,3993,3994,3961,3915,3870,3839,3838,3837,3836,3788,3789,3790,3791,3792,3793,3794,3795,3796,3723,3724,3725,3700,3701,3707,3702,3703,3708,3704,3705,3733,3734,3736,3737,3803,3802,3847,3879,3924,3922,3877,3876,3921,3920,3875,3846,3840,3801,3732,3731,3730,3729,3728,3727,3726,3799,3798,3797,3844,3872,3917,3918,3873,3845,3874,3919,3966,3989,3990,3968,3969,3970,4019,4017,4016,4015,4014,4013,4079,4012,4011,4010,4009,4008,4078,4077,4076,4075,4074,4073,4109,4123,4148,4175,4176,4240,4202,4203,4178,4150,4177,4149,4102,4103,4104,4124,4151,4179,4204,4205,4206,4227,4207,4208,4228,4209,4293,4244,4243,4242,4292,4291,4403,4410,4404,4405,4398,4246,4247,4248,4249,4399,4406,4361,4319,4251,4297,4320,4337,4362,4389,4363,4338,4298,4253,4252,4230,4229,4190,4192,4193,4162,4135,4161,4134,4113,4133,4160,4180,4159,4132,4112,4111,4131,4158,4189,4214,4213,4188,4212,4211,4210,4154,4127,4128,4155,4156,4129,4110,4083,4082,4020,4021,4022,4023,4024,4025,4026,4027,4028,4029,4084,4085,4030,4032,4033,4034,4035,4036,4086,4087,4089,4090,4038,4037,3996,3995,3976,3975,3974,3931,3886,3851,3885,3930,3929,3972,3971,3925,3880,3926,3881,3848,3882,3927,3928,3883,3849,3884,3850,3809,3810,3811,3842,3853,3933,3888,3812,3889,3934,3963,3935,3890,3854,3891,3936,3977,3978,3979,3937,3892,3813,3814,3815,3754,3753,3752,3751,3750,3749,3748,3747,3746,3745,3744,3743,3808,3806,3805,3804,3738,3739,3740,3741,3742,3709,3710,3679,3680,3681,3669,3682,3645,3527,3526,3561,3560,3525,3523,3522,3521,3520,3519,3556,3557,3558,3559,3595,3614,3643,3642,3613,3612,3641,3668,3640,3611,3594,3593,3610,3639,3677,3638,3609,3637,3608,3592,3553,3554,3518,3517,3516,3515,3477,3492,3478,3479,3493,3480,3481,3455,3424,3397,3398,3425,3457,3426,3399,3382,3381,3423,3396,3347,3348,3350,3351,3303,3302,3301,3300,3299,3298,3297,3295,3294,3293,3292,3291,3341,3290,3289,3304,3265,3224,3223,3173,3133,3114,3174,3134,3115,3135,3175,3136,3176,3177,3226,3264,3227,3257,3228,3229,3231,3232,3182,3181,3180,3139,3211,3178,3137,3116,3071,3015,3016,3072,3073,3075,3076,2980,2971,2959,2979,2978,3013,3070,3069,3068,3066,3065,3064,3007,3008,3009,3010,3011,3012,2976,2977,2958,2946,2924,2896,2872,2842,2802,2803,2747,2746,2745,2801,2841,2871,2894,2922,2945,2921,2840,2799,2772,2771,2770,2769,2768,2740,2717,2695,2679,2673,2645,2674,2680,2696,2718,2719,2697,2720,2721,2698,2681,2682,2699,2683,2700,2684,2649,2648,2647,2617,2616,2646,2615,2614,2613,2579,2540,2504,2541,2505,2479,2440,2478,2503,2539,2538,2502,2477,2537,2501,2476,2435,2376,2377,2378,2379,2436,2438,2380,2381,2439,2382,2383,2384,2385,2386,2441,2480,2506,2542,2508,2544,2545,2481,2442,2443,2392,2391,2390,2389,2388,2346,2347,2318,2317,2316,2345,2344,2299,2271,2270,2314,2298,2171,2132,2172,2218,2240,2241,2219,2242,2272,2300,2273,2243,2220,2221,2245,2275,2276,2277,2182,2181,2179,2178,2139,2177,2176,2175,2174,2133,2134,2135,2136,2137,2140,2091,2090,2054,2066,2067,2027,2028,1950,1949,1947,2026,1997,1945,1946,1900,1901,1871,1823,1851,1882,1898,1897,1850,1818,1796,1782,1797,1819,1820,1798,1783,1752,1751,1750,1705,1706,1707,1708,1709,1710,1821,1754,1711,1667,1679,1518,1516,1515,1514,1551,1582,1599,1624,1666,1678,1665,1598,1513,1512,1511,1510,1431,1402,1387,1432,1403,1388,1349,1292,1293,1294,1295,1296,1297,1351,1389,1404,1433,1390,1405,1434,1435,1471,1489,1438,1437,1354,1353,1352,1298,1299,1300,1302,1355,1357,1358,1276,1274,1254,1213,1253,1209,1208,1144,1167,1207,1206,1166,1143,1097,1031,1032,1033,1034,1098,1145,1168,1146,1169,1170,1210,1211,1171,1147,1104,1103,1102,1101,1100,1035,1036,1037,1038,1039,1040,1042,1043,1044,986,985,984,983,956,955,954,879,878,877,910,927,953,926,952,982,981,951,925,909,924,950,949,923,908,874,823,824,825,826,875,876,827,829,830,831,832,834,880,881,882,835,786,785,784,783,754,725,755,726,705,727,756,757,728,729,758,759,760,730,706,677,676,675,674,673,672,704,724,753,671,617,618,619,620,622,623,624,625,626,628,629,630,678,679,680,572,557,524,523,493,477,492,522,555,589,588,587,554,586,585,571,552,518,488,475,489,519,547,520,490,476,439,437,400,401,402,403,404,405,440,441,407,408,409,442,443,445,411,410,345,321,212,211,262,261,300,320,333,344,362,361,360,359,343,342,319,318,298,317,297,284,285,299,260,259,258,257,198,199,200,201,202,203,204,205,206,207,208,209,155,154,153,143,142,141,120,105,119,104,76,75,74,73,103,118,94,102,117,140,116,93,20,2,21,22,23,24,25,26,27,28,29,30,31,77,33,122,121,34]

    from pylab import *
    from matplotlib.pyplot import figure, plot
    figure()
    x= list(map(lambda x: data[x-1][1], best_path))
    y= list(map(lambda x: data[x - 1][2], best_path))
    plot(x, y, 'ro')
    plot(x, y)
    show()