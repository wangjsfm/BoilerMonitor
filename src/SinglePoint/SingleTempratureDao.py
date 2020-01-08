#coding=utf-8
"""
#Version: V 1.0
#author:  'WangSheng'
@time:2020/01/08
"""
from django.core.cache  import cache
from datetime import datetime
from RestApi.models import OvertemperatureRecord
from src.TeamRotation.TeamRotationDao import  GetCurrentTeam
from src.OpcHandle.Service.AreaRealDataServer import OpcAreaDataService,GetPartitionDataService




def RegionalMonitor(areaData,areaName,fixedValue):
    """
        区域单点壁温监控
    :param areaData: 区域所有数据，二位数组，单点为一个数组
    :param areaName:区域名
    :param fixedValue:定值
    """
    for tagData in areaData:
        SingleMonitor(tagData,areaName,fixedValue) #单点监控







def SingleMonitor(tagData,fixedValue,areaName):
    """
        温度单点监控处理
    :param tagData: kks码,标签描述，值
    :param fixedValue: 定值
    :param areaName: 该点所在区域
    """
    tagValue = tagData['tagValue']

    if tagValue > fixedValue: #缓存到redis
        CatchData(tagData,fixedValue,areaName)
    else:
        PassPersiter(fixedValue,areaName)


def PassPersiter(fixedValue,areaName):
    """
        将该区域的缓存清除掉，保存到数据库，
        如果没有缓存，则不做任何操作
    :param fixedValue:
    :param areaName:
    """
    tempratureData = cache.get(areaName)
    team = GetCurrentTeam() #当前值

    if tempratureData != None:

        beginDate = tempratureData['beginDate']
        endDate = datetime.now()

        persistence = OvertemperatureRecord(
            name=tempratureData['tagKks'],  # KKS码
            desc=tempratureData['tagDesc'],
            maxValue=tempratureData['tagValue'],
            area= areaName, #该点所在区域
            thresholdValuet = fixedValue,
            classic = team,
            beginTime=beginDate,
            endTime = endDate,
            tiemDiff=(endDate - beginDate).seconds
        )
        persistence.save()  # 保存到数据库
        cache.delete(areaName)  # 删除缓存


def CatchData(tagData,fixedValue,areaName):
        """
            将数据缓存到redis
        :param tagData:  报警点相关信息
        :param fixedValue:  报警定值
        :param areaName:  报警点所属区域
        """
        tempratureData  = cache.get(areaName)

        if tempratureData is None: #新建缓存
            cache.set(areaName,{
                'tagKks':tagData[0],
                'tagDesc':tagData[1],
                'tagValue':tagData[2],
                'tagArea':areaName,#该点所在的区域
                'thresholdValuet':fixedValue,
                'beginDate': datetime.now()
            },timeout=None )# 永不超时
        else:#更新缓存
            tempratureData['tagKks'] = tagData[0]
            tempratureData['tagDesc'] = tagData[1]
            tempratureData['tagValue'] = tagData[2]
            tempratureData['thresholdValuet'] = fixedValue
            cache.set(areaName,tempratureData,timeout=None)#更新缓存














