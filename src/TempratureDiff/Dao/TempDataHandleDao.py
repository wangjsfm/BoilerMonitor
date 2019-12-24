from datetime import datetime
from django.core.cache  import cache
from RestApi.models import DeviationAlermItem




def GetMaxMinData(areaOpcData):
    """
    筛选出最大、最小值
    :param opcData: 区域数据
    :return:
    """
    flag = 0
    maxValue = [0, '', '']  # 0：最大值，1：标签名，2:标签描述
    minvalue = [0, '', '']  # 0：最小值，1：标签名，2:标签描述

    # 从opc中获取 区域最大值，最小值
    for index, row  in areaOpcData:

        tagName = row['ItemID']
        tagDesc = row['Name']
        tagValue = round(float(row['Value']), 2)



        if tagValue < 0.01:  # 防止数据为负值
            tagValue = 0

        if flag == 0: #初始化 最大最小值

            minvalue[0] = tagValue
            minvalue[1] = tagName
            minvalue[2] = tagDesc

            maxValue[0] = tagValue
            maxValue[1] = tagName
            maxValue[2] = tagDesc

            flag =1


        if tagValue > maxValue[0]:  #判断当前数据是否为最大值
            maxValue[0] = tagValue
            maxValue[1] = tagName
            maxValue[2] = tagDesc
        elif tagValue < minvalue[0]:  #判断当前数据是否为最小值
            minvalue[0] = tagValue
            minvalue[1] = tagName
            minvalue[2] = tagDesc



    return maxValue,minvalue


def RemoveCatch(region,unit):
    """
        报警结束，持久化缓存数据
    :param region:
    """

    area = region + unit
    get_catch_data = cache.get(area)

    OPREATION_CLASSIC='1'
    # if boilerUrls.OPREATION_CLASSIC == 0:
    #     boilerUrls.OPREATION_CLASSIC = UpdataPeriodTeam()  # 更新OPREATION_CLASSIC

    if get_catch_data != None:

        beginDate = get_catch_data['beginDate']
        endDate = datetime.now()
        persistence = DeviationAlermItem(
            name =area,
            maxTageName=get_catch_data['maxTageName'],
            maxTageDesc=get_catch_data['maxTageDesc'],
            maxTageValue=get_catch_data['maxTageValue'],
            minTageName=get_catch_data['minTageName'],
            minTageDesc=get_catch_data['minTageDesc'],
            minTageValue=get_catch_data['minTageValue'],
            classic=OPREATION_CLASSIC,
            deviationValuet = get_catch_data['diffValue'],
            beginTime= beginDate,
            endTime=endDate,
            tiemDiff = (endDate-beginDate).seconds
        )
        persistence.save() # 保存到数据库
        # cache.delete(area)  # 报警结束 删除缓存

def updataCatch(maxTag,minTag,diffValue,redisData):
    """
    更新缓存数据，格式化
    :param maxTag:
    :param minTag:
    :param diffValue:
    :param redisData:
    """
    redisData['maxTageValue'] = maxTag[0]
    redisData['maxTageName'] = maxTag[1]
    redisData['maxTageDesc'] = maxTag[2]
    redisData['minTageValue'] = minTag[0]
    redisData['minTageName'] = minTag[1]
    redisData['minTageDesc'] = minTag[2]
    redisData['diffValue'] = diffValue

    return redisData







