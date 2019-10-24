#coding=utf-8
#Version: V 1.0
author: 'WangSheng'
date: '2019/6/2 15:44'

from src.OpcHandle.Service.AreaRealDataServer import OpcAreaDataService
from src.Config.TagGroupConfig import LowerWaterWallGroup,UpperWaterWallGroup
from src.Config.OpreaterConfig import DeviationThreshold
from src.DeviationMonitor.Dao.TempDataHandleDao import GetOpcDataClassic,TempreatureDiffHandle
from src.RedisHandle.Service.RedisClientService import RedisClient
import  time

RedisClient = RedisClient()


def EvaluationTempDiff():
    pass

def DevitionConfig(unit):
    ALLAreaData = OpcAreaDataService()  # 获得所有区域OPC数据

    #获取上部、下部水冷壁的数据

    lowerGroupList = GetOpcDataClassic(ALLAreaData, LowerWaterWallGroup, unit)
    upperGroupList = GetOpcDataClassic(ALLAreaData, UpperWaterWallGroup, unit)

    # 区域内部数据，偏差监控，处理
    altemText1 = TempreatureDiffHandle(lowerGroupList,DeviationThreshold,unit,RedisClient,'lowerGroup')
    alterm2 = TempreatureDiffHandle(upperGroupList, DeviationThreshold, unit,RedisClient,'upperGroup')


    print(alterm2)
    print(altemText1)






if __name__ == '__main__':
    while True:
        DevitionConfig('1')
        time.sleep(3)

