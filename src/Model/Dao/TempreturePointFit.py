#coding=utf-8
#Version: V 1.0
author: 'WangSheng'
date: '2019/3/21 14:27'



class TempreturePointFitClass:

    # kList = []
    # bList = []

    #初始化时就将K、B参数设置好
    #输入参数是，首尾多两条数据
    def __init__(self,x,y):
        self.x = x
        self.kList =[]
        self.bList=[]
        if len(x) == len(y):
            for i in range(len(x)):
                if i + 1 < len(x):
                    k = (y[i] - y[i + 1]) / (x[i] - x[i + 1])
                    b = y[i] - (x[i] * k)
                    self.kList.append(k)
                    self.bList.append(b)
        else:
            raise ValueError('输入数据长度，不一致')

    #根据返回温度定值  y= k x +b 分段函数
    def curveFunction(self,presure,k=1):

        for i in range(len(self.x)):
            if i + 1 < len(self.x):
                if self.x[i] <= presure <= self.x[i + 1]:
                    y = self.kList[i] * presure + self.bList[i]
                    return y*k

