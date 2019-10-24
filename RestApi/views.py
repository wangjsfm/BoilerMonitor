from django.shortcuts import render
from django.core.cache  import cache
from django.http import JsonResponse,HttpResponse

# Create your views here.

def index(req):
    pass

def RaalDvationData(request):

    region = 'unit1_screen1' #壁温区域

    cacheData = cache.get(region)

    if cacheData != None:  # 根据点名获取缓存数据
        return JsonResponse({'responseData': cacheData})

    return JsonResponse({'responseData': {}})