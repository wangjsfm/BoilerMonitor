#coding=utf-8
"""
#Version: V 1.0
#author:  'WangSheng'
@time:2019/12/25
"""


from src.Tools.UtilTools import SecondsToHMS


def FilterDevitionHistory(startTime,endTime,seletOpreation,table):
    """
        根据开始、结束时间、值别筛选出对应数据
    :param startime: 开始时间
    :param endtime: 结束时间
    :param seletOpreation: 值别
    :param table: 对应的数据库表
    :return:
    """
    global dbData

    if  seletOpreation == '' :

        dbData = table.objects.filter(beginTime__gte=startTime, endTime__lte=endTime)
    else:
        dbData = table.objects.filter(beginTime__gte=startTime, endTime__lte=endTime,
                                                            classic__exact=seletOpreation)
    list = []
    for item  in dbData:
        list.append([
            item.name,
            item.maxTageName,
            item.maxTageDesc,
            round(item.maxTageValue,2),
            item.classic,
            item.minTageName,
            item.minTageDesc,
            round(item.minTageValue,2),
            round(item.deviationValuet,2),
            item.beginTime.strftime('%Y-%m-%d   %H:%M:%S'),
            item.endTime.strftime('%Y-%m-%d   %H:%M:%S'),
            SecondsToHMS(int(item.tiemDiff)) #将秒 转为时分秒返回

        ])
    return list




def FilterMonthlyData(month,table):
    """
    根据月份筛选对应表数据
    :param month:月份
    :param table:数据表
    :return: 返回按值筛选数据结果
    """

    dbData = table.objects.filter(beginTime__gte=month['mBegin'],endTime__lte=month['mEnd'])
    list1 = [0,0,1] #index 0: 报警次数统计，index 1：报警时长累加, index 2：值别
    list2 = [0,0,2]
    list3 = [0,0,3]
    list4 = [0,0,4]
    list5 = [0,0,5]
    for item in dbData: #按照值统计报警时长，次数
        if item.classic == '1':
           list1[0] = list1[0] +1
           list1[1] = list1[1] + item.tiemDiff
        elif item.classic == '2':
            list2[0] = list2[0] + 1
            list2[1] = list2[1] + item.tiemDiff
        elif item.classic == '3':
            list3[0] = list3[0] + 1
            list3[1] = list3[1] + item.tiemDiff
        elif item.classic == '4':
            list4[0] = list4[0] + 1
            list4[1] = list4[1] + item.tiemDiff
        elif item.classic == '5':
            list5[0] = list5[0] + 1
            list5[1] = list5[1] + item.tiemDiff


    list1[1] =  SecondsToHMS(int(list1[1])) #将秒 转为时分秒返回
    list2[1] = SecondsToHMS(int(list2[1]))  # 将秒 转为时分秒返回
    list3[1] = SecondsToHMS(int(list3[1]))
    list4[1] = SecondsToHMS(int(list4[1]))
    list5[1] = SecondsToHMS(int(list5[1]))


    return [ list1,list2,list3,list4,list5 ]



