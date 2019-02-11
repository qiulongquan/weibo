#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 用户待取消关注列表(用户关注列表)
# 处理逻辑
# 调用API接口获取最新用户待取消关注列表 然后和当前待取消关注列表进行对比，
# 当前列表少的uid 表明已近被删掉，本地列表也删掉并加入到用户最近取消关注列表 （user_recently_unfollowed）

import authorization
import time
from weiboDB.weiboDB_user_should_unfollow import MyMongoDB
from weiboDB.weiboDB_user_recently_unfollowed import MyMongoDB_urunf

# 用户待取消关注列表(用户关注列表) API数据获取 写入调用操作
def insert_user_should_unfollow(access_token,src_wb_id):
    resp_text = authorization._http('GET', 'https://api.weibo.com/2/friendships/friends/ids.json',
                                    access_token=access_token, uid=src_wb_id)
    print resp_text
    r = authorization._parse_json(resp_text)
    # JsonDict型的数据直接用 .key 来提取值

    print ("获取用户待取消关注列表(用户关注列表) list的长度  " + str(len(r.ids)))
    print ("获取用户待取消关注列表(用户关注列表) total_number  " + str(r.total_number))
    db_operate(r.ids,r.total_number,src_wb_id)
    print("获取用户待取消关注列表(用户关注列表) 操作完成")

def get_return_info(access_token,src_wb_id):
    resp_text = authorization._http('GET', 'https://api.weibo.com/2/friendships/friends/ids.json',
                                    access_token=access_token, uid=src_wb_id)
    print resp_text
    r = authorization._parse_json(resp_text)
    # JsonDict型的数据直接用 .key 来提取值

    print ("获取用户待关注列表 list的长度  " + str(len(r.ids)))
    print ("获取用户待关注列表 total_number  " + str(r.total_number))
    return r

def db_operate(should_unfollow_user_list,total_number,src_wb_id):
    mydb = MyMongoDB()
    dic = {}
    dic_sub_1 = {}
    dic['src_wb_id'] = str(src_wb_id)
    for should_unfollow_user_list1 in should_unfollow_user_list:
        dic_sub_2 = {}
        dic_sub_2['tgt_wb_id'] = should_unfollow_user_list1
        dic_sub_2['unfollow_date'] = ''
        dic_sub_2['latest_message_release_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dic_sub_1[str(should_unfollow_user_list1)] = dic_sub_2

    dic['should_unfollow_user_list'] = dic_sub_1
    # 所有的粉丝id 加入dic后，退出循环，最后加入total_number
    dic['total_number'] = total_number
    # 将获取的数据写入到数据库中
    mydb.insert_user_should_unfollow(dic)

# 获取指定uid用户的  用户待取消关注列表(用户关注列表)user_should_unfollow表中的粉丝数量
def actual_insert_user_count(src_wb_id):
    mydb = MyMongoDB()
    result = mydb.find_return_result(str(src_wb_id))
    count=0
    for result1 in result:
        count=len(result1['should_unfollow_user_list'])
    return count

# 用户滑屏刷新页面操作
def refresh(access_token,src_wb_id):
    r=get_return_info(access_token,src_wb_id)
    # 删除掉src_wb_id的待关注用户信息，然后把新获取内容写入
    delete_src_should_unfollow_list(src_wb_id)
    print("删除%s记录完成"%src_wb_id)
    # 获取到的新数据 写入数据库操作方法
    db_operate(r.ids, r.total_number, src_wb_id)
    print("用户待关注列表刷新操作完成")

def delete_src_should_unfollow_list(src_wb_id):
    mydb=MyMongoDB()
    dic={'src_wb_id':str(src_wb_id)}
    mydb.delete_src_should_unfollow_list(dic)

# 用户取消关注一个粉丝用户操作
# 用户取消关注一个粉丝用户后 调用user_should_unfollow的逻辑处理 从user_should_unfollow表中删掉待取消关注的粉丝
# 同时user_recently_unfollowed 增加刚才取消关注的粉丝uid
def remove_one_follow(access_token,uid,unfollow_target):
    dic={'src_wb_id':str(uid)}
    mydb=MyMongoDB()
    mydb_urunf=MyMongoDB_urunf()
    # 从用户待取消关注列表(用户关注列表)中删除unfollow_target
    dict_sub_tmp=mydb.find_and_remove(dic,uid,unfollow_target)
    # 当前指定uid用户的  用户待关注列表(粉丝列表)表中的粉丝数量
    print ("当前指定uid %s用户的  用户待关注列表(粉丝列表)表中的粉丝数量%s" %(str(uid),str(actual_insert_user_count(uid))))
    # 将删除的follow_target加入到用户最近关注列表（粉丝列表 已关注）user_recently_followed中
    mydb_urunf.insert_user_to_user_recently_unfollowed(str(uid),unfollow_target,dict_sub_tmp)