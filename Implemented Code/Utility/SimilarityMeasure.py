import cv2
import numpy as np
from operator import itemgetter
from google.colab.patches import cv2_imshow
from Distance import*
import os

class DistanceCalculation():
    def __init__(self, image, blocks, positions, delta=None, gamma=None):
        self.image = image
        self.blocks = blocks
        self.positions = positions
        self.DistanceThreshold = delta
        self.SortThreshold = gamma
        print(f'\nDelta (minimum distance between pair of blocks) set to : {self.DistanceThreshold}')
        print(f'Gamma (Sort and take minimum distance ranging from 0 to gamma in every cluster) set to : {self.SortThreshold}')


    def Calculate(self, method, distribution=[]):

        if len(distribution) == 2:
          mean, variance = distribution[0], distribution[1]

        size = len(self.blocks)
        ForgeryRegions = [[] for i in range(size)]

        for cluster_Pos in range(size):
            for RefIndex, RefImg in enumerate(self.blocks[cluster_Pos]):
                for TestIndex, TestImg in enumerate(self.blocks[cluster_Pos]):
                    if (RefIndex == TestIndex) or ((self.positions[cluster_Pos][RefIndex]) == (self.positions[cluster_Pos][TestIndex])):pass
                    else:
                        if method == "HuMoments":
                            distance = HuMoments(RefImg, TestImg)

                            if self.DistanceThreshold != None:
                              if distance <  self.DistanceThreshold: ForgeryRegions[cluster_Pos].append([distance, (self.positions[cluster_Pos][RefIndex], self.positions[cluster_Pos][TestIndex])])
                            else: ForgeryRegions[cluster_Pos].append([distance, np.array([self.positions[cluster_Pos][RefIndex], self.positions[cluster_Pos][TestIndex]])])
                        
                        elif method == "SSIM":
                            distance = SSIM(RefImg, TestImg)
                            if self.DistanceThreshold != None:
                              if distance >=  self.DistanceThreshold: 
                                ForgeryRegions[cluster_Pos].append([distance, (self.positions[cluster_Pos][RefIndex], self.positions[cluster_Pos][TestIndex])])
                            else: ForgeryRegions[cluster_Pos].append([distance, np.array([self.positions[cluster_Pos][RefIndex], self.positions[cluster_Pos][TestIndex]])])

                        elif method == "Hu_Adapthreshold":
                            if len(variance)==7:cntlmt = 7
                            else: cntlmt = 1
                            count = 0
                            diff_Hu = Hu_Adapthreshold(RefImg, TestImg, cntlmt)

                            if cntlmt != 1:
                              for moment_index, Hus_moment in enumerate(diff_Hu):
                                if (Hus_moment <= (mean[moment_index] + (3*variance[moment_index]))) and (Hus_moment >= (mean[moment_index] - (3*variance[moment_index]))):
                                  count+=1
                            else:
                              if (diff_Hu <= (mean[0] + (3*variance[0]))) and (diff_Hu >= (mean[0] - (3*variance[0]))):
                                count=1
                            if count == cntlmt:
                              ForgeryRegions[cluster_Pos].append(['NA', np.array([self.positions[cluster_Pos][RefIndex], self.positions[cluster_Pos][TestIndex]])])
                            
                        
                        # if self.DistanceThreshold != None:
                        #     if distance <  self.DistanceThreshold: ForgeryRegions[cluster_Pos].append([distance, (self.positions[cluster_Pos][RefIndex], self.positions[cluster_Pos][TestIndex])])
                        # else: ForgeryRegions[cluster_Pos].append([distance, np.array([self.positions[cluster_Pos][RefIndex], self.positions[cluster_Pos][TestIndex]])])

        if  self.SortThreshold != None:
            Clusterlist = []
            for Cluster_Pos, ClusterRegions in enumerate(ForgeryRegions):
                ClusterRegions = sorted(ClusterRegions, key = itemgetter(0))
                ClusterRegions = ClusterRegions[: self.SortThreshold]
                Clusterlist.append(ClusterRegions)

            ForgeryRegions = Clusterlist.copy()
        else:pass


        height, width, channels = self.image.shape
        binaryimage = np.zeros(shape=[height, width, 3], dtype=np.uint8)
        for regions in ForgeryRegions:

            colour = np.random.random_integers(50, 200, 3)

            for R in range(len(regions)):
                for i in range(0, 2):
                    a, b = regions[R][1][i]
                    x1, x2 = a
                    y1, y2 = b

                    cv2.rectangle(self.image, (x1, y1), (x2, y2), (int(colour[0]), int(colour[1]), int(colour[2])), 1)
                    cv2.rectangle(binaryimage, (x1, y1), (x2, y2), (255,255,255), -1)
        
        cv2.imwrite(f'{os.getcwd()}/Outputs/{method}_initial_blocks.jpg',self.image)
        cv2.imwrite(f'{os.getcwd()}/Outputs/{method}_initial_blocks_Bny.jpg', binaryimage)

        print(f'\nDetected regions after {method} similarity test: \n\n')
        cv2_imshow(self.image)
        # cv2_imshow(binaryimage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return ForgeryRegions