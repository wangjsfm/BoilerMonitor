#coding=utf-8
"""
#Version: V 1.0
#author:  'WangSheng'
@time:2019/12/25
"""

from django.core.cache  import cache
from src.Overtemperature.Dao.DataHandleDao import TemperEstimate
from src.Overtemperature.Dao.GetPresureDao import GetSteamPressure
from src.Tools.OpcHandle import GetPartitionData



def UnitMonitor(opcData,CurveFunctions,fixedValueFunctions,unit):
    """
    机组壁温，超温监控配置
    :param opcData:  所有OPC数据
    :param CurveFunctions: 折现函数
    :param Presure: 管道压力
    :param redisClient:缓存客户端
    :param fixedValueFunctions:
    :param unit:机组信息
    """

    redisClient = cache
    presure = GetSteamPressure(opcData, unit)

    # 固定定值 监控
    for area, curveFun in fixedValueFunctions.items():  # 返回区域所对应的折现函数，固定定值

        regionData = GetPartitionData(area +'_' +unit, opcData)  # 获取对应区域的OPC数据

        TemperEstimate(
            regionData,  # opc数据   例如  'UpperWaterWall'  + '_1'
            curveFun,  # 折线函数
            presure[area +'_' + unit],  # 管内压力
            area +'_' +unit,  # 监控区域   例如  'UpperWaterWall'  + '_1'
            redisClient,
        )

    # 动态定值 监控
    for area, curveFun in CurveFunctions.items():

        regionData = GetPartitionData(area +'_' + unit, opcData)  # 获取对应区域的OPC数据

        TemperEstimate(
            regionData,
            curveFun.curveFunction,
            presure[area +'_' + unit],
            area +'_' + unit,
            redisClient,
        )