from music21 import *
import os
c1=['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']
c2=['c','db','d','eb','e','f','gb','g','ab','a','bb','b']
def change_length(pitch_class, transposed_pitch_class, mark):
    """
    if f# changes into b, that means the length of the element changes,
    which should be marked, when f#/c tried to change into b/f
    :param pitch_class:
    :param transposed_pitch_class:
    :param mark:
    :return:
    """
    if((len(pitch_class) not in {1,2}) or (len(transposed_pitch_class) not in {1,2})): # should be assert and exception?
        print("pitch class is not right")
        print("pitch class: " + pitch_class)
        print("transposed pitch class: " + transposed_pitch_class)
        input("???")
    if (len(pitch_class) == len(transposed_pitch_class)):
        mark = 0
    elif (len(pitch_class) < len(transposed_pitch_class)): #1->2
        mark = 1
    elif (len(pitch_class) > len(transposed_pitch_class)): #2->1
        mark = -1
    return mark

def write_back(tmp, i, j, c1, c2, displacement, flag, mark):
    """
    write the transposed value back to the original one
    :param tmp:
    :param i:
    :param j:
    :param c1:
    :param c2:
    :param displacement:
    :param flag:
    :return:
    """
    if(flag == 1): # means not the end of the element, can look ahead to see the accidentials
        if tmp[i][j + mark + 1] == '#' or tmp[i][j + mark + 1] == 'b':
            pitch_class = tmp[i][j + mark:j + mark + 2]
            pitch_class = pitch_class.lower()
            print(pitch_class)
            transposed_pitch_class = transpose(c1, c2, displacement, pitch_class)
            print(transposed_pitch_class)
            tmp[i] = tmp[i][:j + mark] + transposed_pitch_class + tmp[i][j + mark + 2:]
            mark = change_length(pitch_class, transposed_pitch_class, mark) # if the length changes, mark it



        else: # no accidentials, not the end of the string

                if (j >= 1 and tmp[i][j - 1 + mark] == 'b'): # j = 0 still "works", but not in the right way!
                    print('checkout')
                elif(tmp[i][j + mark] == 'b' and tmp[i][j + mark - 1].isalpha()):
                    print('checkout')
                else:

                    pitch_class = letter.lower()
                    print(pitch_class)
                    transposed_pitch_class = transpose(c1, c2, displacement, pitch_class)
                    tmp[i] = tmp[i][:j + mark] + transposed_pitch_class + tmp[i][j + mark + 1:]
                    mark = change_length(pitch_class, transposed_pitch_class, mark)
                    print(transposed_pitch_class)
    elif(flag == 2): # the end of the element, no accidentials

            if j>=1 and tmp[i][j - 1 + mark] == 'b' :
                print('checkout')
            else:
                pitch_class = letter.lower()
                print(pitch_class)
                transposed_pitch_class = transpose(c1, c2, displacement, pitch_class)
                tmp[i] = tmp[i][:j + mark] + transposed_pitch_class + tmp[i][j + mark + 1:]
                mark = change_length(pitch_class, transposed_pitch_class, mark)

                print(transposed_pitch_class)
    return mark
def get_displacement(k):
    """
    Get displacement, which specifies how many steps to move to C major or A minor
    :param k: key class from music 21
    :return: displcement
    """
    ptr = k.name.find(' ')
    key_tonic = k.name[:ptr]
    key_tonic = key_tonic.lower()
    key_tonic = key_tonic.replace('-', 'b')
    #print('key=' + key_tonic)
    if key_tonic in c1:
        #print(c1.index(key_tonic))
        if (k.mode == 'major'):
            displacement = c1.index(key_tonic)
        else:
            displacement = (c1.index(key_tonic) + 3) % len(c1)
    elif key_tonic in c2:
        #print(c2.index(key_tonic))
        if (k.mode == 'major'):
            displacement = c2.index(key_tonic)
        else:
            displacement = (c2.index(key_tonic) + 3) % len(c2)
    else:
        print('pitch class can not be found!')
        input('what do you think about it')
    return displacement


def transpose(c1, c2, displacement, pitch):
    """
    Transpose the target pitch into the one with the key of C
    :param c1: the pitch class array that only has sharp labels
    :param c2: the pitch class array that only has flat labels
    :param displacement: the distance that need to be transposed in order to get the key of C
    :param pitch: the pitch that needs to be transposed
    :return:
    """
    if pitch in c1:
        ptr = c1.index(pitch)
    elif pitch in c2:
        ptr = c2.index(pitch)
    else: # some exceptions
        if(pitch == 'e#'):
            ptr = c1.index('f')
        elif(pitch == 'fb'):
            ptr = c1.index('e')
        elif(pitch == 'b#'):
            ptr = c1.index('c')
        elif(pitch == 'cb'):
            ptr = c1.index('b')
        else:
            print('pitch class still cannot be found')
            input('what do you think about it')
    target = ((ptr - displacement) + len(c1)) % len(c1)
    if pitch in c1:
        return c1[target]
    else:
        return c2[target]
if __name__ == "__main__":
    for file_name in os.listdir('.\\genos-corpus\\answer-sheets\\bach-chorales'):

            if file_name[-3:] == 'pop' or file_name[-3:] == 'not':
                #if(file_name[:3] != '369'):
                    #continue
                ptr = file_name.find('.')
                s = converter.parse(os.getcwd() + '\\midi_files\\original\\' + file_name[:ptr]+'.mid')
                k = s.analyze('key')
                #print('acc ' + str(k.tonic._accidental.alter))
                displacement = get_displacement(k)

                f = open('.\\genos-corpus\\answer-sheets\\bach-chorales\\'+file_name, 'r')
                fnew = open('.\\genos-corpus\\answer-sheets\\bach-chorales\\'+ 'transposed_' + file_name, 'w')
                fexception = open('.\\genos-corpus\\answer-sheets\\bach-chorales\\'+ 'log.txt', 'a+')
                sign = 0 # to see how many files have upper letter!!!!
                for line in f.readlines():
                    #line = line.lower()
                    '''if (line[0].isupper()):
                        if(sign == 0):
                            print(file_name, file = fexception)
                            sign = 1

                        for i, letter in enumerate(line):
                            if(letter.isalpha()):
                                line = line[:i] + letter.lower() + line[i+1:]'''

                    print (line.split(' '))
                    tmp = line.split(' ')
                    for i, ele in enumerate(tmp):
                        mark = 0 # mark incicates whether the length of this chord symbol changes its length
                        for j, letter in enumerate(tmp[i]):
                            if(mark == -1 and letter == 'b'):
                                continue # bb is replaced into something else, the second b is skipped over
                            if letter.lower() in c1:
                                if(tmp[i][-1] != '\\n'): # should be \n, but this does not affect the correctness of the script
                                    if len(tmp[i])>= j + mark + 2:
                                        #print(len(ele))
                                        mark = write_back(tmp, i, j, c1, c2, displacement, 1, mark)
                                    else:
                                        mark = write_back(tmp, i, j, c1, c2, displacement, 2, mark)
                    for ele in tmp: # write the transposed version to the file
                        print(ele, end = '', file = fnew)
                        if(len(ele) != 0):
                            if(ele[-1] != '\n'):
                                print(' ', end='', file=fnew)






