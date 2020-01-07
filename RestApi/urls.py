from django.conf.urls import url
from . import views

urlpatterns=[

    url(r'^index', views.index),
    url(r'^realTempDiff', views.RaalDvationData), #获取温差报警数据
    url(r'^getTeam', views.GetTeam),#获取当前值
    url(r'^getSulr', views.GetAirPreheater),#获取空预器报警值
]
