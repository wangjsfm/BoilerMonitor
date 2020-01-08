#coding=utf-8
"""
#Version: V 1.0
#author:  'WangSheng'
@time:2020/01/07
"""

from src.Model.Service.AirPreheaterService import SulrPhlurAlerm
from src.AirPreheater.AirPreheaterDao import OverTempretureHandle,SaveAlerm


def AirPreaheaterMonit():
    """
        空预器冷端温度 监控配置
    """
    load_1 = 400
    so2_1 = 3483
    currentTemp_1 = 155

    load_2 = load_1
    so2_2 = so2_1
    currentTemp_2 = currentTemp_1

    alermValue_1 = SulrPhlurAlerm(load_1,so2_1)#报警定制
    alermValue_2 = SulrPhlurAlerm(load_2, so2_2)  # 报警定制

    AirConfig(currentTemp_1,alermValue_1,'a_1')#1号机组 A侧   airpreheater_a_1

    AirConfig(currentTemp_1, alermValue_1, 'b_1')  # 1号机组 B侧  airpreheater_b_1

    AirConfig(currentTemp_2, alermValue_2, 'a_2')#2号机组  A侧
    AirConfig(currentTemp_2, alermValue_2, 'b_2')  # 2号机组  B侧




def AirConfig(airTempratue,alermValue,unit):
    """
        机组 空预器报警 配置
    :param airTempratue: 空预器温度当前值
    :param alermValue:报警定制
    :param unit:机组信息
    """
    areaName = 'airpreheater_' + unit  # 空预器 A、B测 以及机组名

    if  airTempratue < alermValue['dowmlimit'] : #当前温度 低于下限

        OverTempretureHandle(airTempratue,areaName,'le')

    elif airTempratue >   alermValue['uplimit'] : #当前温度 高于上限
        OverTempretureHandle(airTempratue,areaName, 'ge')

    else:
        #持久化，保存到数据库

        SaveAlerm(areaName)
























