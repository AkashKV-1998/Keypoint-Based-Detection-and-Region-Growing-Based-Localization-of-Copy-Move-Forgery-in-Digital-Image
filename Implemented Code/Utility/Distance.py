import cv2
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim

def HuMoments(RefImg, TestImg):

    RefImg   = cv2.cvtColor(RefImg, cv2.COLOR_BGR2GRAY )
    TestImg   = cv2.cvtColor(TestImg, cv2.COLOR_BGR2GRAY )

    distance = (cv2.matchShapes(RefImg, TestImg, cv2.CONTOURS_MATCH_I3,0))*(10**3)

    return distance

def SSIM(TestImg, RefImg):

  TestImg = cv2.cvtColor(TestImg, cv2.COLOR_BGR2GRAY)
  RefImg = cv2.cvtColor(RefImg, cv2.COLOR_BGR2GRAY)
  (score, diff) = compare_ssim(TestImg, RefImg, full=True)

  return score

def Hu_Adapthreshold(TestImg, RefImg, norm=1):

  TestImg   = cv2.cvtColor(TestImg, cv2.COLOR_BGR2GRAY )
  RefImg   = cv2.cvtColor(RefImg, cv2.COLOR_BGR2GRAY )

  moments_ref = cv2.moments(TestImg)
  moments_target = cv2.moments(RefImg)

  huMoments_ref = cv2.HuMoments(moments_ref)
  huMoments_target = cv2.HuMoments(moments_target)

  for i in range(0,7):
    huMoments_ref[i] = -1* np.copysign(1.0, huMoments_ref[i]) * np.log10(abs(huMoments_ref[i]))
    huMoments_target[i] = -1* np.copysign(1.0, huMoments_target[i]) * np.log10(abs(huMoments_target[i]))

  if norm == 1:
    Moments_distance = np.linalg.norm(huMoments_ref - huMoments_target)
  else:  Moments_distance = huMoments_ref - huMoments_target

  return Moments_distance


