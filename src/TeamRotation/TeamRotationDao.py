#coding=utf-8
"""
#Version: V 1.0
#author:  'WangSheng'
@time:2019/12/24
"""
from RestApi.models import TeamRotation
import  datetime


def TeamRotatinoHandle():
    """
        更新一天的上班情况,确定当天有那些班组上班
    """
    teamId = 0
    dbData = TeamRotation.objects.all()
    for item in dbData :
        if item.status: #找到当前是谁上班
            teamId = item.id

    #更新 上班状态

    if teamId  != 0 :

        #修改当前班的 状态
        preTeam = TeamRotation.objects.get(id=teamId)
        preTeam.status = 0
        preTeam.save()
        #将下一个班，设置为上班状态
        if  teamId == 10 :  #为最后一个的时候，需要将ID 设置为1
            preTeam = TeamRotation.objects.get(id= 1)
        else:
            preTeam = TeamRotation.objects.get(id=teamId+1)
        preTeam.status = 1
        preTeam.save() #设置新的一天，上班的班组





def GetCurrentTeam():
    """
    #
    :return:当前正在上班的值
    """
    dbData = TeamRotation.objects.all()

    team = 0  # 应该上班的班组
    nowDate = datetime.datetime.now()
    nowTime = datetime.time(nowDate.hour, nowDate.minute, nowDate.second, nowDate.microsecond) #当前时分秒
    times_2 = datetime.time(2, 0, 0, 0)
    times_9 = datetime.time(9, 0, 0, 0)
    times_17 = datetime.time(17, 0, 0, 0)
    times_0 = datetime.time(0, 0, 0, 0)

    # 当天所有应该上班的班组
    for temp in dbData:
        if temp.status:  # 找到当天是那些  值  上班

            if  nowTime.__ge__(times_2) & nowTime.__lt__(times_9):  #在2-9点
                if temp.team_1 =='3':
                    team = 1
                elif temp.team_2 == '3':
                    team = 2
                elif temp.team_3 == '3':
                    team = 3
                elif temp.team_4 == '3':
                    team = 4
                elif temp.team_5 == '3':
                    team = 5
            elif nowTime.__ge__(times_9) & nowTime.__lt__(times_17): #白班  9-17
                if temp.team_1 =='1':
                    team = 1
                elif temp.team_2 == '1':
                    team = 2
                elif temp.team_3 == '1':
                    team = 3
                elif temp.team_4 == '1':
                    team = 4
                elif temp.team_5 == '1':
                    team = 5
            elif nowTime.__ge__(times_17) :  #中班  17-2
                if temp.team_1 =='2':
                    team = 1
                elif temp.team_2 == '2':
                    team = 2
                elif temp.team_3 == '2':
                    team = 3
                elif temp.team_4 == '2':
                    team = 4
                elif temp.team_5 == '2':
                    team = 5
    return  team




