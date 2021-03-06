#!/usr/bin/env python
# -*- coding:utf-8 -*-

import config.config_parse
from pymongo import MongoClient
import time

# ip=config_parse.config_parse('mongodb','ip')
# port=config_parse.config_parse('mongodb','port')
# db_name=config_parse.config_parse('mongodb','db_name')
# set_name=config_parse.config_parse('mongodb','set_name')

settings = {
    "ip":config.config_parse.config_parse('mongodb_user_recently_followed','ip'),   #ip
    "port":config.config_parse.config_parse('mongodb_user_recently_followed','port'),     #端口
    "db_name" : config.config_parse.config_parse('mongodb_user_recently_followed','db_name'),    #数据库名字
    "set_name" : config.config_parse.config_parse('mongodb_user_recently_followed','set_name')   #集合名字
}

class MyMongoDB_urf(object):
    def __init__(self):
        try:
            self.conn = MongoClient(settings["ip"], int(settings["port"]))
        except Exception as e:
            print(e)
        self.db = self.conn[settings["db_name"]]
        self.my_set = self.db[settings["set_name"]]

    def find_id(self,uid):
        print("开始查找%s是否在DB中存在"%uid)
        count=self.my_set.find({'src_wb_id':uid}).count()
        print("%s存在的count="%uid + str(count))
        return count

    # ’user_recently_followed‘表中插入一个新的document
    def insert_to_DB(self,dic_temp):
        print("insert...")
        self.my_set.insert(dic_temp)
        print("insert ok")

    def delete_uid(self, src_wb_id):
        dic = {'src_wb_id': str(src_wb_id)}
        print("delete...")
        self.my_set.remove(dic)
        print("删除完成。")

    # 获取用户最近关注列表（粉丝列表 已关注）user_recently_followed表中指定uid的关注数量
    def recently_followed_count(self,uid):
        result = self.my_set.find({'src_wb_id': uid})
        for result1 in result:
            count=len(result1['user_recently_followed_list'])
            return count

    def insert_user_to_user_recently_followed(self,uid,follow_target,dict_sub_tmp):
        if self.find_id(uid)==0:
            print ("用户最近关注列表（粉丝列表 已关注）中不存在指定的uid，新建uid操作")
            # list=[]
            # list.append(follow_target)
            # 关注时间赋值 当前系统时间
            if dict_sub_tmp is None:
                dict_sub_tmp= {
                    'tgt_wb_id': follow_target,
                    'follow_date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    'latest_message_release_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                }
            else:
                dict_sub_tmp['follow_date']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            user_recently_followed_list={}
            user_recently_followed_list[follow_target]=dict_sub_tmp
            dic={
                'src_wb_id':uid,
                'user_recently_followed_list':user_recently_followed_list,
                'last_act_time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
            self.insert_to_DB(dic)

        elif self.find_id(uid)>=1:
            print ("用户最近关注列表（粉丝列表 已关注）中存在指定的uid，更新uid的粉丝列表操作")
            dict_tmp={}
            result=self.my_set.find({'src_wb_id': uid})
            for result1 in result:
                dict_tmp=result1['user_recently_followed_list']

            # 查看指定要插入的元素是否已经在dict_tmp中，不存在就插入 存在就不插入
            if follow_target not in dict_tmp.keys():
                dict_sub_tmp1 = {
                    'tgt_wb_id': follow_target,
                    'follow_date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    'latest_message_release_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                }
                dict_tmp[follow_target]=dict_sub_tmp1

                dic = {
                    'src_wb_id': uid,
                    'user_recently_followed_list': dict_tmp,
                    'last_act_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                }
                # 先删除掉uid指定的文档
                self.delete_uid(uid)
                # 然后把新的文档写入DB
                self.insert_to_DB(dic)
                # 获取用户最近关注列表（粉丝列表 已关注）user_recently_followed中指定uid的关注数量
                print self.recently_followed_count(uid)
            else:
                print ("dict_tmp中已经包含要插入的元素%s,中止插入操作。"%follow_target)



