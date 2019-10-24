#coding=utf-8
#Version: V 1.0
author: 'WangSheng'
date: '2019/3/21 14:29'


from src.Model.Dao.TempreturePointFit import TempreturePointFitClass
from src.Config import ModelData
from src.Config.TagGroupConfig import EconomizerExport,ProofExport,\
    HorizontalFlueSideWall,RearShaftWallTube38,\
    RearShaftWallTube51,LowTemperatureSuperheater,\
    PlatenSuperheater45,PlatenSuperheater51,\
    HighTemperatureSuperheater45,HighTemperatureSuperheater51,\
    LowTemperatureReheater,HighTemperatureReheater


#将各个区域的模型初始化
def TempModelInit():

    #根据厂家提供的数据 生存折线函数

    # 省煤器出口吊挂管数据
    economizerExportModle = TempreturePointFitClass(ModelData.x1,ModelData.y1)

    # 顶棚出口
    proofExportModle = TempreturePointFitClass(ModelData.x2, ModelData.y2)

    # 水平烟道侧包墙壁
    horizontalFlueSideWalltModle = TempreturePointFitClass(ModelData.x3, ModelData.y3)

    # 后竖井包墙管38温度报警拟合模型
    rearShaftWallTubeModle38 = TempreturePointFitClass(ModelData.x4, ModelData.y4)

    # 后竖井包墙管51温度报警拟合模型
    rearShaftWallTubeModle51 = TempreturePointFitClass(ModelData.x5, ModelData.y5)

    # 低温过热器出口
    lowTemperatureSuperheaterModle = TempreturePointFitClass(ModelData.x6, ModelData.y6)

    # 屏式过热器45
    platenSuperheaterModle45  = TempreturePointFitClass(ModelData.x7, ModelData.y7)

    # 屏式过热器51
    platenSuperheaterModle51 = TempreturePointFitClass(ModelData.x8, ModelData.y8)

    #高温过热器45出口
    highTemperatureSuperheaterModle45  = TempreturePointFitClass(ModelData.x9, ModelData.y9)

    #高温过热器51出口
    highTemperatureSuperheaterModle51  = TempreturePointFitClass(ModelData.x10, ModelData.y10)

    # 低温再热器出口
    lowTemperatureReheaterModle = TempreturePointFitClass(ModelData.x11, ModelData.y11)

    #高温再热器温度报警拟合模型
    highTemperatureReheaterModle = TempreturePointFitClass(ModelData.x12, ModelData.y12)

    return {
        EconomizerExport:economizerExportModle,
        ProofExport: proofExportModle,
        HorizontalFlueSideWall: horizontalFlueSideWalltModle,
        RearShaftWallTube38: rearShaftWallTubeModle38,
        RearShaftWallTube51: rearShaftWallTubeModle51,
        LowTemperatureSuperheater: lowTemperatureSuperheaterModle,
        PlatenSuperheater45: platenSuperheaterModle45,
        PlatenSuperheater51: platenSuperheaterModle51,
        HighTemperatureSuperheater45: highTemperatureSuperheaterModle45,
        HighTemperatureSuperheater51: highTemperatureSuperheaterModle51,
        LowTemperatureReheater: lowTemperatureReheaterModle,
        HighTemperatureReheater: highTemperatureReheaterModle,
    }


#
# if __name__ == '__main__':
#
#     area = 'highTemperatureSuperheaterModle45'
#     x = ModelData.x9
#     y = ModelData.y9
#     title = ModelData.title9
#
#     modelMap = TempModelInit()
#     yList = []
#     xList = np.arange(0, 40, 0.1)
#     for item in xList:
#         yList.append(modelMap[area].curveFunction(item))
#
#     plt.rcParams['font.sans-serif'] = ['SimHei']
#
#     plt.figure(1)
#     plt.title(title )
#     plt.plot(x, y)
#
#     plt.figure(2)
#     plt.title(title+ ' 拟合的折线函数')
#     plt.plot(xList, yList)
#
#     plt.show()
#
#
