#!/usr/bin/env python
# -*- coding:utf-8 -*-

import user_info
from weiboDB.weiboDB_auth_token import MyMongoDB

def auth_token(access_token,expires,uid):
    result_dic=user_info.check_uid(uid,access_token,expires)
    if result_dic['result_count']==0:
        print("查询user_info表中%s的数量，结果为0.\n’auth_token‘表中插入一个新的document" % uid)
        uuid=uid+"_0"
        print ("uuid   "+uuid)
        mydb=MyMongoDB()

        dic = {"access_token":access_token ,
                "expires":expires,
                "uid":uid,
                "uuid":uuid
                }
        mydb.insert_auth_token(dic)
    elif result_dic['result_count']==1:
        print("查询user_info表中%s的数量，结果为>=1.\n把对应的新纪录修改到‘auth_token’表中" % uid)
        if result_dic['new_uuid']!=None:
            uuid = result_dic['new_uuid']
            print ("new_uuid   " + uuid)
            mydb = MyMongoDB()
            mydb.update_auth_token(uuid,access_token,expires,uid)
        else:
                mydb = MyMongoDB()
                mydb.update_auth_token1(access_token, expires, uid)
