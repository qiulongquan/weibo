#!/usr/bin/env python
# -*- coding:utf-8 -*-

import authorization
import config.config_parse
from weiboDB.weiboDB_userinfo import MyMongoDB

def get_friendship_list(access_token,uid):
    # 通过http方法来调用API接口，并取得返回值
    # 获取用户的关注列表
    resp_text = authorization._http('GET', 'https://api.weibo.com/2/friendships/friends.json',
                      access_token=access_token,uid=uid)
    r = authorization._parse_json(resp_text)
    # JsonDict型的数据直接用 .key 来提取值


    print ("uid  " + str(r.id))
    print ("screen_name  " + r.screen_name.encode('unicode-escape').decode('string_escape').decode('unicode_escape'))
    print ("name " + r.name.encode('unicode-escape').decode('string_escape').decode('unicode_escape'))
    print ("location " + r.get('location').encode('unicode-escape').decode('string_escape').decode('unicode_escape'))
    print ("description " + r.description.encode('unicode-escape').decode('string_escape').decode('unicode_escape'))
    print ("image " + r.profile_image_url.encode('unicode-escape').decode('string_escape').decode('unicode_escape'))
    print ("gender " + r.gender.encode('unicode-escape').decode('string_escape').decode('unicode_escape'))
    print ("profile_url  " + str(r.profile_url))
    print ("domain  " + str(r.domain))
    print ("followers_count  " + str(r.followers_count))
    print ("friends_count  " + str(r.friends_count))
    print ("statuses_count  " + str(r.statuses_count))
    print ("status  " + str(r.status))
    print ("created_at  " + r.created_at)
    print ("verified  " + str(r.verified))
    print ("geo_enabled  " + str(r.geo_enabled))
    print ("allow_all_comment  " + str(r.allow_all_comment))
    print ("allow_all_act_msg  " + str(r.allow_all_act_msg))
    print ("avatar_large  " + str(r.avatar_large))
    print ("avatar_hd  " + str(r.avatar_hd))
    print ("follow_me  " + str(r.follow_me))
    print ("online_status  " + str(r.online_status))
    print ("bi_followers_count  " + str(r.bi_followers_count))

    # 将获取的数据写入到数据库中
    mydb = MyMongoDB()
    dic = {"id": str(r.id),
           "name": r.name.encode('unicode-escape').decode('string_escape').decode('unicode_escape'),
           "screen_name": r.screen_name.encode('unicode-escape').decode('string_escape').decode('unicode_escape'),
           "location": r.get('location').encode('unicode-escape').decode('string_escape').decode('unicode_escape'),
           "description": r.description.encode('unicode-escape').decode('string_escape').decode('unicode_escape'),
           "image": r.profile_image_url.encode('unicode-escape').decode('string_escape').decode('unicode_escape'),
           "gender": r.gender,
           "profile_url": r.profile_url,
           "domain": r.domain,
           "followers_count": r.followers_count,
           "friends_count": r.friends_count,
           "favourites_count": r.favourites_count,
           "statuses_count": r.statuses_count,
           "status": r.status,
           "create_at": r.created_at,
           "verified": r.verified,
           "geo_enabled": r.geo_enabled,
           "allow_all_comment": r.allow_all_comment,
           "allow_all_act_msg": r.allow_all_act_msg,
           "avatar_large": r.avatar_large,
           "avatar_hd": r.avatar_hd,
           "follow_me": r.follow_me,
           "online_status": r.online_status,
           "bi_followers_count": r.bi_followers_count
           }
    mydb.insert_user_info(dic)

    # 也可以用  .get 方法来获取值  r.get('remind_in', None)
    # remind_in = r.get('remind_in', None)