#coding=utf-8
#Version: V 1.0
author: 'WangSheng'
date: '2019/6/2 15:48'
from datetime import datetime


def GroupDataEvaluation():

    pass





def TempreatureDiffHandle(dataList,diffThresholdValuet,unit,redisClient,groupName):
    """

     :param dataList: 壁温数据
    :param diffThresholdValuet: 壁温温差定值r
    :param unit: 机组号
    :param redisClient:  redis客户端
    :param groupName:  区域名称
    :return:
    """
    maxValue=[0,'','']  # 0：最大值，1：标签名，2:标签描述
    minvalue = [0,'','']   # 0：最小值，1：标签名，2:标签描述
    alermTextContent = None

    flag = 0


    # 从opc中获取 区域最大值，最小值
    for item in dataList:
        tagName = item[0]
        tagDesc = item[2]
        tagValue = round(float(item[1]), 2)

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

    diffValue = round(maxValue[0] - minvalue[0] , 2)

    # 区域最大，最小差值大于定值，将数据更新（新建）至redis
    if  diffValue >  diffThresholdValuet:

        #存入redis缓存
        DiffCatch(maxValue,minvalue,diffValue,redisClient,groupName,unit)
        # alermRedisHandle(areaTage,diffValue,maxValue,minvalue )

        #生成报警信息
        alermTextContent = unit+str(maxValue[2])+','+str(minvalue[2])+',偏差'+str(diffValue)+'度'
        # print(alermTextContent)

    #无报警，删除对于区域缓存数据，并将缓存数据存入数据库
    else:
        #删除缓存及持久化
        # removeCatch(areaTage)
        pass

    #返回报警信息
    return  alermTextContent




def DeleteCatch(tagName,redisClient):
    """
        删除redis中标签对应的缓存数据
    :param tagName:
    :param redisClient:
    """
    pass





def DiffCatch(maxValueList,minValueList,diffValue,redisClient,groupName,unit):
    """
      达到报警定值的标签存入redis
    :param maxList: 最大值相关信息
    :param minList: 最小值相关信息
    :param diffValue:  最大、最小值的差值
    :param groupName:区域名称
    """
    alermData = {
            'maxTageName':maxValueList[1],
            'maxTageDesc': maxValueList[2],
            'maxTageValue':maxValueList[0],
            'minTageName': minValueList[1],
            'minTageDesc': minValueList[2],
            'minTageValue':maxValueList[0],
            'beginDate': str(datetime.now()),
            'diffValue':diffValue, #偏差值
            'status':'1'
    }

    maxValue = maxValueList[0]
    minValue = minValueList[0]
    print(type(maxValue))
    cachStatus = redisClient.exists(groupName+unit)  # 1.存在   0.不存在  该条数据是否存在于redis
    cachData = redisClient.hgetall(groupName+unit)
    dataStatus = '0'


    if cachData:
        dataStatus = str(cachData[b'status'], encoding="utf8")  # 该条记录是否被运行确认

    if cachStatus == 0: #无相同名称数据，则新建记录
        redisClient.hmset(groupName+unit, alermData)

    elif cachStatus == 1: #已有记录在redis，更新记录
        if dataStatus == '1':#报警未确认，则更新记录   (  报警确认后，在固定周期内部再更新数据）


            # 若传入偏差值大于 redis缓存中的值，则更新缓存
            if diffValue > float(cachData[b'diffValue']):
                cachData[b'diffValue'] = diffValue
            elif maxValue > float(cachData[b'maxTageValue']):
                cachData[b'maxTageValue'] = maxValue
            elif minValue > float(cachData[b'minTageValue']):
                 cachData[b'minTageValue'] = minValue

            redisClient.hmset(groupName+unit, cachData)  # 更新记录





def GetOpcDataClassic(opcData,areaGroup,unit):
    """
    将标区域组里面的所有区域 数据组合在一起
    :param opcData: opc数据
    :param areaGroup: 区域组
    :param unit: 获取数据 所属机组
    :return:
    """
    dataList = []
    for tagItem in areaGroup:
        for item in opcData[tagItem+'_'+unit]:
            dataList.append(item)

    return  dataList








