from django.db import models

# Create your models here.


class OvertemperatureRecord(models.Model):
    """
    超温点 点表
    """
    name = models.CharField(db_column='name', max_length=100)#超温标签名
    desc = models.CharField(db_column='desc', max_length=300, blank=True, null=True)  # 超温标签描述
    area = models.CharField(db_column='area', max_length=50, blank=True, null=True)#超温标签所在区域（管组）
    classic = models.CharField(db_column='classic', max_length=50, blank=True, null=True)  # 值别
    maxValue =models.DecimalField(db_column='maxValue', max_digits=18, decimal_places=4, blank=True, null=True)#最大值
    thresholdValuet = models.DecimalField(db_column='thresholdValuet', max_digits=18, decimal_places=4, blank=True, null=True)#定值
    beginTime = models.DateTimeField(db_column='beginTime')#超温开始时间
    endTime = models.DateTimeField(db_column='endTime')#超温结束时间
    tiemDiff = models.DecimalField(db_column='tiemDiff', max_digits=18, decimal_places=4, blank=True, null=True) #超温时长

    class Meta:
        db_table = 'OverTemperature'


class DeviationAlermItem(models.Model):
    name = models.CharField(db_column='name', max_length=100)#报警区域名
    maxTageName = models.CharField(db_column='maxTageName', max_length=100)#报警区域名
    maxTageDesc = models.CharField(db_column='maxTageDesc', max_length=100)  # 报警区域名
    maxTageValue = models.DecimalField(db_column='maxTageValue', max_digits=18, decimal_places=4, blank=True, null=True)  # 最大值
    classic = models.CharField(db_column='classic', max_length=50, blank=True, null=True)  # 值别
    minTageName = models.CharField(db_column='minTageName', max_length=100)  # 报警区域名
    minTageDesc = models.CharField(db_column='minTageDesc', max_length=100)  # 报警区域名
    minTageValue = models.DecimalField(db_column='minTageValue', max_digits=18, decimal_places=4, blank=True, null=True)  # 最小值
    deviationValuet = models.DecimalField(db_column='deviationValuet', max_digits=18, decimal_places=4, blank=True, null=True)#偏差值
    beginTime = models.DateTimeField(db_column='beginTime')#报警开始时间
    endTime = models.DateTimeField(db_column='endTime')#报警结束时间
    tiemDiff = models.DecimalField(db_column='tiemDiff', max_digits=18, decimal_places=4, blank=True, null=True) #报警时长


    class Meta:
        db_table = 'DeviationAlermItem'




