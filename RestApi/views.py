from django.core.cache  import cache
from django.http import JsonResponse
import  json
from src.TeamRotation.TeamRotationDao import  GetCurrentTeam
from RestApi import models
from datetime import datetime
from src.Tools.UtilTools import MonthsProcess
from src.Api.ApiService.DataFilterService import FilterDevitionHistory,FilterMonthlyData
from src.Model.Service.AirPreheaterService import SulrPhlurAlerm
# Create your views here.



def index(req):
    pass

def RaalDvationData(request):
    """
    返回1、2机组实时温差数据
    :param request:
    :return:
    """
    # region = 'unit1_screen1' #壁温区域
    recive = json.loads(request.body)
    unit = 1 #默认是一号机组
    if  recive['unit'] != None :
        unit = str(recive['unit'])
    region = 'unit'+unit+'_screen'+unit  # 壁温区域

    cacheData = cache.get(region)

    if cacheData != None:  # 根据点名获取缓存数据
        return JsonResponse({'data': cacheData
                             })
    else:
        pass
    return JsonResponse({'data': None})



def GetTeam(request):
    """
    返回正在上班的值
    :type request: object
    """
    team = GetCurrentTeam()
    return JsonResponse({'data':team})




def GetDevitionHistory(request):
    """
    #   返回 温差  报警历史数据
    :param request:
    :return:
    """
    global  dbData
    recive =  json.loads(request.body)
    startTime =datetime.strptime( recive['startTime'], '%Y-%m-%d %X')
    endTime = datetime.strptime( recive['endTime'], '%Y-%m-%d %X')
    seletOpreation = recive['selectOpr']
    filterData =FilterDevitionHistory(startTime,endTime,seletOpreation,models.DeviationAlermItem) #筛选后的数据

    return JsonResponse({ 'data':filterData})


def GetDevitionAseete(request):
    """
    返回温差 考核数据
    :param request:
    :return:
    """
    recive = json.loads(request.body)
    montDic = MonthsProcess(recive['months'])
    filterData = FilterMonthlyData(montDic, models.DeviationAlermItem)  # 数据筛选

    return JsonResponse({'data': filterData})


def GetOpreationHistory(request):
    """
    获取壁温历史数据
    :param request:
    :return:
    """
    global dbData
    recive = json.loads(request.body)
    startTime = datetime.strptime(recive['startTime'], '%Y-%m-%d %X')
    endTime = datetime.strptime(recive['endTime'], '%Y-%m-%d %X')
    seletOpreation = recive['selectOpr']
    filterData = FilterDevitionHistory(startTime, endTime, seletOpreation, models.TempratureAlermValue)  # 筛选后的数据
    return JsonResponse({'data': filterData})

def GetOpreationAseete(request):
    """
        #按照值别 壁温  返回运行考核数据
    :param request:
    :return:
    """
    recive = json.loads(request.body)
    montDic = MonthsProcess(recive['months'])
    filterData = FilterMonthlyData(montDic,models.TempratureAlermValue)#数据筛选
    return  JsonResponse({ 'data':filterData})



def GetAirPreheater(request):
    """
        返回空预器冷端温度  报警定值
    :param req:
    :return:
    """
    # recive = json.loads(request.body)
    # startTime = datetime.strptime(recive['startTime'], '%Y-%m-%d %X')
    # endTime = datetime.strptime(recive['endTime'], '%Y-%m-%d %X')
    alermValue = None
    if request.method == 'GET':
        load =float( request.GET.get('load'))
        so2 = float(request.GET.get('so2'))
        alermValue = SulrPhlurAlerm(load, so2)


    return JsonResponse( {'data':alermValue})





