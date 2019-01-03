# Automatic Hamornic Analysis Based on Non-Chord-Tone-First Approach

## Installation Guide
1. Use `git clone git@github.com:juyaolongpaul/harmonic_analysis.git` in the terminal to clone the project, then use `cd harmonic_analysis` to go into the project folder.
2. Create a virtual environment using Python 3. An example is: `virtualenv .env --python=python3.5`. Please change `python3.5` into the one installed in your machine. For example, if your machine has Python 3.6, then use `virtualenv .env --python=python3.6`.
3. Activate the virtual environment. If you use the command line provided in the second step, you can activate it by `source ./.env/bin/activate` in Mac OS and Linux; in Windows, it is ` .\.env\Scripts\activate`.
4. Use `pip install -r requirements_gpu.txt` to install the required packages if you have a CUDA-compatiable GPU and you want to train the networks on GPU; use `pip install -r requirements_cpu.txt` if you want to train the networks on CPU.
5. Use `python main.py` to run the project.
## Workflow Overview
In `main.py`, there are many parameters to customize regarding the analytical styles, types of machine learning models, model architectures, and hyper-parameters. I will provide a chart introducing all the available combinations of these parameters in the section of "Parameter Adjustment".

For now, the project can accept Bach and Praetorius chorales, and the corresponding annotations from [here](https://natsguitar.github.io/FlexibleChoraleHarmonicAnalysisGUI/) based on my co-authored paper with Nathaniel Condit-Schultz called ["A Flexible Approach to Automated Harmonic Analysis: Multiple Annotations of Chorales by Bach and Praetorius"](http://ismir2018.ircam.fr/doc/pdfs/283_Paper.pdf), where the music and annotations are encoded in `.krn` files. Afterward, a series of functions are applied to pre-process the data to feed the machine learning models as inputs and outputs for training, and then the model will predict non-chord tones and the corresponding chord labels on the test set, presented as musicXML files for users to see the end results. Specifically, in the script of `main.py`:
* `extract_chord_labels` function is used to extract the chord labels from the `.krn` files and save them as `.txt` files. For example, for the annotations of the maximally melodic style, which can be found in the repository, the function processes the `.krn` files located under `./genos-corpus/answer-sheets/bach-chorales/New_annotation/rule_MaxMel/`, and generates `.txt` files (for chord labels) in the same directory. 
* `annotation_translation` function is used to translate the chord syntax of the annotations into one which can be recognized by `music21`, a package which this project will rely on to do various kinds of music processing. 
* `provide_path_12keys` will transpose the chord annotations into 12 possible keys, so we can use either the annotations in the key of C (without data augmentation), or use the annotations in all keys (with data augmentation) to train the model. Correspondingly, `transpose_polyphony` is used to translate the music into 12 keys. These files will all be saved in the directory of `./genos-corpus/answer-sheets/bach-chorales/New_annotation/rule_MaxMel/`. 
* Once we have the music and the chord labels ready, `generate_data_windowing_non_chord_tone_new_annotation_12keys` will translate all of them into an encoding (one-hot) which can be directly used by the machine learning models. These files will be saved in the directory of `./data_for_ML`.
* Last, `train_and_predict_non_chord_tone` will train the machine learning model, saves all the models, output all the performance information into the text file (they are saved in the directory of `./ML_result/`), and visualize all the predicted non-chord-tones as well as the chord labels through the generated musicXML files (saved in the directory of `/predicted_result`).   
* For users who want to train the model using the annotations from a different analytical style generated by the rule-based algorithm, just simply go to [this page](https://natsguitar.github.io/FlexibleChoraleHarmonicAnalysisGUI/), specify the preferences and filters you want, download the annotations (as a zip file). After that, create a folder (you can rename the directory with the name of this analytical style) under the directory of `./genos-corpus/answer-sheets/bach-chorales/New_annotation/` and copy all the files (inside of the zip file) to this directory. Last, you need to specify the parameter of source when you run `main.py` to train the model. For example, run the program with `python main.py -s 'THE NAME OF THE ANALYTICAL STYLE YOU NAMED'`.
## Parameter Adjustment
In this program, there are many ajustable parameters, ranging from the analytical styles, types of machine learning models, model architectures, and hyper-parameters. All of the parameters and the corresponding available values are shown in the chart below. The first value will be the default one. If you look at the `main.py` script, you will notice there are a few more parameters. However, they are either not essential for the task or not fully tested yet. Please let me know if you want to experiment with these parameters. 

Parameters   |Values   | Explanation
---|---|---
--source (-s)   |`rule_Maxmel` and many other analytical styles you can specify!   |The kind of annotations you want to use for training
--num_of_hidden_layer (-l)   |3, usually ranging from 2-5   |The number of hiddel layers (not effective in `SVM`)
--num_of_hidden_node (-n)   |300, usually ranging from 100-500  |The number of hidden nodes (not effective in `SVM`)
--model (-m)   |`DNN`, `SVM`, `LSTM` and `BLSTM` also available  |The types of models you want to use
--pitch (-p)   |`pitch_class`, `pitch_class_4_voices` also available   |The kind of pitch you want to use as features. `pitch_class` means using 12-d pitch class for each sonority; `pitch_class_4_voices` means using 12-d pitch class for each of the 4 voices
--window (-w)  |1, usually ranging from 0-5|The static window you can add as context for `DNN` or `SVM` model (not effective in `LSTM` and `BLSTM` since they can get the contextual information by specifying the `timestep`)   
--output (-o)   |`NCT`, `NCT_pitch_class` and `CL` also available|`NCT` means using 4-d output vector specifying which voice contains Non-chord-tones (NCTs), used with `pitch_class_4_voices`; `NCT_pitch_class` means using 12-d output vector specifying which pitch classes contain NCTs, used with `pitch_class`;  `CL` means training the model to predict chord directly, skipping NCT identification step. 
--input (-i)   |`3meter`, `barebone`, `2meter` and `NewOnset` also available   | Specify what input features, besides pitch, you are using. You can use meter features: `2meter` means you are using on/off beat feature; `3meter` means you are using 'strong beat, on/off beat' feature; `NewOnset` means whether the current slice has a real attack or not across all the pitch classes/voices. If used with `pitch_class`, it will add another 12-d vector in the input specifying which pitch classes are the real attacks; if used with `pitch_class_4_voices`, it will add another 4-d vector in the input specifying which voices have the real attacks
--timestep (-time)   |2, usually ranging from 2-5|`timestep` is the parameter used in `LSTM` and `BLSTM` to provide contextual information. 2 means LSTM will look at a slice before the current one as context; for BLSTM, it means the model will look a slice before and after the current one as context    
--predict (-pre)   |'Y', 'N' also available|Specify whether you want to predict and output the results in musicXML
### Usage Example
* Use DNN with 3 layers and 300 nodes each layer; 12-d pitch class, 3-d meter and the sign of real/fake attacks as input features, output as 12-d pitch class vector indicating which pitch class is NCT. Use a contextual window size of 1 and the annotation of maximally melodic and predict the results and output into musicXML file: `python main.py -l 3 -n 300 -m 'DNN' -w 1 -o 'NCT_pitch_class' -p 'pitch_class' -i '3meter_NewOnset -pre 'Y' -time 0`. 
* Use BLSTM with the same configuration above. Only one thing to change is that the window size needs to be set as 0, and the timestep needs to be specified: `python main.py -l 3 -n 300 -m 'BLSTM' -w 0 -o 'NCT_pitch_class' -p 'pitch_class' -i '3meter_NewOnset -pre 'Y' -time 2`
* Use DNN with the same configuration, but conduct harmonic analysis directly by skipping the identification of NCTs: `python main.py -l 3 -n 300 -m 'DNN' -w 1 -o 'CL' -p 'pitch_class' -i '3meter_NewOnset -pre 'Y' -time 0`
## Example of the Model's Architecture
For input and output encoding, I use the one-hot encoding method. The example uses 12-d pitch class, 2 meter features to indicate the current slice (highlighted in the solid line) being on/off beat and the window size 1 to add the previous slice and the following slice (highlighted in the dashed line) as context, along with 12-d pitch class for output indicating which pitch classes are NCTs, the resulting model's architecture looks like this:
![image](https://user-images.githubusercontent.com/9313094/50612164-081daa80-0ea7-11e9-85d1-b46246f7ae5f.png)
Other experimental settings are shown here:
![image](https://user-images.githubusercontent.com/9313094/50612318-91cd7800-0ea7-11e9-84ba-f1dc5fd6bb9b.png)


## The Aim of This Project
### Introduction
Despite being a core component of Western music theory, Harmonic analysis is difficult because: (1) It is a time-consuming process requiring years of training. (2) Even expert analysts will often disagree in their interpretations of certain passages, and are often inconsistent in their interpretive styles. Due to these difficulties, harmonic analysis remains a subjective endeavor, resistant to automation. As a result, few large datasets of high-quality harmonic analysis data exist, a situation that has significantly retarded the systematic study ofWestern harmony.

In this project, I propose an innovative workflow to conduct harmonic analysis automatically with multiple analytical styles using artificial intelligence. This approach will be the first of its kind to explicitly address and systematically resolve the ambiguities and interpretive flexibility of harmonic analysis. Hence, the vast amounts of generated harmonic analyses can be curated into a searchable, large-scale database, serving as an invaluable resource for music theoretic, musicological, and music information retrieval research.

The project contains four steps. First, I will define two distinct harmonic analysis rubrics – maximally melodic and maximally harmonic – with a definitive set of rules. Second, instead of requiring annotators to follow the rules and label the whole dataset from scratch, I will develop a rule-based algorithm to generate preliminary harmonic analyses. Although the algorithm cannot deal with sophisticated passages as well as annotators, it can generate 100% consistent analyses in each style. Third, annotators will modify a subset of the analyses. To make the modification consistent, multiple annotators will work on the same passage, and modify analyses based on consensus. Last, these highly consistent and accurate analyses will be used to train computers to generate analyses automatically, in which computers (machine learning models) learn just as music students learn from textbooks written by expert analysts. 

In this way, not only are we able to minimize the work of the annotators with artificial intelligence techniques (issue 1 addressed), and create consistent, accurate harmonic analysis with multiple interpretive styles (issue 2 addressed), also we will have machine learning models to generate harmonic analyses automatically for the unannotated music.
### Motivation for This Repository 
This repository specifically deals with the last step of the proposal. The first two steps of the proposal have been addressed in the [paper](http://ismir2018.ircam.fr/doc/pdfs/283_Paper.pdf) on two largely homorhythmic datasets: chorales by Praetorius (1571-1621) and Bach. Currently, this repository utilizes the annotations introduced in the paper to train machine learning models to conduct harmonic analysis automatically. In the future, we will address the step three of the proposal by hiring expert annotators to modify the preliminary analyses generated by the rule-based algorithm. Once the highly consistent and accurate analyses are obtained, the machine learning models are expected to generate the highly consistent and accurate analyses of the similar quality for the un-annotated music.

Specifically, I proposed a NCT identification [model](https://dl.acm.org/citation.cfm?id=3144753), which is considered as an essential step for harmonic analysis in the literature. Once the model identifies and removes NHTs from the music, a dictionary is defined to map harmonic tones into chords. The traditional workflow of harmonic analysis, compared to the proposed "non-chord-tone-first" appraoch, is illustrated in the figure below on the left and right side, respectively. 
![image](https://user-images.githubusercontent.com/9313094/50607126-262edf00-0e96-11e9-8f64-d0b9945a58f8.png)

## Current Progress and Result
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
DNN+12|f1:0.617±0.024<br/>FA:0.775±0.017|f1:0.648±0.029<br/>FA:0.787±0.019|f1:0.782±0.027<br/>FA:0.852±0.020|f1:0.815±0.025<br/>FA:0.867±0.020<br/>CA:0.852±0.021|||**f1:0.820±0.026<br/>FA:0.867±0.021<br/>CA:0.853±0.021**
DNN+12+NO7th||||**f1:0.836±0.024<br/>FA:0.882±0.018<br/>CA:0.883±0.018**
DNN+CL+NO7th||||**CA:0.883±0.018**
DNN+4||||f1:0.810±0.025<br/>FA:0.863±0.021|f1:0.799±0.020|f1:0.789±0.028<br/>FA:0.842±0.022
DNN+4<br/>Original key||||f1:0.780±0.025|
DNN+4+A||||||f1:0.794±0.024<br/>FA:0.846±0.018
DNN+CL||||CA:0.851±0.019||CA:0.850±0.021
SVM+CL||||CA:0.838±0.019
LSTM+4||||f1:0.795±0.025<br/>FA:0.856±0.019
BLSTM+4||||f1:0.797±0.025<br/>||f1:0.781±0.020<br/>
BLSTM+12||||f1:0.801±0.023<br/>|||f1:0.809±0.025<br/>FA:0.866±0.020<br/>
### Useful Findings
* Overall, using the same input and output structures, DNN achieves the best performance, BLSTM is 0.001 consistantly lower than DNN appraoch in f1-measure; SVM has about 1.5-2% consistant lower chord accuracy compared to DNN.
* The best input combination so far is PC12+M+W+O12, reaching a f1-measure of 0.820
* Results show that if only PC12 is used as input feature on DNN+12, f1-measure is only 0.617, but with a small window as context, the performance boosts significantly to 0.782, and with the meter features, it further improves to 0.815. By specifying the sign of real/fake attack on 12 pitch class, the performance further improves to 0.820.
* Results show that using pitch class for 4 voices (to incorporate more voice leading infomation) actually undermines the performance by about 0.002 in f1-measure, since it causes the problem of overfitting. Therefore, we need more training data in order to use these features. 
* By collapsing 7th chord into triads, the performance further improves into 0.836 in f1-measure, and frame accuracy and chord accuracy is above 88%.
## Examples of the Result
The program can output the predicted results, along with the ground truth annotations, into musicXML files. The figure below is an example:

![image](https://user-images.githubusercontent.com/9313094/50618085-98b3b500-0ebe-11e9-8d8e-10ce73ea3531.png)

There are 6 rows underneath the score. The first one is the ground truth chord labels, the second one is the corresponding ground truth non-chord tones, the third one is the model’s predicted NCTs, the fourth one entails whether the predicted NCTs are correct. The fifth one is the inferred chord label (based on a heuristic algorithm I wrote), and the last one entails whether the predicted chord label is correct.
## Current Problem to Solve
* Not enough data to train: There are many other features to experiment, but once the scale of the input vector increases, even only adding voice leading information by introducing 12-d pitch class for each voice will lead to the problem of over-fitting. Although the model achieves an f1-measure of 0.820 using only 12-d pitch class, the information of voice leading is very limited in this case, and some voice leading errors can be observed in the generated musicXML files.  Therefore, by introducing 12-d pitch class for each voice (12*4=48 in total), the performance should improve once we have enough data.
* Bad performances on the 7th chords: The machine learning model has a poor performance distinguishing 7th chords and their corresponding triads (the majority of the errors are 7th chords mis-classified as triads, and the accuracy of all 7th chords are below 50% in average), comprising more than 10% of the total errors. Once the 7th chords are collapsed into traids, the f1-measure improves from 0.815 to 0.836, where the error rate decreases by more than 10%. 
* Some of the ground truth annotations are contradictory: There are some annotations where my model constantly makes mistakes, but when I examine these slices, those annotations do not make a lot of sense to me, especially the ones around cadences. Overall, the annotations often choose V64-I around cadences, but there are inconsistencies. For example, in chorale 233, the annotations choose I64-V-I(m), coloured in blue, where you can see my model adopts V64-I, and compared to the annotations, they are considered as "mistakes":
![image](https://user-images.githubusercontent.com/9313094/50620390-fbac4880-0ecc-11e9-8297-dae321e1adf7.png)

However, in later section (two measures later) of chorale 233, the annotations adopt V64-I again: 
![image](https://user-images.githubusercontent.com/9313094/50620405-05ce4700-0ecd-11e9-8a4a-2018c441c349.png)

Furthermore, there are other contradictory annotations around cadences. For example, chorale 061 measure 16, the annotations are four F major, which should really be g major instead:
![image](https://user-images.githubusercontent.com/9313094/50620411-0d8deb80-0ecd-11e9-9db3-de576f42e4ea.png)

In chorale 012 M13, the annotations are four E minor, which should really be G major:
![image](https://user-images.githubusercontent.com/9313094/50620423-1a124400-0ecd-11e9-9512-36a81da1766b.png)

Sometimes, the annotations do not really match the sonorities. In chorale 064 measure 1. The annotations are four A minor in a row where the sonorites match C major and D major perfectly:
![image](https://user-images.githubusercontent.com/9313094/50620435-2eeed780-0ecd-11e9-8aa3-8c17c504c7f6.png)

In chorale 352 measure 17, the annotations are three E minor in a row where there is no natural G (but G# found in the adjacent slices):
![image](https://user-images.githubusercontent.com/9313094/50620446-3ada9980-0ecd-11e9-980f-0cb0ce9f1e61.png)

As a part of the training data, I am afraid that these problematic annotations will be detrimental to my training process, and they also will create an artificial ceiling for the evaluation as well.

## Future Work
* Gather more data
* Hire analysts to improve the quality of the annotations generated by the rule-based model.
* Train the machine learning models to conduct harmonic analysis automatically 
