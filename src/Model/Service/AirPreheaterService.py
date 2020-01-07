#coding=utf-8
"""
#Version: V 1.0
#author:  'WangSheng'
@time:2020/01/07
"""

def LoadSo2Fit(load,so2):
    """
        根据负荷、so2返回 入炉煤硫份
    :param load:
    :param so2:
    :return:
    """
    return -0.0014193*load+0.00037522*so2+0.702842



def SulphlurTempreturFit(sulr):

    """
        根据入炉煤硫份，计算冷端综合温度
    :param sulr: 硫份
    :return:
    """
    return 13.87236099*sulr+134.55304656





def SulrPhlurAlerm(load,so2):

    """
        根据负荷，so2,生成硫份
    :param load:
    :param so2:
    :return:
    """
    sulr = LoadSo2Fit(load,so2)#入炉煤硫份
    alerm = round(
            SulphlurTempreturFit(sulr),
            2
    )  #冷端综合温度 报警定值
    return {

            'uplimit':alerm+2.5,
            'dowmlimit':alerm-2.5,
            'fitAlermValue':alerm
    }