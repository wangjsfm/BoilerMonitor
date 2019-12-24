from django.shortcuts import render
from django.core.cache  import cache
from django.http import JsonResponse,HttpResponse
import  json
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