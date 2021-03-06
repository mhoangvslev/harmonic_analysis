'''Train a LSTM on the IMDB sentiment classification task.
The dataset is actually too small for LSTM to be of any advantage
compared to simpler, much faster methods such as TF-IDF+LogReg.
Notes:
- RNNs are tricky. Choice of batch size is important,
choice of loss and optimizer is critical, etc.
Some configurations won't converge.
- LSTM loss decrease patterns during training can be quite different
from what you see with CNNs/MLPs/etc.
GPU command:
    THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python imdb_lstm.py
'''
from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.preprocessing import sequence
from keras.utils import np_utils
#from keras.utils.visualize_util import plot # draw fig
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.datasets import imdb
from scipy.io import loadmat
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
import h5py
import os
import numpy as np
import keras.callbacks as CB
import sys
import string
#import SaveModelLog
def divide_training_data(k, portion, times, trainxo, trainyo, testset = 'Y'):
    placement = int(trainxo.shape[0] / k)
    placement2 = int(trainxo.shape[0] / k)
    valid_x = trainxo[times*placement2:(times+1)*placement2]
    if(times != 9):
        test_x = trainxo[((times+1))*placement2:((times+2))*placement2]
    else:
        test_x = trainxo[((times + 1)%k) * placement2:((times + 2)%k) * placement2]
    if(times*placement!=0):
        if(times != 9):
            train_x = np.vstack((trainxo[:times*placement], trainxo[(times+2)*placement:]))
        else:
            train_x = np.vstack((trainxo[((times+2)%k)*placement2:times*placement2]))
    else:
        train_x = trainxo[((times+2)%k)*placement:]
    valid_y = trainyo[times*placement2:(times+1)*placement2]
    if (times != 9):
        test_y = trainyo[((times + 1)) * placement2:((times + 2)) * placement2]
    else:
        test_y = trainyo[((times+1)%k) * placement2:((times+2)%k) * placement2]
    if(times*placement!=0):
        if (times != 9):
            train_y = np.vstack((trainyo[:times*placement], trainyo[((times+2))*placement:]))
        else:
            train_y = np.vstack((trainyo[((times+2)%k)*placement2:times*placement2]))
    else:
        train_y = trainyo[((times+2)%k)*placement:]
     # we want test set
    train_x = train_x[:int(portion*train_x.shape[0])]
    train_y = train_y[:int(portion * train_y.shape[0])]
    if(testset == "N"):  # We don't want test set
        train_x = np.vstack((train_x, test_x))
        train_y = np.vstack((train_y, test_y))
    print('times' + str(times) + 'valid' + str(valid_x.shape[0]) + 'train' + str(train_x.shape[0]) + 'test' + str(test_x.shape[0]) + 'portion' + str(portion))
    return train_x, train_y, valid_x, valid_y, test_x, test_y
