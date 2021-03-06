# this file offers code realizing certain functions
import os
from music21 import *
from scipy import stats
import numpy as np
from collections import Counter
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def count_pickup_measure_NO():
    for fn in os.listdir(r'C:\Users\juyao\Documents\Github\harmonic_analysis\Bach_chorale_FB\FB_source\musicXML_master'):
        if 'FB_align' not in fn: continue
        print(fn)
        s = converter.parse(os.path.join(r'C:\Users\juyao\Documents\Github\harmonic_analysis\Bach_chorale_FB\FB_source\musicXML_master', fn))
        previous_beat = 0
        previous_mm_number = 0
        for i, thisChord in enumerate(s.parts[-1].recurse().getElementsByClass('Chord')):
            #print('measure number', thisChord.measureNumber, thisChord, 'beat:', thisChord.beat)
            if thisChord.measureNumber == previous_mm_number:
                if thisChord.beat < previous_beat:
                    print('pick up measure found!')
                previous_beat = thisChord.beat
            else:
                previous_beat = 0
                previous_mm_number = thisChord.measureNumber
    # this one counts the number of pick up measures and output them


def put_chords_into_files(sChord, a_chord_label=[], replace='Y', f=[]):
    previous_chord = []
    all_chords = []
    for i, thisChord in enumerate(sChord.recurse().getElementsByClass('Chord')):
        # obtain all the chord labels
        chord_label = []
        for j, label in enumerate(thisChord.lyrics):
            if len(label.text) > 0:
                if label.text[0].isalpha() and label.text[0].isupper(): # this is a chord label
                    chord_label.append(label.text)
        if i == 0 and (len(chord_label) == 0):
            print('the first chord is empty!')
        elif len(chord_label) == 0:
            if not previous_chord == []:
                if f != []:
                    print(previous_chord, file=f)
                a_chord_label.append(previous_chord)
                all_chords.append(previous_chord)
            # else:
            #     print('debug')
        else:
            if f != []:
                print(chord_label, file=f)
            a_chord_label.append(chord_label)
            all_chords.append(chord_label)
        if chord_label != []:
            previous_chord = chord_label
    return a_chord_label, all_chords


def extract_chord_labels():
    path = os.path.join(os.getcwd(), 'Bach_chorale_FB', 'FB_source', 'musicXML_master')
    for fn in os.listdir(path):
        if 'chordify' not in fn:
            continue
        if 'FB.txt' in fn or 'IR.txt' in fn:
            continue
        print('extracting chord labels for', fn)
        f_FB = open(os.path.join(path, fn[:-4] + '_FB.txt'), 'w')
        f_IR = open(os.path.join(path, fn[:-4] + '_IR.txt'), 'w')
        s = converter.parse(os.path.join(path, fn))
        voice_FB = s.parts[-2]
        voice_IR = s.parts[-1]
        put_chords_into_files(voice_IR, f_IR)
        put_chords_into_files(voice_FB, f_FB)
        f_FB.close()
        f_IR.close()


