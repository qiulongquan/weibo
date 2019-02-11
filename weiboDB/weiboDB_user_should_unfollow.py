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
    "ip":config.config_parse.config_parse('mongodb_user_should_unfollow','ip'),   #ip
    "port":config.config_parse.config_parse('mongodb_user_should_unfollow','port'),     #端口
    "db_name" : config.config_parse.config_parse('mongodb_user_should_unfollow','db_name'),    #数据库名字
    "set_name" : config.config_parse.config_parse('mongodb_user_should_unfollow','set_name')   #集合名字
}

class MyMongoDB(object):
    def __init__(self):
        try:
            self.conn = MongoClient(settings["ip"], int(settings["port"]))
        except Exception as e:
            print(e)
        self.db = self.conn[settings["db_name"]]
        self.my_set = self.db[settings["set_name"]]

    # 根据指定的id 查找DB中是否有这个记录  有返回true 没有返回 false
    def find_id(self,id):
        print("开始查找%s是否在DB中存在"%id)
        count=self.my_set.find({'weibo_id':id}).count()
        print("%s存在的count="%id + str(count))
        return count

    def find_return_result(self,uid):
        result=self.my_set.find({'src_wb_id':uid})
        return result

    #  user_should_unfollow表中插入一个新的document
    def insert_user_should_unfollow(self,dic_temp):
        print("insert...")
        self.my_set.insert(dic_temp)
        print("insert ok")

    def delete_src_should_unfollow_list(self,dic_temp):
        print("delete...")
        self.my_set.remove(dic_temp)
        print("删除完成。")

    def find_and_remove(self,dic,uid,unfollow_target):
        print("find...")
        result = self.my_set.find(dic)
        for result1 in result:
            dict_tmp=result1['should_unfollow_user_list']
            try:
                # if dict_tmp.index(int(unfollow_target))>=0:
                # # 如果有符合的条件 就把 unfollow_target 对象从list_tmp中删掉
                #     index=list_tmp.index(int(unfollow_target))
                #     del list_tmp[index]
                dict_sub_tmp = dict_tmp[unfollow_target]
                dict_tmp.pop(unfollow_target)
                dic1 = {
                    'src_wb_id': str(uid),
                    'should_unfollow_user_list': dict_tmp,
                    'total_number': result1['total_number']
                }
                # 删除掉指定uid的document
                dic2={
                    'src_wb_id':str(uid)
                }
                self.delete_src_should_unfollow_list(dic2)
                # 插入修改后的新document
                self.insert_user_should_unfollow(dic1)
                print("user_should_unfollow表的list中 %s 已经删除"%unfollow_target)
                return dict_sub_tmp
            except Exception, e:
                print ("user_should_unfollow表中不存在指定的unfollow_target %s ,修改更新操作中止。"%unfollow_target)

