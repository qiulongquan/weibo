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
    "ip":config.config_parse.config_parse('mongodb_userinfo','ip'),   #ip
    "port":config.config_parse.config_parse('mongodb_userinfo','port'),     #端口
    "db_name" : config.config_parse.config_parse('mongodb_userinfo','db_name'),    #数据库名字
    "set_name" : config.config_parse.config_parse('mongodb_userinfo','set_name')   #集合名字
}

class MyMongoDB(object):
    def __init__(self):
        try:
            self.conn = MongoClient(settings["ip"], int(settings["port"]))
        except Exception as e:
            print(e)
        self.db = self.conn[settings["db_name"]]
        self.my_set = self.db[settings["set_name"]]

    def insert_user_info(self,dic):
        print("insert...")
        self.my_set.insert(dic)
        print("insert ok")

    # 返回指定uid在userinfo表中的数量 判断是否大于0用  或大于等于1用
    def find_return_uid_count_result(self,uid):
        print("find...")
        result_count = self.my_set.find({'id':uid}).count()
        return result_count

    # 返回最近一个document的时间和flag状态
    def return_flag_and_last_login_time(self,uid):
        resultSet = self.my_set.find({'id': uid}).sort([('last_login_time', -1)]).limit(1)
        return resultSet

    # 返回screen_name的值
    def return_screen_name(self,uid):
        print

    # 修改flag的状态为9
    def update_flag_status(self,uuid):
        # {"count": { $gt: 1}}, { $set: {"test2": "OK"}}
        # 表达式需要分开写，dic1 和 dic2 然后作为参数放入update
        dic1 = {'uuid': uuid}
        dic2 = {'$set': {'status_flag': "9"}}
        self.my_set.update(dic1, dic2)

    # 更新userinfo表里面指定uuid的最后登录时间
    def update_last_login_time(self,uuid,last_login_time):
        # {"count": { $gt: 1}}, { $set: {"test2": "OK"}}
        # 表达式需要分开写，dic1 和 dic2 然后作为参数放入update
        dic1 = {'uuid': uuid}
        dic2 = {'$set': {'last_login_time': last_login_time}}
        self.my_set.update(dic1, dic2)

    # 更新userinfo表里面指定uuid的最新的token
    def update_last_token(self,uuid,access_token):
        # {"count": { $gt: 1}}, { $set: {"test2": "OK"}}
        # 表达式需要分开写，dic1 和 dic2 然后作为参数放入update
        dic1 = {'uuid': uuid}
        dic2 = {'$set': {'token': access_token}}
        self.my_set.update(dic1, dic2)