def compare_against_sam():
    path_FB = os.path.join(os.getcwd(), 'genos-corpus', 'answer-sheets', 'bach-chorales', 'New_annotation', 'ISMIR2019', 'comparing_to_FB_translation', 'FB')
    path_IR = os.path.join(os.getcwd(), 'genos-corpus', 'answer-sheets', 'bach-chorales', 'New_annotation', 'ISMIR2019', 'comparing_to_FB_translation', 'IR')
    path_GT = os.path.join(os.getcwd(), 'genos-corpus', 'answer-sheets', 'bach-chorales', 'New_annotation', 'ISMIR2019', 'comparing_to_FB_translation', 'Sam')
    a_counter = 0
    a_counter_correct_FB = 0
    a_counter_correct_IR = 0
    FB_accuracy = []
    IR_accuracy = []
    FB_error = []
    IR_error = []
    for fn in os.listdir(path_GT):
        f_FB = open(os.path.join(path_FB, fn[:-4] + '_FB_lyric_chordify_FB.txt'))
        f_IR = open(os.path.join(path_IR, fn[:-4] + '_FB_lyric_chordify_IR.txt'))
        f_GT = open(os.path.join(path_GT, fn))
        FB_results = f_FB.readlines()
        IR_results = f_IR.readlines()
        GT_results = f_GT.readlines()
        for i, elem in enumerate(FB_results):
            if 'maj7' in elem:
                FB_results[i] = FB_results[i].replace('maj', 'M')
        for i, elem in enumerate(IR_results):
            if 'maj7' in elem:
                IR_results[i] = IR_results[i].replace('maj', 'M')
        if not len(FB_results) == len(IR_results) and len(FB_results) == len(GT_results):
            print('does not align!')
        counter = len(IR_results)
        counter_correct_FB = 0
        counter_correct_IR = 0
        for i, each_GT_label in enumerate(GT_results):
            if each_GT_label == FB_results[i]:
                counter_correct_FB += 1
                a_counter_correct_FB += 1
            else:
                FB_error.append((each_GT_label+':'+FB_results[i]).replace('\n', ''))
            if each_GT_label == IR_results[i]:
                counter_correct_IR += 1
                a_counter_correct_IR += 1
            else:
                IR_error.append((each_GT_label+':'+IR_results[i]).replace('\n', ''))
        print('FB accuracy for', fn, 'is', counter_correct_FB / counter)
        FB_accuracy.append((counter_correct_FB / counter) * 100)
        print('IR accuracy for', fn, 'is', counter_correct_IR / counter)
        IR_accuracy.append((counter_correct_IR / counter) * 100)
        a_counter += counter
    print('FB errors', Counter(FB_error), 'total count is', len(FB_error))
    c = Counter(FB_error)
    s = sum(c.values())
    for elem, count in c.items():
        print(elem, count / s)
    print('IR errors', Counter(IR_error), 'total count is', len(IR_error))
    c = Counter(IR_error)
    s = sum(c.values())
    for elem, count in c.items():
        print(elem, count / s)
    print('Overall FB accuracy for is', np.mean(FB_accuracy), '%', '±', stats.sem(FB_accuracy), '%')
    print('Overall FB accuracy for is', np.mean(IR_accuracy), '%', '±', stats.sem(IR_accuracy), '%')
    print('Overall FB accuracy for is', np.mean(FB_accuracy), '%', '±', np.std(FB_accuracy), '%')
    print('Overall FB accuracy for is', np.mean(IR_accuracy), '%', '±', np.std(IR_accuracy), '%')


def parse_filename(f):
    f = f.replace('.musi', '').rsplit('_', 3)
    filename, stage, a, b = f
    return filename, stage


def get_index(fn, stage, keyword):
    if '2_op13_1_' in fn and keyword != 'omr':
        replace = fn.replace(stage, keyword).replace('C', 'a_ori')
    else:
        replace = fn.replace(stage, keyword)
    with open(os.path.join(inputpath, replace)) as f:
        json_dict = json.loads(f.read())
        json_dict = {float(k):v for k, v in json_dict.items()}
        index = list(json_dict.keys())
        index = [float(value) for value in index]
    return index, json_dict


