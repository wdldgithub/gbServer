# coding:utf-8
import matplotlib
import matplotlib.pyplot as plt
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .models import StandardData,Result
from django.db import connection
from numpy import *
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation
from pylab import *

import math
import MySQLdb
import json
import datetime
import random

##################### 接受已转换好格式的数据#################
@csrf_exempt
def accept(request):
    if request.method == 'POST':
        receive_data = request.POST.get('receive_data')
        receive_data = json.loads(receive_data)
#接受多组数据
        for i in range(len(receive_data)):
            get_data = receive_data[i]
#每一组数据都为数组，数组中有两个元素，第一个存放四个rssi与xy，第二个元素存放4个ap的bssid
            data = get_data[0]
            for item in data:
                if item == 'rssi1':
                    rssi1 = data['rssi1']
                elif item == 'rssi2':
                    rssi2 = data['rssi2']
                elif item == 'rssi3':
                    rssi3 = data['rssi3']
                elif item == 'rssi4':
                    rssi4 = data['rssi4']
                elif item == 'x':
                    x = data['x']
                elif item == 'y':
                    y = data['y']
            bssid = get_data[1]
#设定组号，组号为日期加4位随机数
            t = datetime.data.today()
            team = str(t.year) + str(t.month) + str(t.day) + str(random(0,9999))
#将数据存入数据库
            '''
            for i in range(len(x)):
                StandardData.objects.create(rssi1=rssi1[i], rssi2=rssi2[i], rssi3=rssi3[i], rssi4=rssi4[i], x=x[i], y=y[i], bssid1=bssid['bssid1'], bssid2=bssid['bssid2'], bssid3=bssid['bssid3'], bssid4=bssid['bssid4'], team=team)
            '''
    return HttpResponse('Done')

########################### 算法##########################
@csrf_exempt
def regression(request):
# 载入数据
    data_list = []
    for i in StandardData.objects.all():
        data_list.append([float(i.rssi1), float(i.rssi2), float(i.rssi3), float(i.rssi4), i.x, i.y])
#记录bssid的组号
    team = StandardData.objects.values('team').distinct()
    team = team[0]
    team = team['team']
    num = len(data_list)
    data_value = [[]]*num
    data_pos_xy = [[]]*num
# 将4个bssid与xy分开
    i = 0
    for item in data_list:
        data_value[i] = [item[0],item[1],item[2],item[3]]
        data_pos_xy[i] = [item[4],item[5]]
        i = i+1
# 转换成array
    data_list = array(data_list)
    data_value = array(data_value)
    data_pos_xy = array(data_pos_xy)
# 进行随即分组，分成taining组，和test组
    training_value, test_value, training_pos_xy, test_pos_xy = cross_validation.train_test_split(data_value, data_pos_xy, test_size = 0.1,random_state=3)
# 将xy分离
    test_num = len(test_pos_xy)
    train_num = len(training_value)
    test_pos_x = []
    test_pos_y = []
    training_pos_x = []
    training_pos_y = []
    for i in range(len(test_pos_xy)):
        test_pos_x.append(test_pos_xy[i][0])
        test_pos_y.append(test_pos_xy[i][1])
    for i in range(len(training_pos_xy)):
        training_pos_x.append(training_pos_xy[i][0])
        training_pos_y.append(training_pos_xy[i][1])
# 进行模型的训练
    clf_x = LogisticRegression()
    clf_y = LogisticRegression()
    clf_x.fit(training_value, training_pos_x)
    clf_y.fit(training_value, training_pos_y)
# 计算结果
    result_pos_x = clf_x.predict(test_value)
    result_pos_y = clf_y.predict(test_value)
    print result_pos_x
    print result_pos_y
    return HttpResponse('Done')

# 将计算结果存入数据库
'''
    for i in range(test_num):
        Result.objects.create(x=result_pos_x[i], y=result_pos_y[i], real_x=test_pos_x[i], real_y=test_pos_y[i],  test_num=test_num, train_num=train_num,  bssid_team=team)
    return HttpResponse('Done')
'''
#############################################################
#############################################################

###########################计算误差##########################
@csrf_exempt
def calculate(request):
    x_list = []
    y_list = []
    x_real_list = []
    y_real_list = []
    for i in Result.objects.filter(test_num=6):
        x_list.append(float(i.x))
        y_list.append(float(i.y))
        x_real_list.append(float(i.real_x))
        y_real_list.append(float(i.real_y))
    x_dis = []
    y_dis = []
    for i in range(len(x_list)):
        x_dis.append(abs(x_list[i] - x_real_list[i]))
        y_dis.append(abs(y_list[i] - y_real_list[i]))
    x = (sum(x_dis))/len(x_list)
    y = (sum(y_dis))/len(y_list)
    print x,y
###################画图######################
    plt.title('temp')
    plt.xlabel('x axis')
    plt.ylabel('y axis')
    plt.scatter(x_list,y_list,marker='s',color='r',s=150)
    plt.scatter(x_real_list,y_real_list,marker='s',color='y',s=150)
    for i in range(len(x_list)):
        x = [x_list[i],x_real_list[i]]
        y = [y_list[i],y_real_list[i]]
        plt.plot(x,y,'b')
    plt.show()
    return HttpResponse('Done')

