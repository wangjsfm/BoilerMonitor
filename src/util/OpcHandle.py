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
    # 从opc中获取 单条数据 实例
    # for index, row in pd_filter_data.iterrows():
    #     tagName = row['ItemID']
    #     tagDesc = row['Name']
    #     tagValue = round(float(row['Value']), 2)
    #     if tagValue < 0.01:  # 防止数据为负值
    #         tagValue = 0
    #     dataProcess(tagName, tagValue, tagDesc, thresholdValuet, opcAreaClassification)
    return selectData.iterrows()


if __name__ == '__main__':
    orign = GetDataFromOpc()
    data = GetPartitionData('unit1_screen',orign)

    for index, row in data:
        tagName = row['ItemID']
        tagDesc = row['Name']
        tagValue = round(float(row['Value']), 2)
        if tagValue < 0.01:  # 防止数据为负值
            tagValue = 0
        print(tagDesc,tagValue)
    print(data)