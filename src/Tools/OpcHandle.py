import  requests
from src.Config.OpcConfig import OpcServer_API
import pandas as pd


def GetDataFromOpc():
    """
    从OPC服务器获取 所有数据
    :return:
    """
    retult = requests.get(OpcServer_API).json()

    return  retult

def GetPartitionData(area,opcData):
    """
    获取所需区域数据
    :param area:
    :return:
    """
    pd_opc_real_data = pd.DataFrame(opcData)  # 转为pandas的DataFrame数据格式，以便处理
    filterData = pd_opc_real_data[pd_opc_real_data['GroupName'] == area]  # 获取指定区域的数据
    selectData = filterData[['ItemID', 'Name', 'Value']]  # 获取指定字段的数据

    return selectData.iterrows()


def PartitionDataHandle(iterrowsData):
    """
        将iterrows类型数据转为 List
    :param iterrowsData:
    :return:
    """
    tempList = []
    for index, row in iterrowsData:
        tagName = row['ItemID']
        tagDesc = row['Name']
        tagValue = round(float(row['Value']), 2)
        tempList.append([tagName,tagDesc,tagValue])
    return  tempList



if __name__ == '__main__':
    areaName = 'PlatenSuperheater1'

    opcData = GetDataFromOpc()
    data= GetPartitionData(areaName,opcData)
    pd_data = PartitionDataHandle(data)
    print(pd_data)

