# Automatic Hamornic Analysis Based on Non-Chord-Tone-First Approach

## Installation Guide
1. Use `git clone git@github.com:juyaolongpaul/harmonic_analysis.git` in the terminal to clone the project, then use `cd harmonic_analysis` to go into the project folder
2. Create a virtual environment using Python 3. An example is: `virtualenv .env --python=python3.5`. Please change `python3.5` into the one installed in your machine. For example, if your machine has Python 3.6, then use `python3.6`
3. Activate the virtual environment. If you use the command line provided in the second step, you can activate it by `source ./.env/bin/activate` in Mac OS and Linux; in Windows, it is ` .\.env\Scripts\activate`
4. Use `pip install -r requirements_gpu.txt` to install the required packages if you have a CUDA-compatiable GPU and you want to train the networks on GPU; use `pip install -r requirements_cpu.txt` if you want to train the networks on CPU
5. Use `python main.py` to run the project
## Workflow Overview
In `main.py`, there are many parameters to customize regarding the analytical styles, types of machine learning models, model architectures, and hyper-parameters. I will provide a chart introducing all the available combinations of these parameters below.

For now, the project can accept Bach and Praetorius chorales and the corresponding annotations from [here](https://natsguitar.github.io/FlexibleChoraleHarmonicAnalysisGUI/) based on my co-authored paper with Nathaniel Condit-Schultz called ["A Flexible Approach to Automated Harmonic Analysis: Multiple Annotations of Chorales by Bach and Praetorius"](http://ismir2018.ircam.fr/doc/pdfs/283_Paper.pdf), where the music and annotations are encoded in `.krn` files. Afterward, a series of functions are applied to pre-process the data to feed the machine learning models as inputs and outputs for learning, and then the model will predict non-chord tones and the corresponding chord labels on the test set, presented as musicXML files for users to see the end results. Specifically:
* `extract_chord_labels` function is used to extract the chord labels from the `.krn` files and save them as `.txt` files. For example, for the maximally melodic style (since this Github repository already provide the annotations in this style), the `.krn` files are located under `./genos-corpus/answer-sheets/bach-chorales/New_annotation/rule_MaxMel/`, and the generated `.txt` files (for chord labels) are saved in the same directory. 
* `annotation_translation` function is used to translate the chord syntax into one recognizable by `music21`, a package which this project will rely on in order to do various music processing. 
* `provide_path_12keys` will transpose the chord annotations into 12 possible keys, so we can use either the annotations in the key of C (without data augmentation) to train the model, or use the annotations in all keys (with data augmentation) to train the model. Correspondingly, `transpose_polyphony` is used to translate the music into 12 keys as well. These files will all be saved in the directory of `./genos-corpus/answer-sheets/bach-chorales/New_annotation/rule_MaxMel/`, for example. 
* Once we have the music and the chord labels ready, `generate_data_windowing_non_chord_tone_new_annotation_12keys` will translate all of them into a (one-hot) encoding which can be directly used by the machine learning models. These files will be saved in the directory of `./data_for_ML`.
* Last, `train_and_predict_non_chord_tone` will train the machine learning model, saves all the models, output all the performance information into the text file (models and performance infomation are saved in the directory of `./ML_result/`), and visualize all the predicted non-chord-tones as well as the chord labels through generated musicXML files (saved in the directory of `/predicted_result`).   
* For users who want to train the model using annotations from a different analytical style generated by the rule-based algorithm, just simply go to [this page](https://natsguitar.github.io/FlexibleChoraleHarmonicAnalysisGUI/), specify the preferences and filters you want, download the annotations (as a zip file). After that, create a folder (you can rename the directory with the name of this analytical style) under the directory of `./genos-corpus/answer-sheets/bach-chorales/New_annotation/` and copy all the files (inside of the zip file) to this directory. Last, you need to specify the parameter of source when you run `main.py` to train the model. For example, run the program with `python main.py -s 'THE NAME OF THE ANALYTICAL STYLE'`.
## Parameter Adjustment
In this program, there are many ajustable parameters, ranging from the analytical styles, types of machine learning models, model architectures, and hyper-parameters. All of the parameters and the corresponding available values are shown in the chart below. The first value will be the default one. If you look at the `main.py` script, you will notice there are a few more parameters. However, they are either not essential for the task or not fully tested yet. Please let me know if you want to experiment with these parameters as well. 

Parameters   |Values   | Explanation
---|---|---
--source (-s)   |'rule_Maxmel' and many other analytical styles you can specify!   |The kind of data you want to use
--num_of_hidden_layer (-l)   |3, usually ranging from 2-5   |The number of hiddel layers (not effective in 'SVM')
--num_of_hidden_node (-n)   |300, usually ranging from 100-500  |The number of hidden nodes (not effective in 'SVM')
--model (-m)   |'DNN', 'SVM', 'LSTM', 'BLSTM' also available  |The types of models you can use
--pitch (-p)   |'pitch_class', 'pitch_class_4_voices' also available   |The kind of pitch you want to use as features. `pitch_class` means using 12-d pitch class for each sonority; 'pitch_class_4_voices' means using 12-d pitch class for each of the 4 voices
--window (-w)  |1, usually ranging from 0-5|The static window you can add as context for `DNN` or `SVM` model (not effective in 'LSTM' and 'BLSTM' since they can get the contextual information by specifying the `timestep`)   
--output (-o)   |'NCT', 'NCT_pitch_class', 'CL'|'NCT' means using 4-d output vector specifying which voice contains Non-chord-tones (NCTs), used with 'pitch_class_4_voices'; 'NCT_pitch_class' means using 12-d output vector specifying which pitch classes contain NCTs, used with 'pitch_class';  'CL' means training the model to predict chord directly, skipping NCT identification step. 
--input (-i)   |'3meter', 'barebone', '2meter', 'NewOnset' available   | Specify what input features, besides pitch, you are using. You can use meter features: '2meter' means you are using on/off beat feature; '3meter' means you are using 'strong beat, on/off beat' feature; 'NewOnset' means whether the current slice has a real attack or not across all the pitch classes/voices. If used with 'pitch_class', it will add another 12-d vector in the input specifying which pitch classes are the real attacks; if used with 'pitch_class_4_voices', it will add another 4-d vector in the input specifying which voices have the real attacks
--timestep (-time)   |2, usually ranging from 2-5|`timestep` is the parameter used in `LSTM` and `BLSTM` to provide contextual information. 2 means LSTM will look at a slice before the current one as context; for BLSTM, it means the model will look a slice before and after the current one as context    
--predict (-pre)   |'Y', 'N' available|Specify whether you want to predict and output the resultd in musicXML
### Usage example
* Use DNN with 3 layers and 300 nodes each layer; 12-d pitch class, 3-d meter and the sign of real/fake attacks as input feature, output as 12-d pitch class vector indicating which pitch class is NCT, using a contextual window size of 1; use the annotation of maximally melodic and predict the results and output into musicXML file: `python main.py -l 3 -n 300 -m 'DNN' -w 1 -o 'NCT_pitch_class' -p 'pitch_class' -i '3meter_NewOnset -pre 'Y' -time 0`. 
* Use BLSTM with the same configuration above. Only one thing to notice is that the window size needs to set as 0 and specify timestep instead: `python main.py -l 3 -n 300 -m 'BLSTM' -w 0 -o 'NCT_pitch_class' -p 'pitch_class' -i '3meter_NewOnset -pre 'Y' -time 2`
* Use DNN with the same configuration, but conduct harmonic analysis directly by skipping the identification of NCTs: 'python main.py -l 3 -n 300 -m 'DNN' -w 1 -o 'CL' -p 'pitch_class' -i '3meter_NewOnset -pre 'Y' -time 0'
## The Aim of This Project
### Introduction
Despite being a core component of Western music theory, Harmonic analysis is difficult because: (1) It is a time-consuming process requiring years of training. (2) Even expert analysts will often disagree in their interpretations of certain passages, and are often inconsistent in their interpretive styles. Due to these difficulties, harmonic analysis remains a subjective endeavor, resistant to automation. As a result, few large datasets of high-quality harmonic analysis data exist, a situation that has significantly retarded the systematic study ofWestern harmony.

In this project, I propose an innovative workflow to conduct harmonic analysis automatically with multiple analytical styles using artificial intelligence. This approach will be the first of its kind to explicitly address and systematically resolve the ambiguities and interpretive flexibility of harmonic analysis. Hence, the vast amounts of generated harmonic analyses can be curated into a searchable, large-scale database, serving as an invaluable resource for music theoretic, musicological, and music information retrieval research.

The project contains four steps. First, I will define two distinct harmonic analysis rubrics – maximally melodic and maximally harmonic – with a definitive set of rules. Second, instead of requiring annotators to follow the rules and label the whole dataset from scratch, I will develop a rule-based algorithm to generate preliminary harmonic analyses. Although the algorithm cannot deal with sophisticated passages as well as annotators, it can generate 100% consistent analyses in each style. Third, annotators will modify a subset of the analyses. To make the modification consistent, multiple annotators will work on the same passage, and modify analyses based on consensus. Last, these highly consistent and accurate analyses will be used to train computers to generate analyses automatically, in which computers (machine learning models) learn just as music students learn from textbooks written by expert analysts. 

In this way, not only are we able to minimize the work of the annotators with artificial intelligence techniques (issue 1 addressed), and create consistent, accurate harmonic analysis with multiple interpretive styles (issue 2 addressed), also we will have machine learning models to generate harmonic analyses automatically for the unannotated music.
### Motivation for This Repository 
This repository specifically deals with the last step of the proposal. The first two steps of the proposal have been addressed in our [paper](http://ismir2018.ircam.fr/doc/pdfs/283_Paper.pdf) on two largely homorhythmic datasets: chorales by Praetorius (1571-1621) and Bach. Currently, this repository utilizes the annotations introduced in the paper to train machine learning models to conduct harmonic analysis automatically. In the future, we will address the step three of the proposal by hiring expert annotators to modify the preliminary analyses generated by the rule-based algorithm. Once the highly consistent and accurate analyses are obtained, hopefully the machine learning models will generate the highly consistent and accurate analyses for the un-annotated music.

Specifically, I proposed a NCT identification [model](https://dl.acm.org/citation.cfm?id=3144753), which is considered as an essential step for harmonic analysis in the literature. Once the model identifies and removes NHTs from the music, a dictionary is defined to map harmonic tones into chords. The workflow of this approach, compared to the traditional harmonic analysis, is illustrated in the figure below on the right and left side, respectively. 
![image](https://user-images.githubusercontent.com/9313094/50607126-262edf00-0e96-11e9-8f64-d0b9945a58f8.png)

## Current Progress and Result
## Examples of the Result
## Current Problem to Solve
## Future Work
