#coding=utf-8
"""
#Version: V 1.0
#author:  'WangSheng'
@time:2019/12/25
"""

import datetime,calendar
from RestApi.models import TeamRotation

#将输入的秒，转为时分秒
def SecondsToHMS(seconds):

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return  str(h)+'时'+str(m)+'分'+str(s)+'秒'

#输入年月，返回该月第一天及最后一天
def MonthsProcess(str1):
    temp = str1.split('-')
    months_begin = datetime.datetime.strptime(str1, '%Y-%m')
    lastDay = calendar.monthrange(int(temp[0]), int(temp[1]))[1]  # 获得该月最后一天
    end_str = temp[0] + '-' + temp[1] + '-' + str(lastDay) + ' 23:59:59'
    months_end = datetime.datetime.strptime(end_str, '%Y-%m-%d %X')

    return {
        'mBegin':months_begin,
        'mEnd':months_end,
    }

def MonthsByDay(dateStr):
    temp = dateStr.split('-')
    lastDay = calendar.monthrange(int(temp[0]), int(temp[1]))[1]  # 获得该月最后一天
    return lastDay





#获取当前上班的班组
def getCurrentTeam():
    dbData = TeamRotation.objects.all()
    currentTeam = None
    for item in dbData :
        if item.status: #找到当前是谁上班
            pass

    return  currentTeam


