# -*- coding: UTF-8 -*-
from __future__ import print_function
from config import config
import cv2
import os, time
from keras.preprocessing.image import img_to_array
import numpy as np
from Build_model import Build_model

class PREDICT(Build_model):
    def __init__(self, config, pic_name):
        Build_model.__init__(self, config)
        self.pic_name = pic_name

    def classes_id(self):
        with open('train_class_idx.txt', 'r') as f:
            lines = f.readlines()
            lines = [line.rstrip() for line in lines]
        return lines

    def mkdir(self, path):
        if os.path.exists(path):
            return path
        os.mkdir(path)
        return path

    def Predict(self):
        model = Build_model(self.config).build_model()
        model.load_weights(os.path.join(os.path.join(self.checkpoints, self.model_name), self.model_name+'_transfer.h5'))

        img_ = cv2.resize(cv2.imread(self.pic_name), (self.normal_size, self.normal_size))
        img = np.array([img_to_array(img_)], dtype='float')/255.0
        pred = model.predict(img).tolist()[0]
        label = self.classes_id()[pred.index(max(pred))]
        confidence = max(pred)

        print('predict label     is: ', label)
        print('predict confidect is: ', confidence)
        return label


def vibwriter(file_name, num_letters):
    letters = ''
    for i in range(num_letters):
        pic_name = file_name[:-4] + '_letter_' + str(i) + '.png'
        predict = PREDICT(config, pic_name)
        letters = letters + predict.Predict()
    return letters

# file_name = 'data/test1616572601.39/test1616572601.39.txt'
# num_letters = 1
# vibwriter(file_name, num_letters)



