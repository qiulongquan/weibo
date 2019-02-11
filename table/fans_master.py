#!/usr/bin/env python
# -*- coding:utf-8 -*-

from weiboDB.weiboDB_fans_master import MyMongoDB
import authorization

def insert_fans_master_info(access_token,uid):
    # 通过http方法来调用API接口，并取得返回值
    # 获取用户的关注列表
    resp_text = authorization._http('GET', 'https://api.weibo.com/2/friendships/friends.json',
                                    access_token=access_token,uid=uid)
    print resp_text
    r = authorization._parse_json(resp_text)
    # JsonDict型的数据直接用 .key 来提取值

    print ("获取用户的关注列表 list的长度  "+str(len(r.users)))
    print ("获取用户的关注列表 total_number  " + str(r.total_number))
    db_operate(r.users)
    print("获取用户的关注列表 操作完成")

    # 获取用户的粉丝列表
    resp_text = authorization._http('GET', 'https://api.weibo.com/2/friendships/followers.json',
                                    access_token=access_token,uid=uid)
    print resp_text
    r = authorization._parse_json(resp_text)
    # JsonDict型的数据直接用 .key 来提取值

    print ("获取用户的粉丝列表 list的长度  "+str(len(r.users)))
    print ("获取用户的粉丝列表 total_number  " + str(r.total_number))
    db_operate(r.users)
    print("获取用户的粉丝列表 操作完成")

def db_operate(users):
    mydb = MyMongoDB()
    i = 0
    for str_user in users:
        i=i+1
        print ("第%s个user用户名：%s"%(str(i),str_user['screen_name'].encode("utf-8")))

        dic={'weibo_id':str_user['id'],
             'screen_name':str_user['screen_name'],
             'description':str_user['description'],
             'profile_image_url':str_user['profile_image_url'],
             'avatar_large':str_user['avatar_large'],
             'profile_url': str_user['profile_url'],
             'followers_count': str_user['followers_count'],
             'friends_count': str_user['friends_count'],
             'statuses_count': str_user['statuses_count'],
             'favourites_count': str_user['favourites_count'],
             'follow_me': str_user['follow_me'],
             'recent_flag': 'false'
        }

        if mydb.find_id(str_user['id']) == 0:
            # 将unicode和中文同时显示使用的方法加入 .encode("utf-8")
            # print ("第一个参数" + str_text['screen_name'].encode("utf-8"))
            # print ("screen_name  " + r.screen_name.encode('unicode-escape').decode('string_escape').decode('unicode_escape'))
            # 将获取的数据写入到数据库中
            mydb.insert_fans_master(dic)
        elif mydb.find_id(str_user['id'])>=1:
            mydb.update_fans_master(dic)