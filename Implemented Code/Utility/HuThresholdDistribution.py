import cv2
from Distance import HuMoments
import matplotlib.pyplot as plt
from google.colab.patches import cv2_imshow
import numpy as np
import pandas as pd
import tqdm
import os

def start_points(size, split_size, overlap=0):
    points = [0]
    stride = int(split_size * (1-overlap))
    counter = 1
    while True:
        pt = stride * counter
        if pt + split_size >= size:
            points.append(size - split_size)
            break
        else:
            points.append(pt)
        counter += 1
    return points

def groundtruth_mapper(path_to_binary, path_to_forgery):

    count = 0
    name = 'splitted'
    frmt = 'jpeg'
    get_blocks = []

    binary_img = cv2.imread(path_to_binary)
    forgery_img = cv2.imread(path_to_forgery)

    input_size = (512, 512)

    binary_img = cv2.resize(binary_img, input_size)
    forgery_img = cv2.resize(forgery_img, input_size)

    img_h, img_w, _ = forgery_img.shape
    split_width = 10
    split_height = 10

    X_points = start_points(img_w, split_width, 0.5)
    Y_points = start_points(img_h, split_height, 0.5)

    for i in Y_points:
        for j in X_points:
            split_area = i, i+split_height, j, j+split_width
            get_blocks.append(split_area)
            count += 1

    truth_regions = []

    for region in get_blocks:
        x, y, w, h = region
        location = binary_img[w: h, x: y]

        if np.mean(location) == 255:
            truth_regions.append([x, y, w, h])

    # height, width, channels = forgery_img.shape
    # binaryimage = np.zeros(shape=[height, width, 3], dtype=np.uint8)

    # loc_forgery = forgery_img.copy()
    # for i in range(len(truth_regions)):

    #     x1, x2, y1, y2 = truth_regions[i]

    #     cv2.rectangle(loc_forgery, (x1, y1), (x2, y2), (0, 0, 255), 1)
    #     cv2.rectangle(binaryimage, (x1, y1), (x2, y2), (255,255,255), -1)

    # print("Number of blocks: ", len(truth_regions))

    # cv2_imshow(loc_forgery)
    # cv2_imshow(binaryimage)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return truth_regions

def Get_imgs_HuMoments(truth_regions, path_to_forgery):

    forgery_img = cv2.imread(path_to_forgery)

    input_size = (512, 512)

    forgery_img = cv2.resize(forgery_img, input_size)

    set_distance_limit = 2
    # temp_region = []
    min_distance = []
    Hu_moments = []

    for index_ref, region_ref in enumerate(truth_regions):
        xi1, xi2, yi1, yi2 = region_ref
        img_1 = forgery_img[yi1:yi2, xi1:xi2]
        previous_val = np.inf
        flag = False

        for index_target, region_target in enumerate(truth_regions):
            if index_ref != index_target:
                xj1, xj2, yj1, yj2 = region_target
                img_2 = forgery_img[yj1:yj2, xj1:xj2]
                distance = HuMoments(img_1, img_2)

                if distance < previous_val:
                  if distance < set_distance_limit:
                    # temp_region = [region_ref, region_target]
                    previous_val = distance

                    img_ref   = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY )
                    img_target   = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY )

                    flag =True

        if flag == True:

          moments_ref = cv2.moments(img_ref)
          moments_target = cv2.moments(img_target)

          huMoments_ref = cv2.HuMoments(moments_ref)
          huMoments_target = cv2.HuMoments(moments_target)

          for i in range(0,7):
              huMoments_ref[i] = -1* np.copysign(1.0, huMoments_ref[i]) * np.log10(abs(huMoments_ref[i]))
              huMoments_target[i] = -1* np.copysign(1.0, huMoments_target[i]) * np.log10(abs(huMoments_target[i]))

          Moments_distance = huMoments_ref - huMoments_target

          # min_distance.append(temp_region)
          Hu_moments.append(Moments_distance)

    return Hu_moments

def Get_Hu_distributions(samples_path, data_dir, norm=True):

    try:
      samples = pd.read_csv(samples_path)
    except:
      print('Samples file not found...')

    Hu_Mean_Var = []
    Collect_mean = []
    Collect_var = []
    Hu_temp_list = [[] for i in range(0, 7)]

    for name in tqdm.tqdm(samples['0'], desc="Loading..."):

        path_to_binary = data_dir + "/" + (name[:4]+ str('B.png'))
        path_to_forgery =  data_dir + "//" + name

        truth_regions = groundtruth_mapper(path_to_binary, path_to_forgery)
        Hu_moments = Get_imgs_HuMoments(truth_regions, path_to_forgery)


        for i in range(0, 7):
          for moments in Hu_moments:
              moment_value = moments[i]
              Hu_temp_list[i].append(moment_value)

    temp_list = []
    for i in range(len(Hu_temp_list)):
        moment_value = Hu_temp_list[i]
        temp_list.append(moment_value)

        moments_mean = np.mean(temp_list)
        moments_variance = np.std(temp_list)

        print(f'\nHu\'s Moment: {i} \n')
        plt.figure(figsize=(20,10))
        plt.hist(moment_value, bins=10)
        plt.show()

        Collect_mean.append(moments_mean)
        Collect_var.append(moments_variance)

    if norm == True:
      mean_norm = np.linalg.norm(Collect_mean)
      var_norm = np.linalg.norm(Collect_var)

      Collect_mean, Collect_var = [], []
      Collect_mean.append(mean_norm)
      Collect_var.append(var_norm)
      file_name = 'Distribution_Norm_True.npy'
    elif norm == False:
      file_name = 'Distribution.npy'
    else:
      print('Invalid norm given. norm=True uses np.linalg.norm over mean and veriance, else use norm=False')

    save_file = f'{os.getcwd()}/Outputs/{file_name}'
    np.save(save_file, (Collect_mean, Collect_var), allow_pickle=True)

    print('Distribution file is saved to Output directory')