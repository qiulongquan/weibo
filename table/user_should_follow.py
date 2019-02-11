#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 处理逻辑
# 调用API接口获取最新待关注列表
# 然后和当前待关注列表进行对比，
#
# 用户滑屏刷新页面操作
# 客户刷新操作先从微博服务器获取最新的粉丝列表
# 然后和程序服务器进行对比，程序服务器少的uid进行增加操作
# 程序服务器多的uid删除操作
#
# 用户关注一个粉丝用户操作
# 用户关注一个粉丝用户后调用user_should_follow的逻辑处理
# 从user_should_follow表中删掉关注的粉丝
# 同时user_recently_followed增加刚才关注的粉丝uid

import authorization
import time
from weiboDB.weiboDB_user_should_follow import MyMongoDB
from weiboDB.weiboDB_user_recently_followed import MyMongoDB_urf

# 用户待关注列表(粉丝列表)  API数据获取 写入调用操作
def insert_user_should_follow(access_token,src_wb_id):
    # 调用获取最新待关注列表方法
    r=get_return_info(access_token,src_wb_id)
    # 写入数据库操作方法
    db_operate(r.ids,r.total_number,src_wb_id)
    print("获取用户待关注列表 操作完成")

def get_return_info(access_token,src_wb_id):
    resp_text = authorization._http('GET', 'https://api.weibo.com/2/friendships/followers/ids.json',
                                    access_token=access_token, uid=src_wb_id)
    print resp_text
    r = authorization._parse_json(resp_text)
    # JsonDict型的数据直接用 .key 来提取值

    print ("获取用户待关注列表 list的长度  " + str(len(r.ids)))
    print ("获取用户待关注列表 total_number  " + str(r.total_number))
    return r

def db_operate(should_follow_user_list,total_number,src_wb_id):
    mydb = MyMongoDB()
    dic={}
    dic_sub_1={}
    dic['src_wb_id'] = str(src_wb_id)
    for should_follow_user_list1 in should_follow_user_list:
        dic_sub_2 = {}
        dic_sub_2['tgt_wb_id']=should_follow_user_list1
        dic_sub_2['follow_date']=''
        dic_sub_2['latest_message_release_time']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dic_sub_1[str(should_follow_user_list1)]=dic_sub_2

    dic['user_should_follow_list'] = dic_sub_1
    # 所有的粉丝id 加入dic后，退出循环，最后加入total_number
    dic['total_number']=total_number
    # 将获取的数据写入到数据库中
    mydb.insert_user_should_follow(dic)


# 读取指定uid对应的文档中的 待关注的粉丝列表内容
def return_user_should_follow_info(src_wb_id):
    mydb = MyMongoDB()
    result=mydb.find_return_result(str(src_wb_id))
    for sub_result in result:
        for sub_result1 in sub_result['user_should_follow_list']:
            print sub_result1


# 获取指定uid用户的  用户待关注列表(粉丝列表)user_should_follow表中的粉丝数量
def actual_insert_user_count(src_wb_id):
    mydb = MyMongoDB()
    result = mydb.find_return_result(str(src_wb_id))
    count=0
    for result1 in result:
        count=len(result1['user_should_follow_list'])
    return count

# 用户滑屏刷新页面操作
def refresh(access_token,src_wb_id):
    r=get_return_info(access_token,src_wb_id)
    # 删除掉src_wb_id的待关注用户信息，然后把新获取内容写入
    delete_src_should_follow_list(src_wb_id)
    print("删除%s记录完成"%src_wb_id)
    # 获取到的新数据 写入数据库操作方法
    db_operate(r.ids, r.total_number, src_wb_id)
    print("用户待关注列表刷新操作完成")

def delete_src_should_follow_list(src_wb_id):
    dic={'src_wb_id':str(src_wb_id)}
    mydb = MyMongoDB()
    mydb.delete(dic)



# 用户关注一个粉丝用户后 调用user_should_follow的逻辑处理 从user_should_follow表中删掉关注的粉丝
# 同时user_recently_followed 增加刚才关注的粉丝uid

# 添加和删除一个用户不能通过现有API实现。
# 所以支持服务器根据手机端正常处理结果反馈情况来进行相应处理。
def add_one_follow(access_token,uid,follow_target):
    dic={'src_wb_id':str(uid)}
    mydb=MyMongoDB()
    mydb_urf=MyMongoDB_urf()
    # 从用户待关注列表(粉丝列表)中删除follow_target 同时返回dict_sub_tmp 插入到用户最近关注列表（粉丝列表 已关注）user_recently_followed中
    dict_sub_tmp=mydb.find_and_remove(dic,uid,follow_target)
    # 当前指定uid用户的  用户待关注列表(粉丝列表)表中的粉丝数量
    print ("当前指定uid %s用户的  用户待关注列表(粉丝列表)表中的粉丝数量%s" %(str(uid),str(actual_insert_user_count(uid))))
    # 将删除的follow_target加入到用户最近关注列表（粉丝列表 已关注）user_recently_followed中
    mydb_urf.insert_user_to_user_recently_followed(str(uid),follow_target,dict_sub_tmp)