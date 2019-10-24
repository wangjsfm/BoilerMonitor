#coding=utf-8
#Version: V 1.0
author: 'WangSheng'
date: '2019/5/15 16:41'

from src.Config.RedisConfg import Redis_port,Redis_host,Redis_pwd,Redis_db
import  redis



def RedisClient():
    pool = redis.ConnectionPool(host = Redis_host,port = Redis_port,password=Redis_pwd,db=Redis_db)
    client = redis.Redis(connection_pool=pool)
    redis.StrictRedis(host=Redis_host, port=Redis_port, password=Redis_pwd,db=Redis_db)
    return  client



if __name__ == '__main__':

    client = RedisClient()
    #
    # client.hmset(tagName,data)
    # # client.delete(tagName)
    # getdA = client.hgetall()
    # sta = getdA[b'status']
    # print(type(client.exists(tagName)))
    # print(sta)
    # print(str(sta, encoding = "utf8"))
    # print(type(str(sta, encoding = "utf8")))

    data = client.hgetall('lowerGroup1')

    print(data[b'diffValue'])