def compare_chord_labels(inputpath, keyword1, keyword2, keyword3, keyword4):
    a_diff1 = []
    a_diff2 = []
    a_diff3 = []
    for fn in os.listdir(inputpath):
        if not os.path.isdir(os.path.join(inputpath, fn)):
            if fn[-3:] == 'txt' and 'omr' in fn:
                # if 'op44iii_1' in fn or 'op44iii_2' in fn:
                #     continue
                # if 'op44iii_2' not in fn:
                #     continue
                print(fn)
                # f1 = open(os.path.join(input_path_array[0], fn))
                # try:
                #     f2 = open(os.path.join(input_path_array[1], fn))
                # except:
                #     f2 = open(os.path.join(input_path_array[1], fn.replace(keyword1, keyword2)))
                # json_dict1 = json.loads(f1)
                # json_dict2 = json.loads(f1)
                filename, stage = parse_filename(fn.strip())
                try:
                    get_index(fn, stage, keyword1)
                    index1, dict1 = get_index(fn, stage, keyword1)
                except:
                    continue
                try:
                    get_index(fn, stage, keyword2)
                    index2, dict2 = get_index(fn, stage, keyword2)
                except:
                    continue
                try:
                    get_index(fn, stage, keyword3)
                    index3, dict3 = get_index(fn, stage, keyword3)
                except:
                    continue
                try:
                    get_index(fn, stage, keyword4)
                    index4, dict4 = get_index(fn, stage, keyword4)
                except:
                    continue
                # index1, dict1= get_index(fn, stage, keyword1)
                # index2, dict2= get_index(fn, stage, keyword2)
                # index3, dict3= get_index(fn, stage, keyword3)
                # index4, dict4= get_index(fn, stage, keyword4)
                shared_index = index1
                shared_index = list(sorted(set(shared_index + index2)))
                shared_index = list(sorted(set(shared_index + index3)))
                shared_index = list(sorted(set(shared_index + index4)))
                whole_dict = {'shared_index':shared_index}
                whole_dict.update({keyword1:dict1})
                whole_dict.update({keyword2: dict2})
                whole_dict.update({keyword3: dict3})
                whole_dict.update({keyword4: dict4})
                # should make a dictionary here
                df = pd.DataFrame(whole_dict, index=whole_dict['shared_index'])
                # print(df)
                df.fillna(method='ffill', inplace=True)
                # print(df)
                orders = ['omr_corrected', 'corrected_revised', 'revised_aligned']
                df['omr_corrected'] = (df['omr'] != df['corrected'])
                df['corrected_revised'] = (df['corrected'] != df['revised'])
                df['revised_aligned'] = (df['revised'] != df['aligned'])
                diff = df['omr_corrected'].mean()
                diff2 = df['corrected_revised'].mean()
                diff3 = df['revised_aligned'].mean()
                df2 = df

                df = df.melt(id_vars=['shared_index'], value_vars=orders, var_name='comparison',
                             value_name='changed')
                df = df.astype({'changed': 'float64'})
                sns.relplot(
                    x='shared_index',
                    y='changed',
                    row='comparison',
                    kind='line',
                    height=1.5,
                    aspect=15.0,
                    data=df
                )
                plt.title(fn)
                # plt.show()
                print('comparison', diff, diff2, diff3)
                a_diff1.append(diff * 100)
                a_diff2.append(diff2 * 100)
                a_diff3.append(diff3 * 100)
    print('difference between OMR and CORRECTED:', np.median(a_diff1), '%', '±', np.std(a_diff1), '%', sorted(a_diff1)[0], sorted(a_diff1)[-1])
    print('difference between CORRECTED and REVISED:', np.median(a_diff2), '%', '±', np.std(a_diff2), '%', sorted(a_diff2)[0], sorted(a_diff2)[-1])
    print('difference between REVISED and ALIGNED:', np.median(a_diff3), '%', '±', np.std(a_diff3), '%', sorted(a_diff3)[0], sorted(a_diff3)[-1])
                # df.cc.astype('category').cat.codes
                ############## Output results as chord label integers
                # df = df.melt(id_vars=['shared_index'], var_name='stage', value_name='chord_labels')
                # #
                # print(df)
                # df['code'] = pd.factorize(df['chord_labels'])[0]
                # print(df)
                # plt.figure(figsize=(25, 6))
                # sns.lineplot(x='shared_index', y='code', hue='stage', data=df)
                # plt.show()
                # result1 = f1.read().splitlines()
                # result2 = f2.read().splitlines()
                # number_of_differences = 0
                # if len(result1) != len(result2):
                #     print('-------------------------------------------')
                #     print('dimensions for', fn, 'is different!', 'f1 is', len(result1), 'f2 is', len(result2))
                #     print(AffineNeedlemanWunsch(result1, result2))
                #     break
                #     # s1 = converter.parse(os.path.join(os.getcwd(), 'new_music', 'New_alignment', fn.replace('musi_chord_labels.txt', 'musicxml')))
                #     # s2 = converter.parse(os.path.join(os.getcwd(), 'new_music', 'New_corrected', fn.replace('musi_chord_labels.txt', 'musicxml').replace('revised', 'corrected')))
                #     # s1_chordify = s1.chordify()
                #     # s2_chordify = s2.chordify()
                #     # print('music dimensions for f1 is', len(s1_chordify.recurse().getElementsByClass('Chord')), 'f2 is', len(s2_chordify.recurse().getElementsByClass('Chord')))
                # else:
                #     for id, each_result in enumerate(result1):
                #         if id < len(result2):
                #             if each_result != result2[id]:
                #                 number_of_differences += 1
                #
                # print('% of difference for', fn, 'is:', number_of_differences/len(result1))
                # if len(result1) != len(result2):
                #     print('-------------------------------------------')

