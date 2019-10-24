from django.conf.urls import url
from . import views

urlpatterns=[

    url(r'^index', views.index),
    url(r'^realTempDiff', views.RaalDvationData), #获取温差报警数据
    # url(r'^getGrq', views.get_grq_mean_value),
    # url(r'^postClassic', views.persisteOpreation),
    # url(r'^getClassic',views.getOpreation),
    # url(r'^getRealAlerm',views.geteRaalAlarmData),
    # url(r'^getDvationAlerm',views.geteRaalDvationData),#获取redis实时偏差报警数据
    # url(r'^getHistoryData',views.getHistoryDatae), #获取 壁温 历史数据
    # url(r'^getDevitionHistory',views.getDevitionHistory), #获取 温差 历史数据
    # url(r'^getAssessData',views.getOpreationAseete),#壁温考核数据
    # url(r'^getDevitionAssess', views.getOpreationDeviationAseete),#温差考核数据
    # # url(r'^signin', views.signin),
    # url(r'^users',views.resUsers),
    # url(r'^currentUser',views.resCurentUser),
    # url(r'^curentCunter',views.getCurentCunter), #当前报警条数
    # url(r'^monthsCunter',views.getMonthsCunter), #当前报警条数
    # url(r'^allCunter',views.getAllClassicCunter), #当月壁温 报警条数统计Gradient classification
    # url(r'^allDevitionCunter',views.getAllDeviationCunter),#当月温差 报警条数统计
    # url(r'^gradkind', views.gradAnalysis), #返回温差梯度分析
]
