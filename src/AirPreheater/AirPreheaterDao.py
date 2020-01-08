#coding=utf-8
"""
#Version: V 1.0
#author:  'WangSheng'
@time:2020/01/07
"""
from datetime import datetime
from django.core.cache  import cache
from RestApi.models import AirPreheater
from src.TeamRotation.TeamRotationDao import  GetCurrentTeam


def OverTempretureHandle(curenTemp,areaName,alermType):
    """
        空预器温度超温 处理
    :param curenTemp: 当前温度
    :param alermThrosh: 报警定制
    :param areaName: 机组 区域名称
    :param alermType: 报警类型 ge大于上限  le小于下限值
    """

    airData  = cache.get(areaName)

    if airData is None:
        alermLimit = curenTemp
    else:
        alermLimit = airData['alermLimit']  # 报警极限值

    if alermType == 'ge': #当前值 > 上限定值
        if curenTemp > alermLimit:
            ge = curenTemp  # 报警后 最大值
        else:
            ge = alermLimit

        AirDataCach(areaName, ge)  # 缓存


    elif alermType == 'le':
        if curenTemp < alermLimit:
            le = curenTemp  # 报警后 最大值
        else:
            le = alermLimit
        AirDataCach(areaName, le)  # 缓存





def AirDataCach(areaName,alermLimit):
        """
            缓存数据
        :param areaName: 空预器区域名
        :param alermLimit: 当前极限值  最大或者最小值
        """

        get_cache_data = cache.get(areaName)
        # 新建一条缓存信息
        if get_cache_data is None:

            cache.set(areaName, {
                'alermLimit': alermLimit,
                'beginDate': datetime.now()
            },
                      timeout=None,  # 永不超时
                      )
            print('新建 缓存  ', cache.get(areaName))

        else:
            get_cache_data['alermLimit'] = alermLimit
            cache.set(areaName, get_cache_data,timeout=None)

            print('更新 缓存  ', cache.get(areaName))






def SaveAlerm(areaName):
    """
        空预器温度在正常范围内，将缓存 存入数据库，清除缓存
    :param areaName:
    """
    airData = cache.get(areaName)

    if airData != None : #有缓存则保存到数据库，并删除缓存

        if areaName == 'airpreheater_a_1':
            nameTemp = '1号机组空预器A'

        elif areaName == 'airpreheater_b_1':
            nameTemp = '1号机组空预器B'

        elif areaName == 'airpreheater_a_2':
            nameTemp = '2号机组空预器A'

        elif areaName == 'airpreheater_b_2':
            nameTemp = '2号机组空预器B'


        beginDate = airData['beginDate']
        endDate = datetime.now()
        team = GetCurrentTeam()
        persistence = AirPreheater(
            name=nameTemp,  # 区域名
            limitValue=airData['alermLimit'],
            beginTime=airData['beginDate'],
            classic = team, #当前值
            endTime=endDate,
            tiemDiff=(endDate - beginDate).seconds
        )


        persistence.save()  # 保存到数据库
        cache.delete(areaName)  # 删除缓存






