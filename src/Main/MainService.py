#coding=utf-8
#Version: V 1.0
author: 'WangSheng'
date: '2019/5/10 22:30'

from src.Config.ThreadConfig import TempDiffAlermCycl,OverTempCycl
from apscheduler.schedulers.background import BackgroundScheduler
from src.TempratureDiff.Service.TempDiffService import DiffMonitorServer
from src.TeamRotation.TeamRotationDao import TeamRotatinoHandle
from src.Overtemperature.Service.MonitorConfigService import MonitorAllUnit
from src.AirPreheater.AirPreheaterService import AirPreaheaterMonit

"""
    #1、#2机组监控配置
"""


def StartThread():
    """
        开启线程，监控所需内容
    """


    # 壁温监控线程
    # overTemp = threading.Thread(target=MonitorAllUnit)


    # 定期清理运行人员确认的壁温报警点，使得该点可以再次报警
    # comfirmAlerm = threading.Thread(target=ComfirmDelet)

    #开启线程
    # overTemp.start()
    # diffTemp.start()

    # comfirmAlerm.start()


    # BackgroundScheduler: 程序后台运行
    scheduler = BackgroundScheduler()
    # 采用非阻塞的方式

    # 采用固定时间间隔（interval）的方式，间隔时间到，执行任务
    scheduler.add_job(DiffMonitorServer, 'interval', seconds=TempDiffAlermCycl)  #温差监控任务
    scheduler.add_job(MonitorAllUnit, 'interval', seconds=OverTempCycl)  # 单点超温  监控任务
    # scheduler.add_job(AirPreaheaterMonit, 'interval', seconds=OverTempCycl)  # 空预器超温

    # 采用定时（cron）的方式 定时执行任务
    scheduler.add_job(TeamRotatinoHandle, 'cron', hour='1', minute='59', second='59')  # 每天凌晨1：59:59更新每天应该上班的班组



    # 这是一个独立的线程
    scheduler.start()


