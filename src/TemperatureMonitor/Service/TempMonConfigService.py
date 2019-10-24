#coding=utf-8
#Version: V 1.0
author: 'WangSheng'
date: '2019/5/10 22:36'


from src.TemperatureMonitor.Dao.DataHandleDao import TemperEstimate
from src.TemperatureMonitor.Dao.GetPresureDao import GetSteamPressure


def Unit1Monitor(opcData,CurveFunctions,presure,redisClient,fixedValueFunctions):
    """
     #1机组壁温监控配置
    :param opcData:
    :param CurveFunctions:
    :param presure:
    :param redisClient:
    :param fixedValueFunctions:
    """
    # 固定定值 监控
    for area, curveFun in fixedValueFunctions.items():  # 返回区域所对应的折现函数，固定定值

        TemperEstimate(
            opcData[area + '_1'],  # opc数据   例如  'UpperWaterWall'  + '_1'
            curveFun,  # 折线函数
            presure[area + '_1'],  # 管内压力
            area + '_1',  # 监控区域   例如  'UpperWaterWall'  + '_1'
            redisClient,
        )

    # 动态定值 监控
    for area, curveFun in CurveFunctions.items():

        TemperEstimate(
            opcData[area + '_1'],
            curveFun.curveFunction,
            presure[area + '_1'],
            area + '_1',
            redisClient,
        )


def Unit2Monitor(opcData,CurveFunctions,presure,redisClient,fixedValueFunctions):
    """
        #2 机组壁温监控配置
    :param opcData:
    :param CurveFunctions:
    :param presure:
    :param redisClient:
    :param fixedValueFunctions:
    """
    #固定定值 监控
    for area,curveFun in fixedValueFunctions.items(): #返回区域所对应的折现函数，固定定值

        TemperEstimate(
            opcData[area+'_2'], #opc数据   例如  'UpperWaterWall'  + '_2'
            curveFun, #折线函数
            presure[area + '_2'], #管内压力
            area+'_2',#监控区域   例如  'UpperWaterWall'  + '_2'
            redisClient,
        )

    #动态定值 监控
    for area,curveFun in  CurveFunctions.items():
        TemperEstimate(
            opcData[area+'_2'],
            curveFun.curveFunction,
            presure[area + '_2'],
            area+'_2',
            redisClient,
        )






def OverTemperatureMonitor(opcData,CurveFunctions,redisClient,fixedValueFunctions):

    """
        #1\#2 超温监控
    """
    PressureUnit_1 = GetSteamPressure(opcData,'1')
    PressureUnit_3 = GetSteamPressure(opcData, '1')
    # PressureUnit_2 = GetSteamPressure(opcData, '2')
    Unit1Monitor(opcData,CurveFunctions,PressureUnit_1,redisClient,fixedValueFunctions) #  1号炉
    # Unit2Monitor(opcData,CurveFunctions,PressureUnit_2,redisClient,fixedValueFunctions) #  2号炉