def finding_chord_root(chord_name):
    if '#' in chord_name or '-' in chord_name:
        return chord_name[:2]
    else:
        return chord_name[0]


def key_invariant_pairs(each_pair):
        chord_root_1 = finding_chord_root(each_pair[0])
        chord_quality_1 = each_pair[0][len(chord_root_1):]
        if chord_quality_1 == '':
            chord_quality_1 = 'M'
        chord_root_2 = finding_chord_root(each_pair[1])
        chord_quality_2 = each_pair[1][len(chord_root_2):]
        if chord_quality_2 == '':
            chord_quality_2 = 'M'
        a_interval_1 = interval.Interval(noteStart=pitch.Pitch(chord_root_1), noteEnd=pitch.Pitch(chord_root_2))
        number1 = abs(a_interval_1.semitones)
        number2 = abs(a_interval_1.complement.semitones)
        if number1 < number2:
            if '-' in a_interval_1.directedSimpleName:
                return ','.join([chord_quality_2, chord_quality_1, a_interval_1.directedSimpleName.replace('-', '')])
            else:
                return ','.join([chord_quality_1, chord_quality_2, a_interval_1.directedSimpleName])
        else:
            if '-' in a_interval_1.complement.directedSimpleName:
                return ','.join([chord_quality_2, chord_quality_1, a_interval_1.complement.directedSimpleName.replace('-', '')])
            else:
                return ','.join([chord_quality_1, chord_quality_2, a_interval_1.complement.directedSimpleName])


def print_this_plot():
    from matplotlib.ticker import PercentFormatter
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import figure
    plt.rcParams.update({'font.size': 40})
    figure(num=None, figsize=(4, 6), facecolor='w', edgecolor='k')
    counter_fre =  {'M': 0.5113951644867222, 'm': 0.24900911613158938, '7': 0.07520808561236624, 'o': 0.0587594133967499, 'm7': 0.05648038049940547, '/o7': 0.023285770907649623, 'M7': 0.016845025762980578, 'o7': 0.006936187078874356, '+': 0.002080856123662307}
    plt.bar(list(counter_fre.keys()), counter_fre.values(), width=1, color='g')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.ylabel('Percentage (%)')
    plt.xlabel('Chord Qualities')
    # plt.xlabel('Multiple Interpretations')
    plt.xticks(rotation='vertical')
    # plt.figure(figsize=(20, 5))
    plt.show()


def debug():
    unit = ['D7, F#o', 'B,B7', 'B7,B', 'C,Cm7', 'D,DM7', "DM7,D", 'A,A7', 'B, B7', 'A, A7','A7, A', 'F#o, D7']
    for i, each_item in enumerate(unit):
        elements = each_item.split(',')
        for ii, each_chord in enumerate(elements):
            elements[ii] = elements[ii].replace(' ', '')
        unit[i] = ','.join(sorted(elements))
    print(unit)

if __name__ == "__main__":
    # inputpath = os.path.join(os.getcwd(), 'new_music', 'New_later', 'predicted_result')
    # compare_chord_labels(inputpath, 'omr', 'corrected', 'revised', 'aligned')
    # #count_pickup_measure_NO()
    # print_this_plot()
    key_invariant_pairs()