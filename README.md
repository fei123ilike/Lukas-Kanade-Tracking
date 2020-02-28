# Lucas-Kanade-tracking-and-Correlation-Filters
This repository contains implementation of **Lucas-Kanade algorithm** proposed by Lucas and Kanade. Lucas-Kanade algorithm can be used for **sparse optical flow** (associate feature points across frames) and **tracking** (associate image patch cross frames). 

This repo implements the algorithm for tracking a single template across 400 frames video.   
Please download the data from [here](https://drive.google.com/open?id=11W2dOSgI1G4udoyUc9OA6Im1EeaHmfbJ), unzip and put it in /data folder.

## Lucas Kanade Tracking with one single template  
The "vanilla" algorithm for tracking with single template from the first frame. Reference paper [Lucas-Kanade 20 Years On: A Unifying Framework](https://www.ri.cmu.edu/pub_files/pub3/baker_simon_2002_3/baker_simon_2002_3.pdf)  

**Example**

<img src="https://github.com/fei123ilike/Lukas-Kanade-Tracking/blob/master/results/car1.png" width=30% height=30%><img src="https://github.com/fei123ilike/Lukas-Kanade-Tracking/blob/master/results/car100.png" width=30% height=30%><img src="https://github.com/fei123ilike/Lukas-Kanade-Tracking/blob/master/results/car300.png" width=30% height=30%>

**Run**
```
python ./code/testCarSequence.py
```
## Lucas Kanade Tracking with corrected template  
To address the bbox drifting issue, reset the reference frame every 100 frames.Reference paper [The Template Update Problem](https://www.ri.cmu.edu/publications/the-template-update-problem/)  

**Example**

<img src="https://github.com/fei123ilike/Lukas-Kanade-Tracking/blob/master/results/car_correct1.png" width=30% height=30%><img src="https://github.com/fei123ilike/Lukas-Kanade-Tracking/blob/master/results/car_correct100.png" width=30% height=30%><img src="https://github.com/fei123ilike/Lukas-Kanade-Tracking/blob/master/results/car_correct300.png" width=30% height=30%>

**Run**
```
python ./code/testCarSequenceWithTemplateCorrection.py
```
## Lucas Kanade Tracking with appearance basis  
The prior mehod may suffer from drastic appearance change like rotation or deformation, to address this issue, we can decompose the template into a series of bases,  track the object with predefined bases. 

Red bbox: w/o basis.   Green bbox: w/ basis.

**Example**

<img src="https://github.com/fei123ilike/Lukas-Kanade-Tracking/blob/master/results/toy1.png" width=30% height=30%><img src="https://github.com/fei123ilike/Lukas-Kanade-Tracking/blob/master/results/toy200.png" width=30% height=30%><img src="https://github.com/fei123ilike/Lukas-Kanade-Tracking/blob/master/results/toy300.png" width=30% height=30%>

**Run**
```
python ./code/testSylvSequence.py
```

## Lucas Kanade Tracking with dominant affine motion  

**Example**

<img src="https://github.com/fei123ilike/Lukas-Kanade-Tracking/blob/master/results/inverse30.png" width=30% height=30%><img src="https://github.com/fei123ilike/Lukas-Kanade-Tracking/blob/master/results/inverse60.png" width=30% height=30%><img src="https://github.com/fei123ilike/Lukas-Kanade-Tracking/blob/master/results/inverse90.png" width=30% height=30%>

**Run**
```
python ./code/testAerialSequence.py
```
