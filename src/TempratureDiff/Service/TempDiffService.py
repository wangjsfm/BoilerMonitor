from src.Tools.OpcHandle import GetDataFromOpc,GetPartitionData
from src.TempratureDiff.Dao.TempDataHandleDao import GetMaxMinData,OutOfGaugeHandleDao
from src.Config.TempDiffConfig import TemperatureDifferenceRegion_1,\
    TemperatureDifferenceRegion_2,DeviationThreshold
import time
from src.TeamRotation.TeamRotationDao import  GetCurrentTeam


def DiffMonitorServer():
    """
    配置1、2号机组偏差报警
    """

    team = GetCurrentTeam() #当前正在上班的值
    print('job:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print(team)

    AllOpcData = GetDataFromOpc()  # 获取所有OPC数据

    UnitMonitor(AllOpcData, '1', TemperatureDifferenceRegion_1,team)  # 监视#1机组壁温
    UnitMonitor(AllOpcData, '2', TemperatureDifferenceRegion_2,team)  # 监视#2机组壁温



def UnitMonitor(allOpcData,unit,areaList,currentTeam):
    """
    单台机组温差监控 处理
    :param allOpcData:  所有OPC数据r
    :param unit: 机组编号
    :param areaList: 所有监控区域  水冷壁分上、下两部分
    """
    for partitionName in areaList: #获取单个分区名称
        regionData = GetPartitionData(partitionName,allOpcData) #获取对应区域的OPC数据
        maxTag,minTag = GetMaxMinData(regionData) #帅选出最大、最小值
        OutOfGaugeHandleDao(maxTag,minTag,DeviationThreshold,partitionName,unit,currentTeam) #对最大最小值做超限判断及处理





# if __name__ == '__main__':
#     AllOpcData = GetDataFromOpc()  # 获取所有OPC数据
#     UnitMonitor(AllOpcData,'1',TemperatureDifferenceRegion_1)