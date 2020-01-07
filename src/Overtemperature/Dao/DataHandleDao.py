#coding=utf-8
#Version: V 1.0
author: 'WangSheng'
date: '2019/5/10 23:27'

from datetime import datetime
from django.core.cache  import cache
from RestApi.models import OvertemperatureRecord
from src.Config.OpreaterConfig import Coefficient


def  TemperEstimate(data,curveFun,presure,area,redisClient):
    """

    判断整个区域壁温点是否超过定值

    :param data: 壁温点数据
    :param curveFun: 折线函数
    :param presure: 当前压力
    :param area:  当前处理的区域
    :param redisClient:  redis客户端
    """
    thresholdValue  =curveFun(presure)  #生成报警定值
    alermValue = curveFun(presure,Coefficient) #根据报警系数 生成的定值
    # 从opc中获取 单条数据
    for index,item in data:
        tagName = item[0]
        tagDesc = item[1]
        tagValue = item[2]

        if tagValue < 0.01:  # 防止数据为负值
            tagValue = 0


         #超过定值，存入redis 或者存入DB,同时并报警
        DataHandle(tagName, tagValue, tagDesc, thresholdValue, area)

        #达到报警条件
        DataAlermHandle(tagName, tagValue, tagDesc, alermValue,thresholdValue, redisClient)





def DataAlermHandle(tagName, tagValue, tagDesc, alermValue, redisClient):
    """
        数据超过报警值，存入redis（超过记录定值不再一个实例）
    :param tagName:
    :param tagValue:
    :param tagDesc:
    :param alermValue:
    :param thresholdValue:
    :param area:
    :param redisClient:
    """
    tagCachStatus = redisClient.exists(tagName)  # 1.存在   0.不存在
    tagCachData = redisClient.hgetall(tagName)
    tagDataStatus='0'



    if tagCachData:
        tagDataStatus = str(tagCachData[b'status'], encoding="utf8") #该条记录是否被确认

    alermData = {
        'tagValue':tagValue,
        'tagDesc':tagDesc,
        'alermValue':alermValue,
        'status':'1',
    }


    if tagValue >= alermValue  : #在报警范围内

        if tagCachStatus == 0: #redis中无缓存，新建记录
            redisClient.hmset(tagName,alermData)
        elif tagCachStatus == 1:#redis中有缓存，更新记录
            if tagDataStatus=='1':  #报警未确认，则继续更新
                redisClient.hmset(tagName,alermData) #更新记录



    elif tagValue < alermValue: #未在报警范围，删除报警信息

        if tagCachStatus == 1: #数据存在，则删除
            redisClient.delete(tagName)












def DataHandle(name,value,tagDesc,thresholdValuet,area):
    """
    处理单个壁温点数据，超过定值后存入redis缓存。
    若已在缓存中，继续报警则更新缓存，报警不再超过定值则将上次报警数据存入DB
    :param tagName:  标签名(KKS）
    :param tagValue:  标签当前值
    :param tagDesc:  标签描述
    :param thresholdValue:  报警定值
    :param area: 处理数据所属的区域
    """
    get_value_catch = cache.get(name)  # 根据标签名获取redis中对应的数据

    if get_value_catch is None:  # redis中无标签对应的数据，则新建一条数据缓存到redis

        if value >= thresholdValuet:  # 标签当前值大于定值

            # 超过定值，放入redis
            cache.set(name, {
                'tagDesc': tagDesc,  # 标签描述
                'curentValue': value,  # 当前值
                'maxValue': value,  # 最大值，第一次最大值为当前值
                'thresholdValuet': thresholdValuet,
                'beginDate': datetime.now(),
                'area': area,
                'endDate': '',
                'status': 1  # 1：报警  0:报警结束
            },
                      timeout=None,  # 永不超时
                      )



    else:

        if get_value_catch['status'] == 1:  # 1：报警未结束

            if value >= thresholdValuet:  # 大于定值 更新缓存maxvalue数据

                maxValue = get_value_catch['maxValue']
                get_value_catch['thresholdValuet'] = thresholdValuet  #
                if value > maxValue:
                    get_value_catch['maxValue'] = value  # 更新状态

                get_value_catch['curentValue'] = value  # 更新状态
                cache.set(name, get_value_catch, timeout=None)  # 更新数据到redis

            else:

                get_value_catch['status'] = 0  # 更新状态
                get_value_catch['endDate'] = datetime.now()  # 结束日期
                cache.set(name, get_value_catch, timeout=None)  # 更新数据到redis



        elif get_value_catch['status'] == 0:  # 该条报警状态已结束，保存到数据库，随后删除redis中数据

            beginTime1 = get_value_catch['beginDate'],
            endTime1 = get_value_catch['endDate'],

            # if BoilerUrl.OPREATION_CLASSIC == 0:
            #     BoilerUrl.OPREATION_CLASSIC = UpdataPeriodTeam()  # 更新OPREATION_CLASSIC

            persistence = OvertemperatureRecord(
                name=name,
                desc=get_value_catch['tagDesc'],
                area=get_value_catch['area'],
                # classic=boilerUrls.OPREATION_CLASSIC,
                classic='2',
                maxValue=get_value_catch['maxValue'],
                thresholdValuet=get_value_catch['thresholdValuet'],
                beginTime=get_value_catch['beginDate'],
                endTime=get_value_catch['endDate'],
                tiemDiff=(endTime1[0] - beginTime1[0]).seconds)

            persistence.save()  # 保存到数据库

            cache.delete(name)  # 报警结束 删除缓存


