#coding=utf-8
#Version: V 1.0
author: 'WangSheng'
date: '2019/5/10 22:30'

import  threading,time
from src.TemperatureMonitor.Service.TemperMoinitorSevice import MonitorAllUnit,\
    ComfirmDelet
from src.TempratureDiff.Service.TempDiffService import DiffMonitorServer

"""
    #1、#2机组壁温、温差报警监控
"""

def StartThread():
    """
        开启线程，监控所需内容

    """
    #设置线程

    # 壁温监控线程
    # overTemp = threading.Thread(target=MonitorAllUnit)
    #  温差 线程、
    diffTemp = threading.Thread(target=DiffMonitorServer)

    # 定期清理运行人员确认的壁温报警点，使得该点可以再次报警
    # comfirmAlerm = threading.Thread(target=ComfirmDelet)

    #开启线程
    # overTemp.start()
    diffTemp.start()

    # comfirmAlerm.start()
