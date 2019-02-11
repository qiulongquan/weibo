#!/usr/bin/env python
# -*- coding:utf-8 -*-
import ConfigParser

def config_parse(section_name,key_name):
    cf=ConfigParser.ConfigParser()
    # 读配置文件（ini、conf）返回结果是列表
    if cf.read('config\config.ini'):
        print ("配置文件存在，开始读取数据")
        config=config_read(cf,section_name,key_name)
        print ("%s域下面的%s的数值为%s" %(section_name,key_name,config))
        return config
    else:
        print ("配置文件不存在。")
    # 获取读到的所有sections(域)，返回列表类型
    # cf.sections()
    # 某个域下的所有key，返回列表类型
    # cf.options('baseconf')
    # 某个域下的所有key，value
    # cf.items('baseconf')


def config_read(cf,section_name,key_name):
    # 检测指定section下是否存在指定的option，如果存在返回True，否则返回False。
    if cf.has_option(section_name,key_name):
        print ("section存在指定的key_name，开始读取key_name的数据")
        # 获取某个section下的key对应的value值
        return cf.get(section_name,key_name)
    else:
        print ("不存在指定的key_name，中止读取数据")
