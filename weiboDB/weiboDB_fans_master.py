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
    "ip":config.config_parse.config_parse('mongodb_fans_master','ip'),   #ip
    "port":config.config_parse.config_parse('mongodb_fans_master','port'),     #端口
    "db_name" : config.config_parse.config_parse('mongodb_fans_master','db_name'),    #数据库名字
    "set_name" : config.config_parse.config_parse('mongodb_fans_master','set_name')   #集合名字
}

class MyMongoDB(object):
    def __init__(self):
        try:
            self.conn = MongoClient(settings["ip"], int(settings["port"]))
        except Exception as e:
            print(e)
        self.db = self.conn[settings["db_name"]]
        self.my_set = self.db[settings["set_name"]]

    # ’fans_master‘表中插入一个新的document
    def insert_fans_master(self,dic_temp):
        print("insert...")
        self.my_set.insert(dic_temp)
        print("insert ok")

    # 根据指定的id 查找DB中是否有这个记录  有返回true 没有返回 false
    def find_id(self,id):
        print("开始查找%s是否在DB中存在"%id)
        count=self.my_set.find({'weibo_id':id}).count()
        print("%s存在的count="%id + str(count))
        return count

    # ’fans_master‘表中修改指定的document
    def update_fans_master(self,dic_temp):
        print("update...")
        # {"count": { $gt: 1}}, { $set: {"test2": "OK"}}
        # 表达式需要分开写，dic1 和 dic2 然后作为参数放入update
        dic1 = {'weibo_id': dic_temp['weibo_id']}
        dic2 = {'$set': {'avatar_large': dic_temp['avatar_large'],
                         'statuses_count':dic_temp['statuses_count'],
                         'description': dic_temp['description'],
                         'friends_count': dic_temp['friends_count'],
                         'profile_image_url': dic_temp['profile_image_url'],
                         'favourites_count': dic_temp['favourites_count'],
                         'screen_name': dic_temp['screen_name'],
                         'follow_me': dic_temp['follow_me'],
                         'followers_count': dic_temp['followers_count'],
                         'recent_flag': dic_temp['recent_flag'],
                         'profile_url': dic_temp['profile_url']
                         }
                }
        self.my_set.update(dic1, dic2)

