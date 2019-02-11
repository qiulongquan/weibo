#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time,datetime

# 计算两个日期相差天数，自定义函数名，和两个日期的变量名。
def Caltime(date1, date2):

    # %Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
    # date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    # date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")

    date1 = time.strptime(date1, "%Y-%m-%d")
    date2 = time.strptime(date2, "%Y-%m-%d")
    # 根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
    # date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    # date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])

    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    # 返回两个变量相差的值，就是相差天数　或者 天数 时间 分钟 秒的差值
    return date2 - date1

# 获取uuid 的脚标 然后+1 并返回new_uuid
def find_substr(str_all):
    substr = '_'
    index1 = str_all.find(substr)
    str1=str_all[:index1]
    str2 = str_all[index1 + 1:]
    print(str1)
    print(str2)
    str2=int(str2)+1
    return str(str1)+"_"+str(str2)

# python实现字符串和日期相互转换的方法
def str_to_date(str_date):
    # # date to str
    # print time.strftime("%Y-%m-%d %X", time.localtime())

    # str to date
    t = time.strptime(str_date, "%Y-%m-%d %H:%M:%S")
    # y, m, d = t[0:3]
    # print y
    # print m
    # print d
    # print datetime.datetime(y, m, d)
    YMD = time.strftime("%Y-%m-%d",t)
    print ("指定的最后更新登录日期的YMD格式 "+YMD)
    return YMD
