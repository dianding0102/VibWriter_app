# -*- coding:utf8 -*-
import socket
import sys
import time


HOST = '192.168.31.130'  # Symbolic name, meaning all available interfaces
PORT = 9004  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

while True: # 循环接收
    # Start listening on socket
    s.listen(10)
    print 'Socket now listening'

    # new file
    file_name = 'test' + str(time.time())
    f = open(file_name + '.txt', 'a')
    print '=================='
    print 'saving to ' + file_name
    print '=================='

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
    while True:
        # wait to accept a connection - blocking call
        # conn, addr = s.accept()
        # print 'Connected with ' + addr[0] + ':' + str(addr[1])
        s.connect()
        s.send('a')
        print 'Send result'


#close
#s.close()
