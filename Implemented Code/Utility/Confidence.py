import math
import numpy as np
from statsmodels.stats.proportion import proportion_confint

def round_up(n, decimals = 0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def Confidence_Intervel(Total_blocks):

    Proportion_list = []
    size = len(Total_blocks)

    if len(Total_blocks) == 0:
        Total_blocks.append([0])

    max_threshold= np.max(Total_blocks)
    loop_threshold = round_up(max_threshold, 1)
    block_confidence = 0

    for i in np.arange(0, loop_threshold, 0.1):
        low_limit = round(i, 2)
        up_limit  = 0.09
        # print(round(i, 2))
        block_counts = 0
        for threshold in Total_blocks:
            if threshold > low_limit and threshold < (low_limit+up_limit):
                block_counts += 1
            else: pass

        Proportion_list.append([block_counts, low_limit])

    Proportion_list = [i for i in Proportion_list if i[0] != 0]

    for Proportion in Proportion_list:
        if Proportion[1] == 0:
            block_confidence += Proportion[0]
        else:
            temp_confidence = Proportion[0] - (np.exp(Proportion[1]*10))
            if temp_confidence > 0:
                block_confidence += temp_confidence

    lower_bound, upper_bound = proportion_confint(int(block_confidence), len(Total_blocks), 0.05)

    if size>0:
        print('\nResult: Forgery detected in given image')
        print('\nConfidence of CMF localization: \n')
        print('Lower Bound: %.3f \nUpper Bound: %.3f' % (lower_bound*100, upper_bound*100))
    else:
        print('\nResult: No forgery regions detected')
        print('\nConfidence of CMF localization: \n')
        print('Lower Bound: %.3f \nUpper Bound: %.3f' % (100, 100))
        print('______' *15)

    return lower_bound, upper_bound