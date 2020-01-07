#coding=utf-8
"""
#Version: V 1.0
#author:  'WangSheng'
@time:2019/12/25
"""

from src.Model.Service.ModInitService import TempModelInit
from src.Config.TagGroupConfig import LowerWaterWall,UpperWaterWall
from src.Model.Service.FixedValueServerce import LowerWaterWallModle,UpperWaterWallModle
from src.Overtemperature.Service.UnitSerice import UnitMonitor
from src.Tools.OpcHandle import GetDataFromOpc


def MonitorAllUnit():
    """
        配置#1、2号机组超温监控
    """
    AllOpcData = GetDataFromOpc()  # 获取所有OPC数据

    CurveFunctions = TempModelInit()  # 各个区域，动态报警定值生成折线函数

    FixedValueFunctions = {  # 固定定值函数
        LowerWaterWall: LowerWaterWallModle,
        UpperWaterWall: UpperWaterWallModle,
    }

    UnitMonitor(AllOpcData, CurveFunctions, FixedValueFunctions,'1')# 1号机组配置
    UnitMonitor(AllOpcData, CurveFunctions, FixedValueFunctions, '2')  # 2号机组配置


if __name__ == '__main__':
    MonitorAllUnit()

