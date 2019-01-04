---
layout: default
title: Current Problems to Solve 

---

## Current Problems to Solve

* Not enough data to train: There are many other features to experiment, but once the scale of the input vector increases, even only adding voice leading information by introducing 12-d pitch class for each voice will lead to the problem of over-fitting. Although the model achieves an f1-measure of 0.822 using only 12-d pitch class, the information of voice leading is very limited in this case, and some voice leading errors can be observed in the generated musicXML files.  Therefore, by introducing 12-d pitch class for each voice (12*4=48 in total), the performance should improve once we have enough data.
* Bad performances on the 7th chords: The machine learning model has a poor performance distinguishing 7th chords and their corresponding triads (the majority of the errors are 7th chords mis-classified as triads, and the accuracy of all 7th chords are below 50% in average), comprising more than 10% of the total errors. Once the 7th chords are collapsed into traids, the f1-measure improves from 0.815 to 0.836, where the error rate decreases by more than 10%. 
* Some of the ground truth annotations are problematic: There are some annotations where my model constantly makes mistakes, but when I examine these slices, those annotations do not make a lot of sense to me, especially the ones around cadences. Overall, the annotations often choose V64-I around cadences, but there are inconsistencies. For example, in chorale 233, the annotations choose I64-V-I(m), coloured in blue, where you can see my model adopts V64-I, and compared to the annotations, they are considered as "mistakes":
![image](https://user-images.githubusercontent.com/9313094/50620390-fbac4880-0ecc-11e9-8297-dae321e1adf7.png)

However, in later section (two measures later) of chorale 233, the annotations adopt V64-I again: 
![image](https://user-images.githubusercontent.com/9313094/50620405-05ce4700-0ecd-11e9-8a4a-2018c441c349.png)

Furthermore, there are other problematic annotations around cadences. For example, chorale 061 measure 16, the annotations are four F major, which should really be g major instead:
![image](https://user-images.githubusercontent.com/9313094/50620411-0d8deb80-0ecd-11e9-9db3-de576f42e4ea.png)

In chorale 012 M13, the annotations are four E minor, which should really be G major:
![image](https://user-images.githubusercontent.com/9313094/50620423-1a124400-0ecd-11e9-9512-36a81da1766b.png)

Sometimes, the annotations do not really match the sonorities. In chorale 064 measure 1. The annotations are four A minor in a row where the sonorites match C major and D major perfectly:
![image](https://user-images.githubusercontent.com/9313094/50620435-2eeed780-0ecd-11e9-8aa3-8c17c504c7f6.png)

In chorale 352 measure 17, the annotations are three E minor in a row where there is no natural G (but G# found in the adjacent slices):
![image](https://user-images.githubusercontent.com/9313094/50620446-3ada9980-0ecd-11e9-980f-0cb0ce9f1e61.png)

As a part of the training data, I am afraid that these problematic annotations will be detrimental to my training process, and they will create an artificial ceiling for the evaluation as well.