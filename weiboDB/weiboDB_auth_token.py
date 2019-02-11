#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import pymongo
import config.config_parse
from pymongo import MongoClient
from datetime import date
import datetime


# ip=config_parse.config_parse('mongodb','ip')
# port=config_parse.config_parse('mongodb','port')
# db_name=config_parse.config_parse('mongodb','db_name')
# set_name=config_parse.config_parse('mongodb','set_name')

settings = {
    "ip":config.config_parse.config_parse('mongodb_auth_token','ip'),   #ip
    "port":config.config_parse.config_parse('mongodb_auth_token','port'),     #端口
    "db_name" : config.config_parse.config_parse('mongodb_auth_token','db_name'),    #数据库名字
    "set_name" : config.config_parse.config_parse('mongodb_auth_token','set_name')   #集合名字
}

class MyMongoDB(object):
    def __init__(self):
        try:
            self.conn = MongoClient(settings["ip"], int(settings["port"]))
        except Exception as e:
            print(e)
        self.db = self.conn[settings["db_name"]]
        self.my_set = self.db[settings["set_name"]]

    # ’auth_token‘表中插入一个新的document
    def insert_auth_token(self,dic):
        print("insert...")
        self.my_set.insert(dic)
        print("insert ok")

    # 大于等于90天的修改  把对应的新纪录修改到‘auth_token’表中  修改对象包括 uuid access_token expires uid
    def update_auth_token(self,uuid,access_token,expires,uid):
        # {"count": { $gt: 1}}, { $set: {"test2": "OK"}}
        # 表达式需要分开写，dic1 和 dic2 然后作为参数放入update
        dic1 = {'uid': uid}
        dic2 = {'$set': {'uuid': uuid,'access_token':access_token,'expires':expires}}
        self.my_set.update(dic1, dic2)

    # 小于90天的修改  把对应的新纪录修改到‘auth_token’表中  修改对象包括 access_token expires uid
    def update_auth_token1(self,access_token,expires,uid):
        # {"count": { $gt: 1}}, { $set: {"test2": "OK"}}
        # 表达式需要分开写，dic1 和 dic2 然后作为参数放入update
        dic1 = {'uid': uid}
        dic2 = {'$set': {'access_token':access_token,'expires':expires}}
        self.my_set.update(dic1, dic2)

    # 查找uid 在user_info集合里面是否存在，存在的话再进行flag的比较
    # 如果结果是0 表示还没有登录到user_info集合里面，返回'_0'
    # 如果结果是 >= 1 表示有多次重复登录的情况根据最后登录时间进行排序
    # 然后查看flag的状态 ，根据flag的状态来决定返回的值
    def find_return_uid_result(self,uid):
        print("find...")
        result = self.my_set.find({'id':uid}).count()
        if result==0:
            return '_0'
        elif result>=1:
            flag_check_result=self.flag_check()
            return flag_check_result

    # 检查flag状态，先判断flag  是不是已经过期  0表示正常   9表示过期
    # 如果是0  然后再判断当前系统时间和最后登录时间的差值 大于90天 就更新 flag为9
    # 然后加入一个新的document 连番加1 微博id_1
    def flag_check(self):
        # 未完成的部分
        print("flag_check功能测试中，等待完善代码")
        return '_1'
