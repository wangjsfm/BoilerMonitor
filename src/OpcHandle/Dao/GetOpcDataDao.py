#coding=utf-8
#Version: V 1.0
author: 'WangSheng'
date: '2019/5/10 21:42'

import  requests
from src.Config.OpcConfig import OpcServer_API



def GetDataFromOpc():
    """
    从OPC服务器获取 所有数据
    :return:
    """
    retult = requests.get(OpcServer_API).json()

    return  retult
