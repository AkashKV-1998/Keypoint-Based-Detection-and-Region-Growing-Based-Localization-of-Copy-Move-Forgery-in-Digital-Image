import imutils
from imutils import contours
from skimage import measure
import cv2
from google.colab.patches import cv2_imshow
import numpy as np
from Distance import HuMoments


def Region_Distance(img, path, delta=5):

    image = img.copy()
    detected_rgns = cv2.imread(path)
    detected_rgns = cv2.cvtColor(detected_rgns, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(detected_rgns, (5, 5), 0)
    thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=4)

    labels = measure.label(thresh, background=0)
    mask = np.zeros(thresh.shape, dtype="uint8")
    # loop over the unique components
    for label in np.unique(labels):
        # if this is the background label, ignore it
        if label == 0:
            continue
        # otherwise, construct the label mask and count the
        # number of pixels
        labelMask = np.zeros(thresh.shape, dtype="uint8")
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero(labelMask)
        # if the number of pixels in the component is sufficiently
        # large, then add it to our mask of "large blobs"
        if numPixels > 300:
            mask = cv2.add(mask, labelMask)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) != 0:
        cnts = contours.sort_contours(cnts)[0]
    # loop over the contours

    forgery_area = []
    for (i, c) in enumerate(cnts):
        # draw the bright spot on the image
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
        location = image[y:y+h, x:x+w]
        forgery_area.append(location)

    # show the output image
    print('\nDetected forgery regions after Hus distance calculation: \n')
    cv2_imshow(image)

    total_final_block = 0
    for f1_index, f1 in enumerate(forgery_area):
        for f2_index, f2 in enumerate(forgery_area):
            if f1_index != f2_index:
                diff = HuMoments(f1, f2)

                if diff < delta:
                    total_final_block+=1

    if total_final_block != 0:
        Forgery = 'Y'
    else:
        Forgery = 'N'

    return Forgery