from music21 import *
import os
import sys
format = ['krn']
cwd = '.\\bach-371-chorales-master-kern\\kern\\'
from get_input_and_output import get_chord_line

def put_chord_into_musicXML(string, string1, string2, outputdim, sign):
    """

    :param string:
    :param string1:
    :param string2:
    :return:
    """
    for id, fn in enumerate(os.listdir(cwd)):
        # print(fn)
        if fn[-3:] == 'krn':
            if (os.path.isfile('.\\useful_chord_symbols\\translated_' + fn[4:7] + '.pop''')):
                f = open('.\\useful_chord_symbols\\translated_'+ fn[4:7] + '.pop', 'r')
                fprediction = open('.\\predicted_result\\transposed_predicted_result_'+ fn[4:7] + '.txt', 'r')

            elif (
            os.path.isfile('.\\useful_chord_symbols\\translated_' + fn[4:7] + '.pop.not''')):
                f = open('.\\useful_chord_symbols\\translated_' + fn[4:7] + '.pop.not', 'r')
                fprediction = open('.\\predicted_result\\transposed_predicted_result_' + fn[4:7] + '.txt', 'r')
            else:
                continue  # skip the file which does not have chord labels
            s = converter.parse(cwd + fn)
            print(fn[4:7])
            sChords = s.chordify()
            lineTotal = ''
            lineTotalNoInversion = ''
            for linepre in fprediction.readlines():
                linepre = get_chord_line(linepre, sign)
                lineTotal += linepre
            chordpreTotal = lineTotal.split()
            lineTotal = ''
            for line in f.readlines():
                line = get_chord_line(line, sign)
                lineNoInversion = get_chord_line(line, '0')
                lineTotal += line
                lineTotalNoInversion += lineNoInversion
            chordTotal = lineTotal.split()
            chordTotalNoInversion = lineTotalNoInversion.split()
            s.insert(0, sChords)
            for i, thisChord in enumerate(sChords.recurse().getElementsByClass('Chord')):
                #print(len(chordTotal))
                #print(i)
                if(i < len(chordTotal)):
                    currentChord = chordTotal[i].encode('ansi')  # string to byte
                    #print(currentChord)
                    thisChord.addLyric(currentChord.decode('utf-8'))  # byte to string
                    if(chordTotalNoInversion[i].lower() != chordpreTotal[i].lower()):
                        currentChord = chordpreTotal[i].encode('ansi')  # string to byte
                        thisChord.addLyric(currentChord.decode('utf-8'))  # byte to string
                else:
                    print('error')
                thisChord.closedPosition(forceOctave=4, inPlace=True)
            s.write('musicxml', fp="C:\\Users\\User\\PycharmProjects\\harmonic_analysis\\predicted_result\\" + fn[4:7] + '.xml')
if __name__ == "__main__":
    # Get input features
    #sign = input("do you want inversions or not? 1: yes, 0: no")
    #output_dim =  input('how many kinds of chords do you want to calculate?')
    put_chord_into_musicXML('train', 'valid', 'test', '50', '1')