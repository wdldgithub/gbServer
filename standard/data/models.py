# coding:utf_8
from django.db import models

# Create your models here.
class StandardData(models.Model):
    rssi1 = models.CharField(max_length = 10)
    rssi2 = models.CharField(max_length = 10)
    rssi3 = models.CharField(max_length = 10)
    rssi4 = models.CharField(max_length = 10)
    x = models.CharField(max_length = 30)
    y = models.CharField(max_length = 30)
####################新增加的列###################
    bssid1 = models.CharField(max_length = 30)
    bssid2 = models.CharField(max_length = 30)
    bssid3 = models.CharField(max_length = 30)
    bssid4 = models.CharField(max_length = 30)
    team = models.CharField(max_length = 30)
    class Meta:
        db_table = 'standard'


class Result(models.Model):
    x = models.CharField(max_length = 30)
    y = models.CharField(max_length = 30)
    real_x = models.CharField(max_length = 30)
    real_y = models.CharField(max_length = 30)
    bssid_team = models.CharField(max_length = 30)
    train_num = models.CharField(max_length = 30)
    test_num = models.CharField(max_length = 30)
    createtime = models.DateTimeField(auto_now = True)
#############################################################
#    alg_type = models.CharField(max_length = 30)
############################################################
    class Meta:
        db_table = 'data_result'
