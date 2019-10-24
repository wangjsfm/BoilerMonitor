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
        报警结束，删除缓存数据
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
        cache.delete(area)  # 报警结束 删除缓存


def AlermDataCatchDao(maxTag,minTag,diffValue,region,unit):
    """
        温差超限 存入redis
    :param maxTag:
    :param minTag:
    :param diffValue: 偏差值
    :param region: 数据所属区域
    """
    area = region+unit
    get_diffValue_catch = cache.get(area)
    maxValue = maxTag[0] #最大值
    minValue = minTag[0]#最小值


    #新建一条缓存信息
    if get_diffValue_catch is None :
        a=cache.set(area,{
            'maxTageName':maxTag[1],
            'maxTageDesc': maxTag[2],
            'maxTageValue':maxValue,
            'minTageName': minTag[1],
            'minTageDesc': minTag[2],
            'minTageValue':minValue,
            'beginDate': datetime.now(),
            'diffValue':diffValue, #偏差值
        },
         timeout=None,  # 永不超时
        )


    #更新缓存信息
    else:

        #若传入偏差值大于 redis缓存中的值，则更新缓存
        if diffValue > get_diffValue_catch['diffValue'] :
            get_diffValue_catch['diffValue'] = diffValue
        elif maxValue > get_diffValue_catch['maxTageValue'] :
            get_diffValue_catch['maxTageValue'] = maxValue
        elif minValue >get_diffValue_catch['minTageValue'] :
            get_diffValue_catch['minTageValue'] = minValue

        a=cache.set(area, get_diffValue_catch, timeout=None)  # 更新数据到redis




def OutOfGaugeHandleDao(maxTag,minTag,alermValue,partitionArea,unit):
    """
        温差超限处理
    :param maxTag: 最大值
    :param minTag:最小值
    :param alermValue:报警阀值
    :param partitionArea:数据所属区域
    :param unit: 机组
    """
    diffValue = maxTag[0]-minTag[0] #最大值-最小值  获得温差

    # 区域最大，最小差值大于定值，将数据更新（新建）至redis
    if  diffValue >  alermValue:
        #存入redis缓存
        AlermDataCatchDao(maxTag,minTag,alermValue,partitionArea,unit)
        #生成报警信息
        alermTextContent = unit+str(maxTag[2])+','+str(minTag[2])+',偏差'+str(diffValue)+'度'

    #无报警，删除对于区域缓存数据，并将缓存数据存入数据库
    else:
        #删除缓存及持久化
        RemoveCatch(partitionArea,unit,)



