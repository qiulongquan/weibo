#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import config.config_parse
import authorization
import table.fans_master
import user_info
import get_friendship_list
import json
import table.auth_token
import table.user_should_follow
import table.user_should_unfollow
from weiboDB.weiboDB_userinfo import MyMongoDB

if __name__ == '__main__':
    APP_KEY=config.config_parse.config_parse('weibo_authorization','APP_KEY')
    APP_SECRET = config.config_parse.config_parse('weibo_authorization', 'APP_SECRET')
    access_token = '2.00JDmx9C0PwxRR143cc743bd_ffgZB'
    uid=2260249131
    # expires = config.config_parse.config_parse('weibo_authorization', 'expires')

    # APP_KEY = '255479695'
    # APP_SECRET = '909e9b6025d5e500577b194bab50e1a6'
    # access_token = '2.00fcTNKH0PwxRR53eb3ad4470jtWn3'
    # uid = 6563905321
    # expires = 1393739173.5
    # access_token=''
    # expires=0

    # c = authorization.APIClient(authorization.SinaWeiboMixin,APP_KEY,APP_SECRET,'https://api.weibo.com/oauth2/default.html',access_token,expires)
    # url = c.get_authorize_url()
    # print ("return url",url)
    # code = '984ecf9617edb1b985957aa9aab826fe'
    # uid = 6563905321

    # 用户同意授权后会重定向到redirect 链接处
    # https: //api.weibo.com/auth2/default.html? code =27a07456dfab444c0b55c4ec5f1c0c05
    # 返回值 code 用于第二步调用oauth2 / access_token接口，获取授权后的 access token

    # get_token=c.request_access_token(code,'https://api.weibo.com/oauth2/default.html')
    # json_string = json.dumps(get_token)
    # temp_get_token=json.loads(json_string,"utf-8")
    # print ("获取的用户token")
    # access_token=temp_get_token['access_token']
    # print(access_token)
    # expires=temp_get_token['expires']
    # print ("获取的用户token的有效期")
    # print(expires)
    # print ("获取的用户token里面的uid")
    # uid=temp_get_token['uid']
    # print(temp_get_token['uid'])

# ----------本次程序使用的调用方法 先去掉注释然后分别调用测试---------------

    # 写入token授权表，进行比对和更新
    # auth_token.auth_token(access_token,expires,str(uid))

    # 用户的粉丝和用户的关注列表内容写入 DB
    # table.fans_master.insert_fans_master_info(access_token,uid)

    # 用户待关注列表(粉丝列表)初期写入操作
    # table.user_should_follow.insert_user_should_follow(access_token,uid)

    # 用户滑屏刷新页面操作(用户待关注列表(粉丝列表))
    # table.user_should_follow.refresh(access_token,uid)

    # 用户关注一个粉丝用户操作
    # target='6549004815'
    # table.user_should_follow.add_one_follow(access_token,uid,target)

    # 用户待取消关注列表(用户关注列表)初期写入操作
    # table.user_should_unfollow.insert_user_should_unfollow(access_token,uid)

    # 用户滑屏刷新页面操作(用户待取消关注列表)
    # table.user_should_unfollow.refresh(access_token,uid)

    # 用户取消关注一个粉丝用户的操作
    # target='5184065814'
    # table.user_should_unfollow.remove_one_follow(access_token,uid,target)


# ----------------------以下为其他功能调用的方法-----------------------------------------

    # access_token现在是手动写入的，
    # 实际情况是用户打开链接然后授权后，
    # 系统获取access_token 和 expires
    # c.set_access_token(access_token,expires)

    # 通过http方法来调用API接口，并取得返回值
    # resp_text = _http('POST', 'https://api.weibo.com/oauth2/authorize',
    #                   client_id=APP_KEY,redirect_uri='https://api.weibo.com/oauth2/default.html')
    # r = _parse_json(resp_text)
    # JsonDict型的数据直接用 .key 来提取值
    # expires = r.expires_in + current
    # 也可以用  .get 方法来获取值  r.get('remind_in', None)
    # remind_in = r.get('remind_in', None)

    # 通过http方法来调用API接口
    # 获取指定的UID用户的信息
    # uid=6563905321
    # get_user_info.get_user_info(access_token,uid)

    # 获取用户的关注列表  调用get_friendship_list 方法
    # get_friendship_list.get_friendship_list(access_token,uid)
    # print ("ok")
    # print("微博内容获取")
    # r=c.statuses.user_timeline.get()
    # for st in r.statuses:
    #     print st.text

    # print("取消授权")
    # r=c.oauth2.revokeoauth2.get()
    # print r

    # print ("获取当前登录用户的API访问频率限制情况 home_timeline")
    # r = c.statuses.home_timeline.get()
    # for st in r.statuses:
    #     print st.text
    #
    # print("获取某个用户最新发表的微博列表")
    # r = c.statuses.user_timeline.get()
    # for st in r.statuses:
    #     print st.text
    #
    # print("获取当前登录用户的API访问频率限制情况")
    # r = c.account.rate_limit_status.get()
    # print("输出的是dict格式 共有10行")
    # for st in r.api_rate_limits:
    #     print st

    # print("获取用户信息")
    # r = c.users.show.get(uid=1404376560)
    # print("需要加入参数uid 否则会显示APIError: 10008")
    # json_string = json.dumps(r)
    # str_temp=json.loads(json_string,"utf-8")
    # print("获取用户信息")
    # print(str_temp)
    # print(str_temp['name'])
    # print(str_temp['description'])

    # print("获取用户信息UID")
    # r = c.account.get_uid.get()
    # # json.dumps用于将Python对象编码成JSON字符串。
    # json_string = json.dumps(r)
    # print(str(json_string))
    #
    # # json.loads用于解码JSON数据。该函数返回Python字段的数据类型。
    # str_temp=json.loads(json_string)
    # print("获取用户信息UID")
    # print(str(str_temp["uid"]))

    # print("获取最新的提到登录用户的微博列表，即@我的微博")
    # r = c.statuses.public_timeline.get()
    # # print json.dumps(json.loads(r),ensure_ascii=False)
    # # json.dumps用于将Python对象编码成JSON字符串。
    # json_string = json.dumps(r,ensure_ascii=False)
    # print (json_string)
    # print type(json_string)
    # # json.loads用于解码JSON数据。该函数返回Python字段的数据类型。
    # str_temp=json.loads(json_string)
    # print type(str_temp)
    # print("信息一览")
    # a=str_temp["statuses"]
    # print type(a)
    # print((a[0])["reposts_count"])

    # print("获取最新的提到登录用户的微博列表，即@我的微博")
    # r = c.statuses.public_timeline.get()
    # print type(r)
    # # print json.dumps(json.loads(r),ensure_ascii=False)
    # # json.dumps用于将Python对象编码成JSON字符串。
    # json_string = json.dumps(r,ensure_ascii=False)
    # print (json_string)
    # print type(json_string)
    # # json.loads用于解码JSON数据。该函数返回Python字段的数据类型。
    # str_temp=json.loads(json_string)
    # print type(str_temp)
    # print("信息一览")
    # a=str_temp["statuses"]
    # print type(a)
    # print((a[0])["reposts_count"])

    # print("对一条微博进行评论 评论内容qlqqlq ")
    # r = c.comments.create.post(comment="qlqqlq",id=4255674026496988)
    # print type(r)
    # json_string = json.dumps(r,ensure_ascii=False)
    # print (json_string)
