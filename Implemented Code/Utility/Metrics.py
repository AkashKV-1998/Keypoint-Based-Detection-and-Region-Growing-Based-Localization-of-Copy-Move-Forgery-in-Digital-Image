import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import cv2
from matplotlib.pyplot import imshow
from prettytable import PrettyTable

def GenerateCM(CodeOut, RealBinary, addon=[]):

    prediction_mask = cv2.imread(CodeOut)
    mask =  cv2.imread(RealBinary)

    prediction_mask = cv2.resize(prediction_mask, (300, 300))
    mask = cv2.resize(mask, (300, 300))

    mask = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
    prediction_mask = cv2.cvtColor(prediction_mask, cv2.COLOR_RGB2GRAY)


    prediction_mask = np.array(prediction_mask)
    mask = np.array(mask)

    forgery = "N"

    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for i in range(0, prediction_mask.shape[0]):
        for j in range(0, prediction_mask.shape[1]):
            if prediction_mask[i][j] == mask[i][j]:
                if prediction_mask[i][j] == 255:
                    forgery = "Y"
                    TP += 1
                else:
                    TN += 1
            else:
                if prediction_mask[i][j] == 255:
                    forgery = "Y"
                    FP += 1
                else:
                    FN += 1

    if forgery == 'Y':
        print('\n')
        if 'precision' in addon:
            precision = TP/(TP+FP)
            print('Precision: ', precision)
        if 'recall' in addon:
            recall = TP/(TP+FN)
            print('Recall: ', recall)
        if 'accuracy' in addon:
            accuracy = (TP+TN)/(TP+FP+TN+FN)
            print('Accuracy: ', accuracy)
        if 'TPR' in addon:
            TPR = TP/(TP+FN)
            print('True Positive Rate(TPR): ', TPR)
        if 'FPR' in addon:
            FPR = FP/(FP+TN)
            print('False Positive Rate(TPR): ', FPR)
        if 'F1' in addon:
            recall = TP/(TP+FN)
            precision = TP/(TP+FP)
            F1_score = (2*precision*recall)/(precision+recall)
            print('F1 Score: ', F1_score)
    else:
        precision = 0
        recall = 0
        accuracy = 0
        TPR = 0
        FPR = 0
        F1_score = 0

    # print(TP, FP, '\n', FN, TN)
    print("\nConfusion metric: \n")

    ConfusionMetric = PrettyTable(["","Actual_CMF_Regions", "False_CMF_Regions"])
    ConfusionMetric.add_row(["Actual_CMF_Regions", str(TP), str(FP)])
    ConfusionMetric.add_row(["False_CMF_Regions", str(FN), str(TN)]) 
    print(ConfusionMetric)

    plt.figure(figsize=(40, 40))
    f, axarr = plt.subplots(1,2)
    print('\n\nComparison between orginal and predicted binary image: \n')
    axarr[0].imshow(mask)
    axarr[1].imshow(prediction_mask)
    