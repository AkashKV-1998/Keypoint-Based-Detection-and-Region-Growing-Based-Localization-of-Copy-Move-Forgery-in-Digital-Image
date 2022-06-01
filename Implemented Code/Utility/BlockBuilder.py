from google.colab.patches import cv2_imshow
from tqdm import tqdm
import numpy as np
import cv2
from Distance import*
import os

class BlockBuilding():

    def __init__(self, image, KeypointClusters, BlockSize=3):
        self.image = image
        self.ImageSize = image.shape[0], image.shape[1]
        self.BlockSize = BlockSize
        self.KeypointClusters = KeypointClusters

    def CreateBlocks(self):

        img =self.image.copy()
        size=np.unique(self.KeypointClusters).shape[0]
        blocks  = [[] for i in range(size)]
        self.Img_clusters = [[] for i in range(size)]
        ignore_keypoints = 0

        for cluster in range(len(self.KeypointClusters)):
            for keypoint in self.KeypointClusters[cluster]:

                try:

                    x, y =  keypoint[0],  keypoint[1]
                    K_L, K_R, K_U, K_D = int(x)-self.BlockSize, int(x)+self.BlockSize, int(y)-self.BlockSize,int(y)+self.BlockSize

                    if (K_L < 0) or (K_R > int(self.ImageSize[0])) or (K_U < 0) or (K_D > int(self.ImageSize[1])):
                        pass
                    else:
                        regions = img[K_L:K_R, K_U:K_D]
                        blocks[cluster].append(regions)
                        self.Img_clusters[cluster].append(((K_L, K_R), (K_U, K_D)))
                
                except IndexError:

                     ignore_keypoints += 1
                     print(f"Keypoints removed during block construction: {ignore_keypoints}")


        return self.Img_clusters, blocks

    def visualize(self):

        print('\nDetected blocks after clustering. Each colour shows different clusters. \n\n')

        img = self.image.copy()

        for clusters in self.Img_clusters:
            colour = np.random.random_integers(50, 200, 3)
            for region in range(len(clusters)):
                a, b = clusters[region]
                x1, x2 = a
                y1, y2 = b

                cv2.rectangle(img, (x1, y1), (x2, y2), (int(colour[0]), int(colour[1]), int(colour[2])), 1)

        cv2.imwrite(f'{os.getcwd()}/Outputs/Keypoint_Clusters.jpg',img)

        cv2_imshow(img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return

## RegionGrowing:

class RegionGrowing():

    def __init__(self, image, ForgeryRegions, delta, BlockSize=3):

          self.copy_move_size = []
          self.Sr_blocks_chk = []
          self.Sr_blocks = []

          self.ForgeryRegions = ForgeryRegions
          self.BlockSize = BlockSize
          self.image = image
          self.threshold = delta

    def Grow(self, method, distribution=[]):

      if len(distribution) == 2:
          mean, variance = distribution[0], distribution[1]

      size = len(self.ForgeryRegions)
      img = self.image.copy()
      Distance = []

      for cluster_Pos in tqdm (range(size), desc="Cluster completed..."):
        for block in self.ForgeryRegions[cluster_Pos]:

          self.Sr_blocks_chk = []

          h_t, h_d =  block[1][0][0]
          w_l, w_r =  block[1][0][1] 
          
          self.Sr_blocks = [((h_t,h_d),(w_l,w_r))]

          m = [self.BlockSize, -(self.BlockSize)]
          (y, x, _) = self.image.shape

          while (len(self.Sr_blocks)) != 0: 

            h, w = self.Sr_blocks.pop()

            ## horizontal move:

            for n in range(0, 2):

                h_t = h[0]
                h_d = h[1]
                w_l = w[0]
                w_r = w[1]

                x1i = w_l
                x2i = w_r

                y1i = h_t+m[n]
                y2i = h_d+m[n]

                if (x1i <= x and x2i >= 0) and (x1i != x2i and y1i != y2i):

                    if ((y1i, y2i), (x1i,x2i)) not in self.Sr_blocks_chk:

                        im = img[y1i:y2i, x1i:x2i]
                        
                        h_t, h_d =  block[1][1][0]
                        w_l, w_r =  block[1][1][1] 
                        
                        x1j = w_l
                        x2j = w_r

                        y1j = h_t+m[n]
                        y2j = h_d+m[n]

                        if ((y1i, y2i), (x1i,x2i)) == ((y1j,y2j), (x1j,x2j)):pass
                        else:
                          im_j  = img[y1j: y2j, x1j: x2j]

                          if method == 'HuMoments':

                              diff = HuMoments(im, im_j)
                            
                              if diff < self.threshold:

                                self.copy_move_size.append(((y1i,y2i), (x1i,x2i)))
                                self.copy_move_size.append(((y1j,y2j), (x1j,x2j)))
                                self.Sr_blocks.append(((y1i,y2i), (x1i,x2i))) 

                                Distance.append([diff])
                          
                          elif method == 'SSIM':

                              diff = SSIM(im, im_j)

                              if diff >= self.threshold:

                                self.copy_move_size.append(((y1i,y2i), (x1i,x2i)))
                                self.copy_move_size.append(((y1j,y2j), (x1j,x2j)))
                                self.Sr_blocks.append(((y1i,y2i), (x1i,x2i))) 

                                Distance.append([diff])

                          elif method == 'Hu_Adapthreshold':
                              if len(variance)==7:cntlmt = 7
                              else: cntlmt = 1
                              count = 0

                              diff_Hu = Hu_Adapthreshold(im, im_j, cntlmt)
                              if cntlmt != 1:
                                for moment_index, Hus_moment in enumerate(diff_Hu):
                                  if (Hus_moment <= (mean[moment_index] + (3*variance[moment_index]))) and (Hus_moment >= (mean[moment_index] - (3*variance[moment_index]))):
                                    count+=1
                              else:
                                  if (diff_Hu <= (mean[0] + (3*variance[0]))) and (diff_Hu >= (mean[0] - (3*variance[0]))):
                                    count=1
                              if count == cntlmt:
                                self.copy_move_size.append(((y1i,y2i), (x1i,x2i)))
                                self.copy_move_size.append(((y1j,y2j), (x1j,x2j)))
                                self.Sr_blocks.append(((y1i,y2i), (x1i,x2i))) 

                self.Sr_blocks_chk.append(((y1i,y2i), (x1i,x2i))) 


            # vertical move:

            for n in range(0, 2):

              h_t = h[0]
              h_d = h[1]
              w_l = w[0]
              w_r = w[1]

              x1i = w_l+m[n]
              x2i = w_r+m[n]

              y1i = h_t
              y2i = h_d

              if (x1i <= x and x2i >= 0) and (x1i != x2i and y1i != y2i):

                  if ((y1i, y2i), (x1i,x2i)) not in self.Sr_blocks_chk:

                      im = img[y1i:y2i, x1i:x2i]
                      
                      h_t, h_d =  block[1][1][0]
                      w_l, w_r =  block[1][1][1] 
                      
                      x1j = w_l+m[n]
                      x2j = w_r+m[n]

                      y1j = h_t
                      y2j = h_d

                      if ((y1i, y2i), (x1i,x2i)) == ((y1j,y2j), (x1j,x2j)):pass
                      else:
                        im_j  = img[y1j: y2j, x1j: x2j]
                        
                        if method == 'HuMoments':

                            diff = HuMoments(im, im_j)
                          
                            if diff < self.threshold:

                              self.copy_move_size.append(((y1i,y2i), (x1i,x2i)))
                              self.copy_move_size.append(((y1j,y2j), (x1j,x2j)))
                              self.Sr_blocks.append(((y1i,y2i), (x1i,x2i))) 

                              Distance.append([diff])
                        
                        elif method == 'SSIM':

                            diff = SSIM(im, im_j)

                            if diff >= self.threshold:

                              self.copy_move_size.append(((y1i,y2i), (x1i,x2i)))
                              self.copy_move_size.append(((y1j,y2j), (x1j,x2j)))
                              self.Sr_blocks.append(((y1i,y2i), (x1i,x2i))) 

                              Distance.append([diff])

                        elif method == 'Hu_Adapthreshold':

                              if len(variance)==7:cntlmt = 7
                              else: cntlmt = 1
                              count = 0

                              diff_Hu = Hu_Adapthreshold(im, im_j, cntlmt)
                              if cntlmt != 1:
                                for moment_index, Hus_moment in enumerate(diff_Hu):
                                  if (Hus_moment <= ((3*variance[moment_index]) + mean[moment_index])) and (Hus_moment >= ((3*variance[moment_index]) - mean[moment_index])):
                                    count+=1
                              else:
                                  if (diff_Hu <= ((3*variance[0]) + mean[0])) and (diff_Hu >= ((3*variance[0]) - mean[0])):
                                    count=1
                              if count == cntlmt:
                                self.copy_move_size.append(((y1i,y2i), (x1i,x2i)))
                                self.copy_move_size.append(((y1j,y2j), (x1j,x2j)))
                                self.Sr_blocks.append(((y1i,y2i), (x1i,x2i))) 

              self.Sr_blocks_chk.append(((y1i,y2i), (x1i,x2i))) 

      return self.copy_move_size, Distance

    def ShowForgery(self):

      height, width, channels = self.image.shape
      binaryimage = np.zeros(shape=[height, width, 3], dtype=np.uint8)

      for i in range(len(self.copy_move_size)):

          a, b = self.copy_move_size[i]
          x1, x2 = a
          y1, y2 = b
          cv2.rectangle(self.image, (x1, y1), (x2, y2), (0, 0, 255), 1)
          cv2.rectangle(binaryimage, (x1, y1), (x2, y2), (255,255,255), -1)


      print("Number of blocks: ", len(self.copy_move_size))
      
      cv2.imwrite(f'{os.getcwd()}/Outputs/CMF_Result.jpg', self.image)   
      cv2.imwrite(f'{os.getcwd()}/Outputs/CMF_Binary_Result.jpg', binaryimage)         
      
      print('\nResult of CMF after applying region growing: \n')
      cv2_imshow(self.image)
      print('\nBinary result of CMF after applying region growing: \n')
      cv2_imshow(binaryimage)
      cv2.waitKey(0)
      cv2.destroyAllWindows()   

