#coding=utf-8
#Version: V 1.0
author: 'WangSheng'
date: '2019/5/31 20:59'
from src.Config.TagGroupConfig import MainSteamPressure, \
    HighTempReheaterSteam,LowTempReheatSteam,LowerWaterWall,UpperWaterWall,\
    EconomizerExport,ProofExport,HorizontalFlueSideWall,RearShaftWallTube38,\
    RearShaftWallTube51,LowTemperatureSuperheater,PlatenSuperheater45,\
    PlatenSuperheater51,HighTemperatureSuperheater45,HighTemperatureSuperheater51,\
    LowTemperatureReheater,HighTemperatureReheater
from src.Tools.OpcHandle import GetPartitionData,PartitionDataHandle
import  numpy as np




def GetSteamPressure(opcData,unit):
    """

    :param opcData:  数据
    :param unit:  机组名称
    :return:各个区域的压力
    """


    tempSteam = []

    # 选择后锅炉主蒸汽压力

    MainSteam = PartitionDataHandle(
        GetPartitionData(MainSteamPressure + '_' + unit, opcData)
    )[0][2]

    # 选择后高温再热器蒸汽压力

    HighTemperatureReheaterSteam = PartitionDataHandle(
        GetPartitionData(HighTempReheaterSteam +'_'+unit,opcData)
        )[0][2]

    #低温再热器进口联箱左侧进口压力(含左右侧两个点)
    tempSteamPresure = PartitionDataHandle(
        GetPartitionData(LowTempReheatSteam + '_' + unit, opcData)
    )
    tempSteam.append(tempSteamPresure[0][2])
    tempSteam.append(tempSteamPresure[1][2])
    LowTempReheaterSteam = TwoInMiddle(tempSteam)

    return {
        LowerWaterWall+'_'+unit:20,
        UpperWaterWall+'_'+unit:20,#固定定值，与压力无关，随便什么值都可以
        EconomizerExport+'_'+unit:LowTempReheaterSteam,
        ProofExport+'_'+unit:MainSteam,
        HorizontalFlueSideWall+'_'+unit:MainSteam,
        RearShaftWallTube38+'_'+unit: MainSteam,
        RearShaftWallTube51+'_'+unit: MainSteam,
        LowTemperatureSuperheater+'_'+unit: MainSteam,
        PlatenSuperheater45+'_'+unit:MainSteam,
        PlatenSuperheater51+'_'+unit: MainSteam,
        HighTemperatureSuperheater45+'_'+unit: MainSteam,
        HighTemperatureSuperheater51+'_'+unit:MainSteam,
        LowTemperatureReheater+'_'+unit: LowTempReheaterSteam,
        HighTemperatureReheater+'_'+unit: HighTemperatureReheaterSteam,
    }











def TwoInMiddle(tempData):
    """
    二取中
    :return:
    """
    middleValue = 0

    if (tempData[0]>0.01) & (tempData[1]>0.01) :
        middleValue = (tempData[0]+tempData[1])/2
    elif (tempData[0]>0.01) & (tempData[1]<0.01):
        middleValue = tempData[0]
    elif (tempData[0]<0.01) & (tempData[1]>0.01):
        middleValue = tempData[1]
    return  middleValue

if __name__ == '__main__':
    tempList = [52,24.3]
    print(TwoInMiddle(tempList))




