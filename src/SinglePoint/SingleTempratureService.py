#coding=utf-8
"""
#Version: V 1.0
#author:  'WangSheng'
@time:2020/01/08
"""
from  src.Tools.OpcHandle import PartitionDataHandle,GetDataFromOpc,GetPartitionData
from src.SinglePoint.SingleTempratureDao import RegionalMonitor

def SingleUnitMonitor(unit):
    """
        单台机组超温 配置
    :param unit: 机组
    """
    areaName = 'PlatenSuperheater1'
    opcData = GetDataFromOpc() #所有区域数据
    area_data = PartitionDataHandle(
        GetPartitionData(areaName, opcData) #该区域数据
    )
    SigleAreaMonitor(area_data) #单个区域 壁温监控



def SigleAreaMonitor(areaData,areaName):
    """
    单个区域 壁温监控
    :param areaData: 区域内所有数据
    :param areaName:  区域名
    """
    fixedValue = 400 #生成定值
    for tagData in areaData: #逐点检查
        RegionalMonitor(tagData,areaName,fixedValue)




















