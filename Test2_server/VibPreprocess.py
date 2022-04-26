# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from PIL import Image
from skimage import img_as_ubyte

def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range

def VibPreprocess(file_name):

    time = []
    acc_x = []
    acc_y = []
    acc_z = []

    f = open(file_name)
    #raw_data = str(f.readlines()).split('\\n')
    raw_data = f.readlines()
    #print(len(raw_data))
    for i in range(int(len(raw_data)/4)*4):
        raw_data_ = raw_data[i]
        # for j in range(5):
        #     if raw_data_[j].isdigit():
        #         raw_data_ = raw_data_[j:-1]
        #         break
        #print(raw_data_)
        if i % 4 == 0:
            time.append(int(raw_data_[:-1]))
        elif i % 4 == 1:
            acc_x.append(float(raw_data_[:-1]))
        elif i % 4 == 2:
            acc_y.append(float(raw_data_[:-1]))
        elif i % 4 == 3:
            acc_z.append(float(raw_data_[:-1]))
    #print(len(acc_x))

    begin_time = time[0]
    delete_time = []
    for i in range(len(time)):
        time[i] = time[i] - begin_time
        # 删除重复时间
        if time[i] == time[i-1]:
            delete_time.append(i)
            #print('...')
        #print(time[i])
    time = np.delete(time, delete_time)
    acc_x = np.delete(acc_x, delete_time)
    acc_y = np.delete(acc_y, delete_time)
    acc_z = np.delete(acc_z, delete_time)

    # plot data
    plt.figure(figsize=(6, 9))
    plt.subplot(411)
    plt.plot(range(len(acc_x)), time)
    plt.subplot(412)
    plt.plot(range(len(acc_x)), acc_x)
    plt.subplot(413)
    plt.plot(range(len(acc_x)), acc_y)
    plt.subplot(414)
    plt.plot(range(len(acc_x)), acc_z)
    plt.show()

    # letter segments
    # 插值
    acc_x_1k = np.interp(range(time[-1]+1), time, acc_x)
    acc_y_1k = np.interp(range(time[-1]+1), time, acc_y)
    acc_z_1k = np.interp(range(time[-1]+1), time, acc_z)
    acc_x_1k = acc_x_1k - np.mean(acc_x_1k)
    acc_y_1k = acc_y_1k - np.mean(acc_y_1k)
    acc_z_1k = acc_z_1k - np.mean(acc_z_1k)
    # segment
    segment_time = []
    threshold_z = 0.3 * max(acc_z_1k)
    for i in range(len(acc_z_1k)):
        if acc_z_1k[i] > threshold_z:
            segment_time.append(i)
    segment_time_ = segment_time[0]
    segment_time2 = [segment_time_]
    for i in range(len(segment_time)):
        if segment_time[i] > segment_time_ + 750:
            segment_time2.append(segment_time[i])
            segment_time_ = segment_time[i]

    plt.figure(figsize=(9, 6))
    plt.plot(range(len(acc_z_1k)), acc_z_1k)
    plt.plot(segment_time2, acc_z_1k[segment_time2], 'ro')
    plt.show()
    # 频谱图
    for i in range(len(segment_time2)):
        if segment_time2[i] > len(acc_z_1k) - 1000 | segment_time2[i] < 500:
            break
        letter_x = np.array(acc_x_1k[segment_time2[i]-500:segment_time2[i]+1000])
        f, t, S_x = signal.spectrogram(letter_x, window=('hamming'), nperseg=128, fs=1000, noverlap=120, nfft=128, mode='psd')
        letter_y = np.array(acc_y_1k[segment_time2[i]-500:segment_time2[i]+1000])
        f, t, S_y = signal.spectrogram(letter_y, window=('hamming'), nperseg=128, fs=1000, noverlap=120, nfft=128, mode='psd')
        letter_z = np.array(acc_z_1k[segment_time2[i]-500:segment_time2[i]+1000])
        f, t, S_z = signal.spectrogram(letter_z, window=('hamming'), nperseg=128, fs=1000, noverlap=120, nfft=128, mode='psd')

        # plt.pcolormesh(t, f, S_x_n)
        # plt.ylabel('Frequency [Hz]')
        # plt.xlabel('Time [sec]')
        # plt.show()
        #
        # plt.pcolormesh(t, f, S_y_n)
        # plt.ylabel('Frequency [Hz]')
        # plt.xlabel('Time [sec]')
        # plt.show()
        #
        # plt.pcolormesh(t, f, S_z_n)
        # plt.ylabel('Frequency [Hz]')
        # plt.xlabel('Time [sec]')
        # plt.show()

        # 归一化
        S_x_n = normalization(S_x)
        S_y_n = normalization(S_y)
        S_z_n = normalization(S_z)

        # 生成图片
        S_ = np.dstack((S_x_n, S_y_n, S_z_n))
        S_image = Image.fromarray(img_as_ubyte(S_)).convert("RGB")
        pic_name = file_name[:-4] + '_letter_' + str(i) + '.png'
        S_image.save(pic_name)
    return len(segment_time2)

#file_name = 'data/test1616569907.78/test1616569907.78.txt'
#pic_name = VibPreprocess(file_name)