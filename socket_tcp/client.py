# -*- coding: utf-8 -*-

# 导入socket库:
import socket
import random
import json

if __name__ == '__main__':
    # 创建一个socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接:
    s.connect(('192.168.8.1', 9978))
    # 接收欢迎消息:
    print(s.recv(1024).decode('utf-8'))
    i=0
    break_flag=0
    while True:
        dict={
            'token':'2.00JDmx9C0PwxRR143cc743bd_ffgZB',
            'method':'method_abc',
            'parameter':'a,b,cd,efg,123,中文汉字'
        }
        encode_json_dict = json.dumps(dict)   #<type 'str'>  把dict转换成string 进行传输
        print encode_json_dict.decode('unicode_escape')
        # 发送数据:
        s.send(encode_json_dict)   #发送的send方法支持 string 和 buffer
        print(s.recv(1024).decode('utf-8'))
        break_flag=1
        if break_flag==1:
            break
    s.send(b'exit')
    s.close()