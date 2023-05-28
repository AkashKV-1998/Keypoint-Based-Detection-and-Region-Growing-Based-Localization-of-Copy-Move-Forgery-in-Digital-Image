# Keypoint-Based Detection and Region Growing-Based Localization of Copy-Move Forgery in Digital Images
<br/>

<a href="https://colab.research.google.com/github/AkashKV-1998/Detection-and-localization-of-CMFD/blob/main/Implemented%20Code/CMFD_Implementated_Code.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

<a href="[https://colab.research.google.com/github/AkashKV-1998/Detection-and-localization-of-CMFD/blob/main/Implemented%20Code/CMFD_Implementated_Code.ipynb](https://link.springer.com/chapter/10.1007/978-981-19-7867-8_41)" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open Published paper"/></a>

Author details: 
<br/>

Author      : Akash Kalluvilayil Venugopalan<sup>1
<br/>
Email🆔    : amenp2ari20001@am.students.amrita.edu 
<br/>
University  : Amrita College of Engineering, Kollam, Kerala, India
    
Author      : Prof. Gopakumar G<sup>2
<br/>
Email🆔    : gopakumarg@am.amrita.edu
<br/>
University  : Amrita College of Engineering, Kollam, Kerala, India

<br/>

📄Paper Link: [Link](https://doi.org/10.1007/978-981-19-7867-8_41)

**This repository contains analysis and results of different copy-move forgery detection approaches.
    
## A Brief Introduction to Copy-Move Forgery
    
### Abstract
    
Image manipulation is a common issue that we can see in social media, news, and many other places. Sometimes it is very difficult to understand these manipulations with our naked eye. Technology is advancing day by day. As the result, image manipulation tools are getting developed to such a level that a normal person with naked eye cannot figure out forgery regions in an image. Some of the common tools that are used to manipulate images are Adobe Photoshop, GIMP, Corel Paint Shop, etc. Image manipulation can create many issues in different field including forensics and fake news creation. There are different types of image manipulations that can be performed in an image. They are retouching, morphing, splicing and copy-move. In this project, we will explore different copy-move forgery detection techniques on available datasets to incorporate novel ideas for improving detection and localization accuracy.
    
### Background
    
Manipulating images or making minor changes to the original image to make them visually attractive is very common nowadays. There are many applications used for image manipulations and these applications provide an easy environment for the user to make changes to the original/authentic image. Therefore, image tampering is very popular and can be done easily. The image manipulations are either done to make the picture more attractive to the audience or to hide some content in the original image. Some common image tampering methods are retouching, morphing, splicing, and copy-move. A figure explaining the image manipulations is given below (Figure: 1) . In figure 1 (a), the bird is copy-moved to create a forged image while in (b) two images are used to create a spliced image. In (c) retouching is used to alter the source image and a morphing example can be
seen in (d). When the original images undergo any of this tampering, then it will be difficult to identify the source image (original image) and tampered images separately. This caused several difficulties in the field of forensic and news broadcasting. We know that it is necessary to prove the authenticity of an image before submitting it to the court. If the tampered image is given to the court for a particular case, then the court may end up in a false conclusion about the case. Therefore, it is relevant for the forensic department to prove whether the particular image has undergone any tampering or not. Many studies are focused on identifying the authenticity of an image by the use of computer vision and machine learning tools. But most of the proposed approaches have less accuracy on detection and localization of tampered regions in an image.
    
 
<br/>
    
![](https://github.com/AkashKV-1998/Detection-and-Localization-of-Copy-Move-Image-Forgery-using-Deep-Learning-Networks/blob/main/Image%20Files%20md/Img_man.png) 
    
### Challenges in Detecting Copy-move forgery

Detecting image manipulations can be classified as active and passive approaches. The active approach requires pre-processing on the image such as adding signature or watermark to the image and is often done during image creation. Here, if the signature or the watermark extracted from the forgery image matches the original image, then we can conclude that the image is forged. The passive approach or blind approach is more difficult when we compare it with the active approach as we don’t consider any signature or watermark in the image. The passive approaches includes pixel-based techniques, format-based techniques, camera-based techniques etc. And these approaches are generally used to detect copy-move forgery, splice forgery, and morphing. Copy-move forgery detection is one of the challenging tasks to detect because the copied source is placed in the same image and hence it will not alter the overall image characteristics. The copied or forged regions may undergo some transformations such as scaling, translation, rotation, and flip. These transformations make it more difficult to identify the copy-move forgery regions in a tampered image. Suppose, if the forged region is made thin or scaled-down than the actual region in the source image, then detecting it with the help of a computer vision tool may not work that efficiently. There are many traditional computer vision and machine learning approaches proposed for detecting and localizing copy-move forgery regions in an image but most of the approaches are not robust to many of the image transformations. This repository contains results of different copy-move forgery detection approaches.


     
## Repository Structure:
<br/>

    1. Implemented Code ___________                                                                               : PROPOSED ALGORITHM THAT MAKE USE OF SIFT AND DBSCAN
                                    |
                                    |
                      Proposed approach for CMFD

    2. Results and Analysis __________________________________________________                                    : THE DIRECTORY CONTAINS OUR ANALYSIS AND RESULTS
                                 |                                            |
                                 |                                            |
                    CoMoFoD_SD_Analysis with codes              MICC_F2000_Analysis with codes                    : DATASET USED FOR TESTING
                                 |                                            |
                      ___________|___________                                 |
                     |                       |                                |
                 Detection             Localization                       Detection                               : ANALYSIS THAT WE DONE ON CODE
                     |                       |                                |
                     |                       |                                |
                 ____|___                ____|_____                       ____|____                               : TESTED CODES
                |    |   |              |     |    |                     |    |    |
             DBSCAN  |   |            DBSCAN  |    |                   DBSCAN |    |
                   DCT   |                   DCT   |                         DCT   |
                      FACMARD                   FACMARD                         FACMARD


    3. Reference code____                                                                                         : CODE THAT WE HAVE IMPLEMENTED FROM OTHER PAPERS
                         |
                         |
         Code of Rotational copy-move forgery 
         detection using SIFT and region 
         growing strategies
         
         
    4. Other Docs                                                                                                 : OTHER IMPORTANT DOCUMENTS
    
    5. Other References Paper Bib file                                                                            : OUR MAIN REFERENCES
    
  
    

 <br/>

## Results and Analysis 
    
Currently, we have tested 3 codes with [CoMoFoD small dataset](https://www.vcl.fer.hr/comofod/download.html) and [MICC-F2000](http://lci.micc.unifi.it/labd/2015/01/copy-move-forgery-detection-and-localization/) dataset for detection and localization confusion matrix. For testing each code, 200 image samples are taken from random uniform distribution from the dataset. The tested codes are:

1. DBSCAN-Based Copy-Move forgery detection 

    Article : [Link](https://medium.com/analytics-vidhya/copy-move-forgery-detection-using-sift-and-dbscan-clustering-4a179c36293e)
    
    Code    : [Link](https://github.com/Himj266/DBSCAN-Copy-Move-Foregry-Detection)
    
2. DCT-Based Copy-Move forgery detection
        
    Code    : [Link](https://github.com/alperencubuk/Copy-Move-Forgery-Detection)
    
3. Forensic Analysis of Copy-Move Attack with Robust Duplication Detection(FACMARD)
    
    Paper   : [Link](https://link.springer.com/chapter/10.1007%2F978-3-030-73689-7_39)
    
    Code    : [Link](https://github.com/rahmatnazali/image-copy-move-detection)

## Reference Paper Implementation 
    
The code of the paper 'Rotational copy-move forgery detection using SIFT and region growing strategies' ([Paper Link](https://link.springer.com/article/10.1007/s11042-019-7165-8)) we have implemented and uploaded in the directory '[Reference Code](https://github.com/AkashKV-1998/Detection-and-Localization-of-Copy-Move-Image-Forgery-using-Deep-Learning-Networks/tree/main/Reference%20Code/Code%20of%20Rotational%20copy-move%20forgery%20detection%20using%20SIFT%20and%20region%20growing%20strategies)'. But the code shows few error and localization is not accurate. The error is possibly on Hu moment calculations. If you want to reuse the code, we suggest kindly try to correct the errors in the code for better results.
    
<br/>
    
<em> Install all dependencies before running the codes: </em>

Packages used:

1. opencv-python==4.0.1.24
2. numpy==1.19.2
3. tqdm==4.61.2
4. matplotlib==3.3.4
5. psutil==5.8.0
    
            pip install -r requirements.txt

## Other Reference 
    
 The directory '[Other Reference](https://github.com/AkashKV-1998/Detection-and-Localization-of-Copy-Move-Image-Forgery-using-Deep-Learning-Networks/tree/main/Other%20References%20Paper%20Bib%20file)' contains our entire references in a bibtex file and also in HTML file for your reference.
    
For more details, please go through the [paper](https://doi.org/10.1007/978-981-19-7867-8_41). 

 <br/>
 <br/>

 Regards,
    
 <em>Best wishes for your research.</em>
