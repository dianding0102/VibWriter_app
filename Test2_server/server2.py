# -*- coding:utf8 -*-
import socket
import sys
import time
import os
import VibPreprocess
import VibWriter

HOST = '192.168.31.130'  # Symbolic name, meaning all available interfaces
PORT = 9000  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print ('Socket bind complete')

# while True: # 循环接收
# Start listening on socket
s.listen(10)
print ('Socket now listening')

# new file
file_ = str(time.time())
file_name = 'data/test' + file_ + '/test' + file_ + '.txt'
os.makedirs('data/test' + file_)
f = open(file_name, 'a')
print ('==================')
print ('saving to ' + file_name)
print ('==================')

# 单个字母
# while True:
#     # wait to accept a connection - blocking call
#     conn, addr = s.accept()
#     print 'Connected with ' + addr[0] + ':' + str(addr[1])
#
#     while True:
#         data = conn.recv(1024)
#         f.write(data)
#         #print data
#         if data.find('end') != -1:
#             break
#     print 'Transform done'
#     break


# input recognition

# send back the letter
# 单个字母
FlagSend = False
while True:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print ('Connected with ' + addr[0] + ':' + str(addr[1]))
    #s.connect()
    while True:
        data = conn.recv(1024)
        f.write(str(data))
        #print data
        if data.find('end'.encode()) != -1:
            break
    print ('Receive done')
    FlagSend = True
    if FlagSend:
        # 震动数据处理
        print ('==================')
        print ('Convertint to pictures...')
        num_letter = VibPreprocess.VibPreprocess(file_name)
        print ('Num of letters: ' + str(num_letter))
        print ('==================')
        # 手写识别
        print ('==================')
        print ('Recgonize the letters...')
        print ('==================')
        letters = VibWriter.vibwriter(file_name, num_letter)
        # print (letters)
        # # 单词建议
        # print ('==================')
        # print ('Word Suggestion...')
        # print ('==================')

        # 结果发送
        conn.send((letters + '\n').encode())
        print ('Send result')
        FlagSend = False
    conn.close()
    break
#close
s.close()
