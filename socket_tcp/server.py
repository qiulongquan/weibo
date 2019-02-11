# -*- coding: utf-8 -*-

# 导入socket库:
import socket
import time
import threading
import json

def tcplink(sock, addr,i):
    print('线程 %s 产生，开始从 %s 接收数据。' % (i,addr))
    sock.send('线程 %s 服务器开始接收你的数据!' %i)
    while True:
        data = sock.recv(1024)
        # print type(data),data.decode('unicode_escape')
        print type(data), data
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send('线程 %s 你发送来的数据是 %s' % (i,data))
        print ("开始解析获取到的dict文件")
        dict=json.loads(data)
        print type(dict)
        print (dict['token'])
        print (dict['method'])  #method_abc
        # print (dict['parameter'])
        list=dict['parameter']
        print (str(list).decode('unicode_escape'))
        # 转换成string 作为参数代入method_prase方法
        str_token=dict['token']
        str_method=dict['method']
        list_parameter=dict['parameter']
        method_prase(str_token,str_method,list_parameter)
    sock.close()
    print('从%s 线程 %s 断开连接 关闭.' % (addr,i))

def method_prase(str_token,str_method,list_parameter):

    if str_method=='method_abc':
        method_abc(list_parameter)
    elif str_method=='method_1':
        method_1(list_parameter)
    elif str_method=='method_2':
        method_2(list_parameter)
    else :
        print("没有对应的方法可以调用，中止程序。")


def method_abc(list_parameter):
    print ("调用了method_abc方法")
    for str_list in list_parameter:
        print (str_list)
def method_1(list_parameter):
    print ("调用了method_1方法")
    for str_list in list_parameter:
        print (str_list)
def method_2(list_parameter):
    print ("调用了method_2方法")
    for str_list in list_parameter:
        print (str_list)

if __name__ == '__main__':
    # 创建一个socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 监听端口:
    s.bind(('192.168.100.106', 9978))
    # 调用listen()方法开始监听端口，传入的参数指定等待连接的最大数量：
    s.listen(5)
    i=1
    print('Waiting for connection...')
    while True:
        # 接受一个新连接:
        sock, addr = s.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=tcplink, args=(sock, addr,i))
        i=i+1
        t.start()

