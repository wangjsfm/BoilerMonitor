#coding=utf-8
#Version: V 1.0
author: 'WangSheng'
date: '2019/5/31 17:01'


def  UpdateStatus(redisClient):
    tagKeys = redisClient.keys(pattern="*")
    for tagName in tagKeys:
        alermData = redisClient.hgetall(tagName)#获取缓存数据
        alermData[b'status'] = '1'#更新状态变了
        redisClient.hmset(tagName,alermData)#更新至redis
