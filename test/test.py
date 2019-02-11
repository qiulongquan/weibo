#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ConfigParser
import config.config_parse
import time,datetime,json

# str1 = u'\u90b1\u73d1\u6cc9'
# print str1.decode('unicode_escape')
# print str1.encode('unicode-escape').decode('string_escape').decode('unicode_escape')

# str2=str1.encode('unicode-escape').decode('string_escape')
# print str2
# print str2.decode('unicode_escape')
#
# str = 1234
# str1 = 12343
# print("ddd%sffff%s" % (str, str1))
def aaa(a=1,b=2,**kw):
    print a
    print b
    print kw['c']
    print kw['d']
    kw['d']=kw['d']+'已经修改过'
    return kw

def bbb(a=1,b=2,**kw):
    print a
    print b
    print kw['c']
    print kw['d']
    result={'result':0,'a':1234,'b':'abcdefg'}
    return result


# 计算两个日期相差天数，自定义函数名，和两个日期的变量名。
def Caltime(date1, date2):

    # %Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。

    date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")

    # date1 = time.strptime(date1, "%Y-%m-%d")
    # date2 = time.strptime(date2, "%Y-%m-%d")
    # 根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
    date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])

    # date1 = datetime.datetime(date1[0], date1[1], date1[2])
    # date2 = datetime.datetime(date2[0], date2[1], date2[2])
    # 返回两个变量相差的值，就是相差天数
    return date2 - date1

def find():
    str = '123123123_01'
    substr = '_'
    index1 = str.find(substr)
    str2 = str[index1 + 1:]
    print(str2)

def strtodate():
    # # date to str
    # print time.strftime("%Y-%m-%d %X", time.localtime())
    # str to date
    t = time.strptime("2017-07-17 12:29:12", "%Y-%m-%d %H:%M:%S")
    y, m, d = t[0:3]
    print y
    print m
    print d
    print datetime.datetime(y, m, d)
    current_time = time.strftime("%Y-%m-%d",t)
    print current_time

def json_test():
    data1 = {'b': 789, 'c': 456, 'a': 123}
    encode_json = json.dumps(data1)
    print type(encode_json), encode_json    #<type 'str'> {"a": 123, "c": 456, "b": 789}
    decode_json = json.loads(encode_json)
    print type(decode_json)                 #<type 'dict'>
    print decode_json['a']                  #123
    print decode_json                       #{u'a': 123, u'c': 456, u'b': 789}

if __name__ == '__main__':

    # json_test()

    str_text = {u'bi_followers_count': 2, u'domain': u'',
                u'avatar_large': u'http://tvax4.sinaimg.cn/crop.11.0.728.728.180/006ozQKIly8fo006dyk15j30ku0k8dhb.jpg',
                u'verified_source': u'', u'ptype': 0,
                u'cover_image_phone': u'http://wx1.sinaimg.cn/crop.0.0.640.640.640/006ozQKIly1fnodbavekgj30qo0qpwf7.jpg',
                u'statuses_count': 2535, u'id': 5859973320L, u'verified_reason_url': u'', u'city': u'1000',
                u'like_me': False, u'verified': False, u'credit_score': 80, u'insecurity': {u'sexual_content': False},
                u'block_app': 1, u'status_id': 4267962158137723L, u'follow_me': False, u'verified_reason': u'',
                u'followers_count': 1860466, u'location': u'\u6d77\u5916', u'verified_trade': u'', u'mbtype': 12,
                u'verified_source_url': u'', u'profile_url': u'u/5859973320', u'block_word': 0,
                u'avatar_hd': u'http://tvax4.sinaimg.cn/crop.11.0.728.728.1024/006ozQKIly8fo006dyk15j30ku0k8dhb.jpg',
                u'star': 0,
                u'description': u'\u8ba9\u5927\u53d4\u5e2e\u4f60\u5b9e\u73b0\u613f\u671b  \u5546\u52a1\u5408\u4f5cVX\uff1axiuyuan018',
                u'friends_count': 13, u'online_status': 0, u'mbrank': 5, u'idstr': u'5859973320',
                u'profile_image_url': u'http://tvax4.sinaimg.cn/crop.11.0.728.728.50/006ozQKIly8fo006dyk15j30ku0k8dhb.jpg',
                u'allow_all_act_msg': False,
                u'cover_image': u'http://wx3.sinaimg.cn/crop.0.0.920.300/006ozQKIly1fniij39o3oj30pk08cgxj.jpg',
                u'screen_name': u'\u5927\u4ea8', u'vclub_member': 0, u'allow_all_comment': True, u'geo_enabled': False,
                u'class': 1, u'name': u'\u5927\u4ea8', u'lang': u'zh-cn', u'weihao': u'', u'remark': u'',
                u'favourites_count': 60, u'like': False, u'url': u'', u'province': u'400',
                u'created_at': u'Mon Feb 15 15:13:42 +0800 2016', u'video_status_count': 0, u'user_ability': 1311232,
                u'story_read_state': -1, u'verified_type': -1, u'gender': u'm', u'following': True,
                u'pagefriends_count': 0, u'urank': 35}
    print ("第一个参数u'\u5927\u4ea8' 解析后  "+str_text['screen_name'].encode("utf-8"))

    # python实现字符串和日期相互转换的方法
    # strtodate()
    # 截取一部分字符串
    # find()

    # 计算时间差值
    # 格式化成2016-03-20 11:45:39形式
    # date1=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # date2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print Caltime(date1, date2)


    # 多个参数返回
    # return_kw=aaa(a=1,b=2,c='3abc',d='4def我要')
    # print return_kw

    # return_kw=bbb(a=1,b=2,c='3abc',d='4def我要')
    # print return_kw['result']
    # print return_kw['a']
    # print return_kw['b']

    # 配置文件读取方法
    # config1=config_parse.config_parse('baseconf','host')
    # print config1
    # cf=ConfigParser.ConfigParser()
    # # 读配置文件（ini、conf）返回结果是列表
    # if cf.read('config.ini'):
    #     print ("配置文件存在，开始读取数据")
    # else:
    #     print ("配置文件不存在。")
    # # 获取读到的所有sections(域)，返回列表类型
    # cf.sections()
    # # 某个域下的所有key，返回列表类型
    # cf.options('baseconf')
    #
    # # 某个域下的所有key，value
    # cf.items('baseconf')
    #
    # # 检测指定section下是否存在指定的option，如果存在返回True，否则返回False。
    # if cf.has_option('baseconf', 'host'):
    #     print ("存在指定的key，开始读取数据")
    #     # 获取某个yu下的key对应的value值
    #     value = cf.get('baseconf', 'host')
    #     print value
    # else:
    #     print ("不存在指定的key，中止读取数据")

