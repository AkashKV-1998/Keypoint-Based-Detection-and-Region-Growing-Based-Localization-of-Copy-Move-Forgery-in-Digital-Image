import sys
import cv2
from google.colab.patches import cv2_imshow
from sklearn.cluster import DBSCAN, KMeans
import numpy as np

class KeypointCluster(object):

    def __init__(self, image):
        self.image = image

    def siftDetector(self):

        sift = cv2.xfeatures2d.SIFT_create()
        gray= cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        self.key_points,self.descriptors = sift.detectAndCompute(gray, None)

        print(f'Length of Keypoints from SIFT feature extractor: {len(self.key_points)} and length of descriptors {len(self.descriptors)}')

        return self.key_points,self.descriptors

    def showSiftFeatures(self):

        gray_image=cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        sift_image=cv2.drawKeypoints(self.image,self.key_points,self.image.copy())

        return sift_image

    def DBSCANLocateForgery(self, eps, min_sample):

        clusters=DBSCAN(eps=eps, min_samples=min_sample).fit(self.descriptors)
        size=np.unique(clusters.labels_).shape[0]-1
        clustered_image=self.image.copy()

        if (size==0) and (np.unique(clusters.labels_)[0]==-1):

            print('No Forgery Found in DB-SCAN Clustering!!')

            return

        if size==0:
            size=1
        cluster_list= [[] for i in range(size)]

        for idx in range(len(self.key_points)):
            if clusters.labels_[idx]!=-1:
                cluster_list[clusters.labels_[idx]].append((int(self.key_points[idx].pt[0]),int(self.key_points[idx].pt[1])))

        return cluster_list

    def KMeansLocateForgery(self, n_clusters):

        clusters = KMeans(n_clusters).fit(self.descriptors)
        size=np.unique(clusters.labels_).shape[0]

        if (size==0) and (np.unique(clusters.labels_)[0]==-1):
            print('No Forgery Found in DB-SCAN Clustering!!')
            return

        clustered_image=self.image.copy()

        if size==0:
            size=1

        cluster_list= [[] for i in range(size)]

        for idx in range(len(self.key_points)):
            cluster_list[clusters.labels_[idx]].append((int(self.key_points[idx].pt[0]),int(self.key_points[idx].pt[1])))


        return cluster_list