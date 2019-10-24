#coding=utf-8
#Version: V 1.0
author: 'WangSheng'
date: '2019/5/10 22:00'
from src.OpcHandle.Dao.GetOpcDataDao import GetDataFromOpc
import pandas as pd
from src.Config.TagGroupConfig import MainSteamPressure, \
    HighTempReheaterSteam,LowTempReheatSteam,LowerWaterWall,UpperWaterWall

def OpcAreaDataService():
    """
    提供各区域壁温数据
    :return:
    """
    opcData = GetDataFromOpc()

    return opcData


def GetPartitionDataService(area,opc_real_data):
    """
    获取所需区域数据
    :param area:
    :return:
    """
    pd_opc_real_data = pd.DataFrame(opc_real_data)  # 转为pandas的DataFrame数据格式，以便处理
    pd_condition_data = pd_opc_real_data[pd_opc_real_data['GroupName'] == area]  # 获取指定区域的数据
    return pd_condition_data



if __name__ == '__main__':
    data = OpcAreaDataService()
    data2 = data[LowTempReheatSteam+'_1']
    f1 = float(data[LowTempReheatSteam+'_1'][0][1])
    f2 = float(data[LowTempReheatSteam+'_1'][1][1])

    print(type(float(f1)))