def AlermDataCatchDao(maxTag,minTag,diffValue,region,unit,alermValue):
    """
        温差超限 存入redis
    :param maxTag:
    :param minTag:
    :param diffValue: 偏差值
    :param region: 数据所属区域
    :param alermValue: 报警阀值
    """
    area = region+unit
    get_diffValue_catch = cache.get(area)
    maxValue = maxTag[0] #最大值
    minValue = minTag[0]#最小值


    if get_diffValue_catch is None:
        cache.set(area, {  # 新建一条缓存信息
            'maxTageName': maxTag[1],
            'maxTageDesc': maxTag[2],
            'maxTageValue': maxValue,
            'minTageName': minTag[1],
            'minTageDesc': minTag[2],
            'minTageValue': minValue,
            'beginDate': datetime.now(),
            'diffValue': diffValue,  # 偏差值
            'state': 0, #报警状态 1报警  0停止
        },
                  timeout=None,  # 永不超时
                  )

    else: #redis有缓存


        if (diffValue < alermValue) & (get_diffValue_catch['state'] == 1): #上一刻报警，此刻没报警，将数据保存到数据库
            # 持久化
            RemoveCatch(region, unit, )
            get_diffValue_catch['state'] = 0

        # 更新缓存信息
        elif diffValue >= alermValue :
            get_diffValue_catch['state'] = 1
            #更新数据
            get_diffValue_catch =  updataCatch(maxTag,minTag,diffValue,get_diffValue_catch)
        elif diffValue < alermValue :
            get_diffValue_catch['state'] = 0
            # 更新数据
            get_diffValue_catch = updataCatch(maxTag, minTag, diffValue, get_diffValue_catch)

            #若传入偏差值大于 redis缓存中的值，则更新缓存
        # # if diffValue > get_diffValue_catch['diffValue'] :
        # #     get_diffValue_catch['diffValue'] = diffValue
        # if maxValue > get_diffValue_catch['maxTageValue'] :
        #     get_diffValue_catch['maxTageValue'] = maxValue
        # if minValue >get_diffValue_catch['minTageValue'] :
        #     get_diffValue_catch['minTageValue'] = minValue

        cache.set(area, get_diffValue_catch, timeout=None)  # 更新数据到redis


    # #新建一条缓存信息
    # if get_diffValue_catch is None :
    #     cache.set(area,{
    #         'maxTageName':maxTag[1],
    #         'maxTageDesc': maxTag[2],
    #         'maxTageValue':maxValue,
    #         'minTageName': minTag[1],
    #         'minTageDesc': minTag[2],
    #         'minTageValue':minValue,
    #         'beginDate': datetime.now(),
    #         'diffValue':diffValue, #偏差值
    #         'state':1,
    #     },
    #      timeout=None,  # 永不超时
    #     )
    #
    #
    # #更新缓存信息
    # else:
    #
    #     #若传入偏差值大于 redis缓存中的值，则更新缓存
    #     if diffValue > get_diffValue_catch['diffValue'] :
    #         get_diffValue_catch['diffValue'] = diffValue
    #     elif maxValue > get_diffValue_catch['maxTageValue'] :
    #         get_diffValue_catch['maxTageValue'] = maxValue
    #     elif minValue >get_diffValue_catch['minTageValue'] :
    #         get_diffValue_catch['minTageValue'] = minValue
    #
    #     cache.set(area, get_diffValue_catch, timeout=None)  # 更新数据到redis
    #







def OutOfGaugeHandleDao(maxTag,minTag,alermValue,partitionArea,unit):
    """
        温差超限处理
    :param maxTag: 最大值
    :param minTag:最小值
    :param alermValue:报警阀值
    :param partitionArea:数据所属区域
    :param unit: 机组
    """
    area = partitionArea + unit
    diffValue = round((maxTag[0]-minTag[0]),2) #最大值-最小值  获得温差

    AlermDataCatchDao(maxTag,minTag,diffValue,partitionArea,unit,alermValue)

    get_diffValue_catch = cache.get(area)

    dataState = get_diffValue_catch['state']#获取数据状态

    if  diffValue < alermValue & get_diffValue_catch['state'] == dataState :#无报警，删除对于区域缓存数据，并将缓存数据存入数据库
            # 删除缓存及持久化
        RemoveCatch(partitionArea, unit, )
    elif diffValue >= alermValue:
        # 生成报警信息
        alermTextContent = unit + str(maxTag[2]) + ',' + str(minTag[2]) + ',偏差' + str(diffValue) + '度'





