# Detection-and-Localization-of-Copy-Move-Image-Forgery-using-Deep-Learning-Networks
<br/>

![](https://github.com/AkashKV-1998/Detection-and-Localization-of-Copy-Move-Image-Forgery-using-Deep-Learning-Networks/blob/main/Image%20Files%20md/logo.jpg)

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



The repository contains analysis and results of different copy-move forgery detection approaches.

## Directory Details:
<br/>

    1. Results and Analysis __________________________________________________                                    : THE DIRECTORY CONTAINS OUR ANALYSIS AND RESULTS
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


    2. Reference code____                                                                                         : CODE THAT WE HAVE IMPLEMENTED FROM OTHER PAPERS
                         |
                         |
         Code of Rotational copy-move forgery 
         detection using SIFT and region 
         growing strategies
         
         
    3. Other References Paper Bib file                                                                            : OUR MAIN REFERENCES
    
    4. Other Docs                                                                                                 : OTHER IMPORTANT DOCUMENTS
    

 <br/>

## Results and Analysis 
    
Currently, we have tested 3 codes with [CoMoFoD small dataset](https://www.vcl.fer.hr/comofod/download.html) and [MICC-F2000](http://lci.micc.unifi.it/labd/2015/01/copy-move-forgery-detection-and-localization/) dataset for detection and localization for confusion matrix. The tested codes are:

1. DBSCAN-Based Copy-Move forgery detection 

    Article : [Link](https://medium.com/analytics-vidhya/copy-move-forgery-detection-using-sift-and-dbscan-clustering-4a179c36293e)
    
    Code    : [Link](https://github.com/Himj266/DBSCAN-Copy-Move-Foregry-Detection)
    
2. DCT-Based Copy-Move forgery detection
        
    Code    : [Link](https://github.com/alperencubuk/Copy-Move-Forgery-Detection)
    
3. Forensic Analysis of Copy-Move Attack with Robust Duplication Detection(FACMARD)
    
    Paper   : [Link](https://link.springer.com/chapter/10.1007%2F978-3-030-73689-7_39)
    
    Code    : [Link](https://github.com/rahmatnazali/image-copy-move-detection)

## Paper Implementation 
    
The code of the paper 'Rotational copy-move forgery detection using SIFT and region growing strategies' ([Paper Link](https://link.springer.com/article/10.1007/s11042-019-7165-8)) we have implemented and uploaded in the directory '[Reference Code](https://github.com/AkashKV-1998/Detection-and-Localization-of-Copy-Move-Image-Forgery-using-Deep-Learning-Networks/tree/main/Reference%20Code/Code%20of%20Rotational%20copy-move%20forgery%20detection%20using%20SIFT%20and%20region%20growing%20strategies)'. But the code shows few error and localization is not accurate. The error is possibly on Hu moment calculations. If you want to reuse the code, we suggest kindly try to correct the errors in the code for better results.

## Other Reference 
    
 The directory '[Other Reference](https://github.com/AkashKV-1998/Detection-and-Localization-of-Copy-Move-Image-Forgery-using-Deep-Learning-Networks/tree/main/Other%20References%20Paper%20Bib%20file)' contains our entire references in a bibtex file and also in HTML file for your reference.
    
 <br/>
 <br/>

 Regards,
    
 <em>Best wishes for your research.</em>
