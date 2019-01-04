---
layout: default
title: Current Progress and Results 

---

## Current Progress and Results

Currently, all the experiments are conducted on the maximally melodic annotations for 366 Bach chorales. All the experiments are using 10-fold cross validation. For evaluation metrics, I use f1-measure (abbreviated as F1) for NCT identification accuracy; frame accuracy (abbreviated as FA) to indicate the accuracy for each slice; chord accuracy (abbreviated as CA) to indicate the predicted chord accuracy compared to the ground truth annotations. The chart below specifies all the results I have got so far: The row header indicates all the experimented input features, the column header indicates all combinations between the output and different models. To save space, I use a series of acronyms for the choice of input and output architectures. Specifically:

### Acronyms for the Row Header

* I use 'PC' for pitch class. 'PC12' means 12-d pitch class category as "C, C#/Db, D, D#/Eb, E, F, F#/Gb, G, G#/Ab, A, A#/Bb, B". 'PC48' means 12-d pitch class is specified for each voice (among 4 voices). 
* I use 'M' to represent the use of 2 or 3 meter features (I did not differenciate between 2 and 3 meters since they achieve almost the same performance). 
* I use "W" to indicate the use of windows as context. Similarly, the window size of 1 or 2 usually has the similar performances, so they are not differentiated here.
* I also experiment generic pitch class as "C, D, E, F, G, A, B" and use "PC7" to represent it. "PC28" represents the generic pitch class for each voice (among 4 voices). 
* To specify whether the current slice contains a real/fake attack (onset) for a certain pitch, I use "O12" to indicate a 12-d vector specifying which pitch class contains real/fake attack by setting the value to 1 and 0, respectively; I use "O4" to incidate a 4-d vector specifying which voices contain real/fake attack. "O12" is used with "PC12/PC7" and "O4" is used with "PC48/PC28" for now. 
* I also use data augmentation in some cases. For the non-augmented approach, I tranpose all the chorales in the key of C; for the augmented appraoch, I transpose the data to 12 possible keys to increase the size of the training data, and use the data in the original key for validating and testing. I use "A" to indicate the use of data augmentation.

### Acronyms for the Column Header

* Currently, the legal chord qualities are major, minor, diminished for triads; dominant seventh, minor seventh, major seventh, half diminised seventh and fully diminished seventh for seventh chords. I also try to collapse all the seventh chords into triads in some experiments, indicated as "NO7th".
* I use "4" to indicate a 4-d vector for output that specifies which voice contains NCTs, "12" to indicate a 12-d vector for output that specifies which pitch class contains NCTs, "CL" (chord label) to indicate the appraoch of direct chord prediction skipping non-chord-tone-first approach. Consequently, the dimension of the output vector equals to the number of chord categories found in the annotations.
* For (B)LSTM models, the timestep is 2 (for best performances).
* I also ignored the number of hidden layers and hidden nodes across different models since they have little effect on the performances.
Here are the results:

### Results

Parameters   |PC12   | PC12+M|PC12+W|PC12+M+W|PC7+M+W|PC48+M+W|PC12+M+W+O12
---|---|---|---|---|---|---|---
DNN+12|f1:0.617±0.024<br/>FA:0.775±0.017|f1:0.648±0.029<br/>FA:0.787±0.019|f1:0.782±0.027<br/>FA:0.852±0.020|f1:0.815±0.025<br/>FA:0.867±0.020<br/>CA:0.852±0.021|||**f1:0.822±0.024<br/>FA:0.869±0.021<br/>CA:0.855±0.021**
DNN+12+NO7th||||**f1:0.836±0.024<br/>FA:0.882±0.018<br/>CA:0.883±0.018**|||
DNN+CL+NO7th||||**CA:0.883±0.018**|||
DNN+4||||f1:0.810±0.025<br/>FA:0.863±0.021|f1:0.799±0.020|f1:0.789±0.028<br/>FA:0.842±0.022
DNN+4<br/>Original key||||f1:0.780±0.025|
DNN+4+A||||||f1:0.794±0.024<br/>FA:0.846±0.018|
DNN+CL||||CA:0.851±0.019||CA:0.850±0.021|
SVM+CL||||CA:0.838±0.019|||
LSTM+4||||f1:0.795±0.025<br/>FA:0.856±0.019|||
BLSTM+4||||f1:0.797±0.025<br/>||f1:0.781±0.020<br/>|
BLSTM+12||||f1:0.801±0.023<br/>|||f1:0.809±0.025<br/>FA:0.866±0.020<br/>

### Useful Findings

* Overall, using the same input and output structures, DNN achieves the best performance, BLSTM is 0.001 consistantly lower than DNN appraoch in f1-measure; SVM has about 1.5-2% consistant lower chord accuracy compared to DNN.
* The best input combination so far is PC12+M+W+O12, reaching a f1-measure of 0.822.
* Results show that if only PC12 is used as input feature on DNN+12, f1-measure is only 0.617, but with a small window as context, the performance boosts significantly to 0.782, and with the meter features, it further improves to 0.815. By specifying the sign of real/fake attack on 12 pitch class, the performance further improves to 0.822.
* Results show that using pitch class for 4 voices (to incorporate more voice leading infomation) actually undermines the performance by about 0.002 in f1-measure, since it causes the problem of overfitting. Therefore, we need more training data in order to use these features. 
* By collapsing 7th chord into triads, the performance further improves into 0.836 in f1-measure, and frame accuracy and chord accuracy is above 88%.