def FineTuneDNN(layer,nodes):
    print('Loading data...')
    #log=open('256LSTM256LSTMNN48lr=0.1dp=0.5.txt','w+')
    #AllData='musicALL7.mat'
    train_xxx = np.loadtxt('train_x.txt')
    train_yyy = np.loadtxt('train_y.txt')
    test_xx = np.loadtxt('test_x.txt')
    test_yy = np.loadtxt('test_y.txt')
    #all_xx = np.loadtxt('all_x.txt')
    #all_yy = np.loadtxt('all_y.txt')
    #np.random.shuffle(all_xx)
    #np.random.shuffle(all_yy)
    '''train_xx = all_xx[:int(len(all_xx)*0.8)]
    valid_xx = all_xx[int(len(all_xx)*0.8):int(len(all_xx)*0.9)]
    test_xx = all_xx[int(len(all_xx)*0.9):]
    train_yy = all_yy[:int(len(all_yy)*0.8)]
    valid_yy = all_yy[int(len(all_yy)*0.8):int(len(all_yy)*0.9)]
    test_yy = all_yy[int(len(all_yy)*0.9):]'''
    #max_features = 20000
    #maxlen = 100  # cut texts after this number of words (among top max_features most common words)
    batch_size = 50
    INPUT_DIM = train_xxx.shape[1]
    OUTPUT_DIM = train_yyy.shape[1]
    HIDDEN_NODE = nodes
    MODEL_NAME = str(layer)+'layer'+str(nodes)+'DNN_no_window'
    K = 10
    cv_log = open('cv_log+' + MODEL_NAME + '.txt', 'w')
    print('Loading data...')
    print('train_xx shape:', train_xxx.shape)
    print('train_yy shape:', train_yyy.shape)
    print('test_xx shape:', test_xx.shape)
    print('test_yy shape:', test_yy.shape)
    print('Build model...')
    cvscores = []
    cvscores_test = []
    for i in range(K):
        train_xx, train_yy, valid_xx, valid_yy = divide_training_data(K, train_xxx, train_yyy, i)
        print('Shape for cross validation...')
        print('train_xx shape:', train_xx.shape)
        print('train_yy shape:', train_yy.shape)
        print('valid_xx shape:', valid_xx.shape)
        print('valid_yy shape:', valid_yy.shape)
        model = Sequential()
        #model.add(Embedding(36, 256, input_length=batch))
        model.add(Dense(HIDDEN_NODE, init='uniform', activation='tanh', input_dim= INPUT_DIM))
        model.add(Dropout(0.2))
        for i in range(layer-1):
        #model.add(LSTM(output_dim=48, init='glorot_uniform', inner_init='orthogonal', activation='softmax', inner_activation='tanh'))  # try using a GRU instead, for fun
        #model.add(LSTM(input_dim=INPUT_DIM, output_dim=500, return_sequences=True, init='glorot_uniform'))
        #model.add(LSTM(output_dim=500, return_sequences=True))
        #model.add(LSTM(output_dim=500, return_sequences=True))
        #model.add(LSTM(48))
            model.add(Dense(HIDDEN_NODE, init='uniform', activation='tanh', input_dim= INPUT_DIM))
            model.add(Dropout(0.2))
        model.add(Dense(OUTPUT_DIM, init='uniform'))
        #model.add(Dropout(0.5)) # dropout does not add at output layer!!
        model.add(Activation('softmax')) # need time distributed softmax??

        # try using different optimizers and different optimizer configs
        #sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
        sgd = SGD(lr=0.1, decay=0.002, momentum=0.5, nesterov=False) # lr = self.lr * (1.0 / (1.0 + self.decay * self.iterations))
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics = ['accuracy'])

        early_stopping =EarlyStopping(monitor='val_acc', patience=1) # set up early stopping
        print("Train...")
        checkpointer = ModelCheckpoint(filepath=MODEL_NAME+".hdf5", verbose=1, save_best_only=True, monitor='val_acc')
        #hist = model.fit(train_xx, train_yy, batch_size=batch_size, nb_epoch=3,validation_split=0.2, shuffle=True, verbose=1, show_accuracy=True, callbacks=[early_stopping])
        hist = model.fit(train_xx, train_yy, batch_size=batch_size, nb_epoch=100, shuffle=True, verbose=1, validation_data=(valid_xx, valid_yy), callbacks=[early_stopping, checkpointer]) # for debug
        #plot(model, to_file='model.png') # draw fig of accuracy
        #score, acc = model.evaluate(valid_xx, valid_yy,
                                   # batch_size=batch_size,
                                   # show_accuracy=True)
        #print('Test score:', score)
        #print('Test accuracy:', acc)
        scores = model.evaluate(valid_xx, valid_yy, verbose=0)
        scores_test = model.evaluate(test_xx, test_yy, verbose=0)
        print(' valid_acc: ', scores[1])
        cvscores.append(scores[1] * 100)
        cvscores_test.append(scores_test[1] * 100)
        #SaveModelLog.Save(MODEL_NAME, hist, model, valid_xx, valid_yy)
    print(np.mean(cvscores), np.std(cvscores))
    print(MODEL_NAME, file=cv_log)
    print('valid:' , np.mean(cvscores) , '%' , '±' , np.std(cvscores) , '%', file=cv_log)
    print('Test:' , np.mean(cvscores_test) , '%' , '±' , np.std(cvscores_test) , '%', file=cv_log)
    #score = model.evaluate(test_xx, test_yy, verbose=0)
    #print('Test loss:', score[0])
    #print('Test accuracy:', score[1])
