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
    "ip":config.config_parse.config_parse('mongodb_user_should_follow','ip'),   #ip
    "port":config.config_parse.config_parse('mongodb_user_should_follow','port'),     #端口
    "db_name" : config.config_parse.config_parse('mongodb_user_should_follow','db_name'),    #数据库名字
    "set_name" : config.config_parse.config_parse('mongodb_user_should_follow','set_name')   #集合名字
}

class MyMongoDB(object):
    def __init__(self):
        try:
            self.conn = MongoClient(settings["ip"], int(settings["port"]))
        except Exception as e:
            print(e)
        self.db = self.conn[settings["db_name"]]
        self.my_set = self.db[settings["set_name"]]

    # ’user_should_follow‘表中插入一个新的document
    def insert_user_should_follow(self,dic_temp):
        print("insert...")
        self.my_set.insert(dic_temp)
        print("insert ok")

    # 根据指定的id 查找DB中是否有这个记录  有返回true 没有返回 false
    def find_id(self,id):
        print("开始查找%s是否在DB中存在"%id)
        count=self.my_set.find({'weibo_id':id}).count()
        print("%s存在的count="%id + str(count))
        return count

    def find_return_result(self,uid):
        result=self.my_set.find({'src_wb_id':uid})
        return result

    # ’user_should_follow‘表中修改指定的document
    def update_user_should_follow(self,dic_temp):
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

    def delete(self, dic):
        print("delete...")
        self.my_set.remove(dic)
        print("删除完成。")

    def update(self, dic,dic1):
        print("update...")
        self.my_set.update(dic,dic1)

    def find_and_remove(self,dic,uid,follow_target):
        print("find...")
        result = self.my_set.find(dic)
        for result1 in result:
            dict_tmp=result1['user_should_follow_list']
            try:
                # if list_tmp.index(int(follow_target))>=0:
                # 如果有符合的条件 就把 follow_target 对象从list_tmp中删掉
                #     index=list_tmp.index(int(follow_target))
                #     del list_tmp[index]
                dict_sub_tmp=dict_tmp[follow_target]
                dict_tmp.pop(follow_target)
                dic1={
                    'src_wb_id':str(uid),
                    'user_should_follow_list':dict_tmp,
                    'total_number':result1['total_number']
                    }
                # 删除掉指定uid的document
                dic2={
                    'src_wb_id':str(uid)
                }
                self.delete(dic2)
                # 插入修改后的新document
                self.insert_user_should_follow(dic1)
                print("user_should_follow表的dict中 %s 已经删除"%follow_target)
                return dict_sub_tmp
            except Exception, e:
                print ("user_should_follow表中不存在指定的follow_target %s ,修改更新操作中止。"%follow_target)

