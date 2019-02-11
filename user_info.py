#!/usr/bin/env python
# -*- coding:utf-8 -*-

import authorization
import config.config_parse
import datetime
import time
import common_def
from weiboDB.weiboDB_userinfo import MyMongoDB

    # 查找uid 在user_info集合里面是否存在，存在的话再进行flag的比较
    # 如果结果是0 表示还没有登录到user_info集合里面，返回'_0'
    # 如果结果是 >= 1 表示有多次重复登录的情况根据最后登录时间进行排序
    # 然后查看flag的状态 ，根据flag的状态来决定返回的值
def check_uid(uid,access_token,expires):
    mydb=MyMongoDB()
    count=mydb.find_return_uid_count_result(uid)
    if count == 0:
        # 新加入一个document，并插入对象值
        get_user_info_and_insert_0(access_token,uid)
        result_dic = {'result_count': 0}
        return result_dic
    elif count >= 1:
        # resultSet就是现在既存在user_info表中最新的用户信息dic
        resultSet = mydb.return_flag_and_last_login_time(uid)
        new_uuid=flag_and_logic_check(resultSet,uid,access_token,expires)
        result_dic = {'result_count': 1,'new_uuid':new_uuid}
        return result_dic

    # 检查flag状态，先判断flag  是不是已经过期  0表示正常   9表示过期
    # 如果是0  然后再判断当前系统时间和最后登录时间的差值 大于90天 就更新 flag为9
    # 然后加入一个新的document 连番加1 微博id_1
def flag_and_logic_check(resultSet,uid,access_token,expires):
    last_login_time=''
    status_flag=-1
    uuid=0
    for resultSet1 in resultSet:
        print ("user_info表里面根据uid查询最近一个时间 " + str(resultSet1['last_login_time']))
        print ("最新一个document的flag状态 " + str(resultSet1['status_flag']))

        last_login_time=str(resultSet1['last_login_time'])
        status_flag=int(resultSet1['status_flag'])
        uuid = resultSet1['uuid']

    if status_flag==0:
        # 调用日期差值比较方法 check是否差值在90天以内
        # 格式化成2016-03-20 11:45:39形式
        current_time = time.strftime("%Y-%m-%d", time.localtime())
        # python实现字符串和日期相互转换的方法
        last_login_time=common_def.str_to_date(last_login_time)
        result= common_def.Caltime(last_login_time,current_time)
        print ("日期比较时间差值为 "+str(result.days))
        mydb = MyMongoDB()
        if result.days>=90:
            # 日期差值大于等于90修改flag状态为9
            mydb.update_flag_status(uuid)
            # 获取uuid 的脚标 然后+1 并返回
            new_uuid=common_def.find_substr(uuid)
            # 新加入一个document，并插入对象值
            get_user_info_and_insert_1(uid,access_token,expires,new_uuid)
            return new_uuid
        else:
            # 日期差值小于90 修改‘user_info’表中的最后登录时间 （last_login_time）  和 新的token 值
            current_time_YMDYHM = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            mydb.update_last_login_time(uuid,current_time_YMDYHM)
            mydb.update_last_token(uuid, access_token)

    elif status_flag==9:
        # 获取uuid 的脚标 然后+1 并返回
        new_uuid = common_def.find_substr(uuid)
        # 新加入一个document，并插入对象值
        get_user_info_and_insert_1(uid, access_token, expires, new_uuid)
        return new_uuid

            # if flag_check_result==0:
    #     # 微博id在user_info表中是否存在
    #     # 不存在的话 返回 ‘0’
    #     # ’user_info‘表中插入新的数值 同时返回插入值的一个备份dic
    #     dic=get_user_info_and_insert(access_token,uid)
    #     # 将获取的字典dic加入一个flag特征值，值为0
    #     dic['flag_check_result']=0
    #     return dic
    # elif flag_check_result>=1:
    #     return flag_check_result


# uid存在的数量等于0 需要新加入一个doccumnet
def get_user_info_and_insert_0(access_token,uid):
    # 通过http方法来调用API接口，并取得返回值
    # 获取指定的UID用户的信息
    resp_text = authorization._http('GET', 'https://api.weibo.com/2/users/show.json',
                      access_token=access_token,uid=uid)
    r = authorization._parse_json(resp_text)
    # JsonDict型的数据直接用 .key 来提取值

    print ("uid  " + str(r.id))
    print ("screen_name  " + r.screen_name.encode('unicode-escape').decode('string_escape').decode('unicode_escape'))
    # 将获取的数据写入到数据库中
    mydb = MyMongoDB()
    dic = {"id": str(r.id),
            "last_login_time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "token":access_token,
            "screen_name": r.screen_name.encode('unicode-escape').decode('string_escape').decode('unicode_escape'),
            "logout_flag":'false',
           # 这个地方需要修改 不能默认写入'_0' 需要判断条件
            "uuid":str(r.id)+'_0',
            "status_flag":'0'
           }
    mydb.insert_user_info(dic)
    return dic

# uid存在的数量大于等于1 需要新加入一个doccumnet
def get_user_info_and_insert_1(uid,access_token,expires,new_uuid):
    # 通过http方法来调用API接口，并取得返回值
    # 获取指定的UID用户的信息
    resp_text = authorization._http('GET', 'https://api.weibo.com/2/users/show.json',
                      access_token=access_token,uid=uid)
    r = authorization._parse_json(resp_text)
    # JsonDict型的数据直接用 .key 来提取值

    print ("uid  " + str(r.id))
    print ("screen_name  " + r.screen_name.encode('unicode-escape').decode('string_escape').decode('unicode_escape'))
    # 将获取的数据写入到数据库中
    mydb = MyMongoDB()
    dic = {"id": str(r.id),
            "last_login_time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "token":access_token,
            "screen_name": r.screen_name.encode('unicode-escape').decode('string_escape').decode('unicode_escape'),
            "logout_flag":'false',
           # 这个地方需要修改 不能默认写入'_0' 需要判断条件
            "uuid":new_uuid,
            "status_flag":'0'
           }
    mydb.insert_user_info(dic)

    # 也可以用  .get 方法来获取值  r.get('remind_in', None)
    # remind_in = r.get('remind_in', None)