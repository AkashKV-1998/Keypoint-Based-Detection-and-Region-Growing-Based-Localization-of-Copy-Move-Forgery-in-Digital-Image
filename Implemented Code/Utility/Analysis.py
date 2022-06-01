import matplotlib.pyplot as plt

def map_truths(data, dataset):

    if dataset == 'CoMoFoD':
        truths = []
        for img in data.File_Name:
            if 'O' in img:
                truths.append('Original')
            else:
                truths.append('Forgery')

        return truths

    elif dataset == 'MICC_F2000':

        truths = []
        for img in data.File_Name:
            if 'tamp' in img:
                truths.append('Forgery')
            else:
                truths.append('Original')

        return truths

    elif dataset == 'Christlein':

        truths = []
        for img in data.File_Name:
            if 'copy' in img:
                truths.append('Forgery')
            else:
                truths.append('Original')


        return truths


def analysis(data, dataset):

    data['Truths'] = map_truths(data, dataset)

    count_N  = 0
    count_Y  = 0
    count_TP = 0
    count_FP = 0
    count_TN = 0
    count_FN = 0

    results = data.Result
    truths = data.Truths

    for i in range(len(results)):
        if len(results) == len(truths):

            if results[i] == 'N':
                count_N += 1

                if truths[i] == 'Forgery':
                    count_FN += 1
                else:
                    count_TN += 1

            elif results[i] == 'Y':
                count_Y += 1

                if truths[i] == 'Forgery':
                    count_TP += 1
                else:
                    count_FP += 1
        else:

            print('Length error!')
            break


    return count_N, count_Y, count_TP, count_FP, count_TN, count_FN


def info(data, dataset):

    N, Y, TP, FP, TN, FN = analysis(data, dataset)

    print("\n\t\t\t Analysis Summary")

    print('\nTotal images tested: ', len(data))
    print('\nTrue Positives: ', TP)
    print('False Positives: ',FP)
    print('True Negatives: ', TN)
    print('False Negatives: ', FN)

    print(f'\nAccuracy of results: {((TP + TN) / (TP + TN + FP + FN))}')
    print(f'True Positive Rate(TPR): {(TP / (TP + FN + 0.001))}')
    print(f'False Positive Rate(FPR): {(FP / (FP + TN + 0.001))}')
    print(f'False Negative Rate(FNR): {(FN / (FN + TP + 0.001))}')

    print(f'Recall: {(TP / (TP + FN + 0.001))}')
    print(f'Precision: {(TP / (TP + FP + 0.001))}')


    labels = 'TP', 'FP', 'TN', 'FN'
    sizes = [TP, FP, TN, FN]
    explode = (0,0,0,0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    fig1, ax1 = plt.subplots(figsize =(10, 7),)
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=30)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Plot showing confusion matrix Phi Chart \n\n")
    print('\n\n')

    plt.show()




