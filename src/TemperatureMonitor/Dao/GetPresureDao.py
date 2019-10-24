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



def GetSteamPressure(opcData,unit):
    """

    :param opcData:  数据
    :param unit:  机组名称
    :return:各个区域的压力
    """
    # 选择后锅炉主蒸汽压力
    tempSteam = []
    temp = MainSteamPressure+'_'+unit
    MainSteam = float(opcData[MainSteamPressure+'_'+unit][0][1])
    # 选择后高温再热器蒸汽压力
    HighTemperatureReheaterSteam = float(opcData[HighTempReheaterSteam +'_'+unit][0][1])
    #低温再热器进口联箱左侧进口压力(含左右侧两个点)
    tempSteamPresure = opcData[LowTempReheatSteam+'_'+unit]
    tempSteam.append(float(tempSteamPresure[0][1]))
    tempSteam.append(float(tempSteamPresure[1][1]))
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




