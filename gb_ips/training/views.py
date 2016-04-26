#from django.shortcuts import render
# coding:utf-8
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.core import serializers
from django.http import HttpResponse
#from django.db.transaction import commit_on_success
from django.db import connection
from .models import TrainingRawData
from numpy import *
from collections import OrderedDict
from .postdata import datapost
#from tools.models import Result
#from postdata.py import *
import datetime
import MySQLdb
import json
import numpy as np
import requests

#########################转换数据格式#######################
class Set(object):
    @classmethod
    def get_all_time(self):# 取出所有的时间（不重复）并格式化
        time_former = []
        time_table = []
        time_former = list(TrainingRawData.objects.values('createtime').distinct())
        for item in time_former:
            time_table.append(str(item['createtime']))
        return array(time_table)
    @classmethod
    def get_all_bssid(self):# 取出所有的bssid（不重复）并格式化
        bssid_table = []
        bssid_former = list(TrainingRawData.objects.values('bssid').distinct())
        for item in bssid_former:
            bssid_table.append(item['bssid'].replace(':','').encode('utf-8'))
        return bssid_table

    @classmethod
    def get_all_data(self):# 取出所有待处理数据，并将时间和bssid格式化
        all_data = []
        for i in TrainingRawData.objects.filter(floor_id = '01'):# 仅取一楼的数据
        # 只留下bssid，rssi，x，y，createtime
            all_data.append([i.bssid, float(i.rssi), i.x, i.y, i.createtime])
        '''
        for i in TrainingRawData.objects.filter(createtime = '2016-01-20 11:01:26'):
            all_data.append([i.bssid, float(i.rssi), i.x, i.y, i.createtime])
        for i in TrainingRawData.objects.filter(createtime = '2016-01-20 11:01:25'):
            all_data.append([i.bssid, float(i.rssi), i.x, i.y, i.createtime])
        for i in TrainingRawData.objects.filter(createtime = '2016-01-20 11:01:21'):
            all_data.append([i.bssid, float(i.rssi), i.x, i.y, i.createtime])
        for i in TrainingRawData.objects.filter(createtime = '2016-01-20 11:01:23'):
            all_data.append([i.bssid, float(i.rssi), i.x, i.y, i.createtime])
        '''
        for item in all_data:# 格式化
            item[0] = item[0].replace(':','').encode('utf-8')# bssid
            item[2] = float(item[2])*250 # x坐标
            item[3] = float(item[3])*120 # y坐标
            item[4] = str(item[4])#时间
        return all_data

class Convert(object):
    @classmethod
    def find(self):# 转换格式
        bssid_table = Set.get_all_bssid()# 取bssid列表
        time_table = Set.get_all_time()# 取时间列表
        all_data = Set.get_all_data()# 取所有待处理数据
        back_data = [] #最后返回的处理完的数据
        # 建立一个字典索引存放bssid
        bssid_table = Set.get_all_bssid()
        index_table = range(0,66)
        bssid_dic = dict(zip(bssid_table, index_table))
        for item in time_table:
            temp = []
            for i in all_data:
                if i[4] == item:# 按照time来搜索all_data中的值
                    temp.append(i)
            if len(temp):
                total = hstack((np.zeros(66), np.ones(2)))# 同一时间下66个rssi和x，y坐标
                for j in temp:
                    total[66:68] = j[2:4]# 存x,y
                    position = bssid_dic[j[0]]# i[0]为bssid值,根据bssid找出该rssi在total中的位置
                    total[position] = j[1]# i[1]为rssi
                back_data.append(list(total))
        return back_data

@csrf_exempt
def run(request):
    co = Convert()
    back = json.dumps({'data':co.find()})
    requests.post('http://120.25.86.215:9300/regression/', {'data':back})
    return HttpResponse(back)

#############################################################

'''
##################接受客户端数据并存入TrainingRawData表#####################
@csrf_exempt
def index(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        data = json.loads(data)#['data']
#        print data
        #解析数据
        for item in data:
            rssi = item['rssi']
            x = item['x']
            y = item['y']
            bssid = item['bssid']
            ssid = item['ssid']
            deviceid = item['device_id']
            market_id = item['market_id']
            floor_id = item['floor_id']
            if ssid == 'GuangBai':
                is_create, obj = TrainingRawData.create(ssid=ssid, bssid=bssid, rssi=str(rssi), device_id=deviceid, market_id=market_id, floor_id=floor_id, x=str(x), y=str(y))
#                print obj
                obj.save()
#            TrainingRawDta.objects.create(rssi=rssi,x=x,y=y,bssid=bssid,ssid=ssid,sessionid=sessionid,deviceid=deviceid,createtime=createtime)
    return HttpResponse('Done')
################################################################################
        for i in TrainingRawData.objects.filter(createtime = '2016-01-20 11:01:26'):
            all_data.append([i.bssid, float(i.rssi), i.x, i.y, i.createtime])
        for i in TrainingRawData.objects.filter(createtime = '2016-01-20 11:01:25'):
            all_data.append([i.bssid, float(i.rssi), i.x, i.y, i.createtime])
        for i in TrainingRawData.objects.filter(createtime = '2016-01-20 11:01:21'):
            all_data.append([i.bssid, float(i.rssi), i.x, i.y, i.createtime])
        for i in TrainingRawData.objects.filter(createtime = '2016-01-20 11:01:23'):
            all_data.append([i.bssid, float(i.rssi), i.x, i.y, i.createtime])


####################向tools_result表中存入计算结果#######################
def result(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        data = json.loads(data)
        print data
        k = data['k']
        test_x = data['test_x']
        test_y = data['test_y']
        result_x = data['result_x']
        result_y = data['result_y']
        for i in len(test_x):
             Result.objects.create(k=k,test_x=test_x[i],test_y=test_y[i],result_x=result_x[i],result_y=result_y[i])
             return HttpResponse(json.dumps('Done'))

###############################################################################
        i = 0
        while i<4:
            Result.objects.create(k=k,test_x=test_x[i],test_y=test_y[i],result_x=result_x[i],result_y=result_y[i])
            i = i+1
        return HttpResponse(json.dumps('Done'))

##############################接受算法的请求并返回数据####################
@csrf_exempt
def datarequest(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        data = json.loads(data)
        for item in data:
            #如果item=bssid返回所有bssid值并去重
            if item == 'bssid':
                if data[item] == 'True':
                    bssidtable = TrainingRawData.objects.values('bssid').distinct()
                    table = []
                    for item in bssidtable:
                        table.append(item['bssid'])
            #如果item=bssid_list，根据bssid_list的值返回相应数据
            elif item == 'bssid_list':
                table = []
                bssidtable1= []
                for i in data['bssid_list']:
                    bssidtable = serializers.serialize("json",TrainingRawData.objects.filter(bssid = i))
                    bssidtable1 = bssidtable1+json.loads(bssidtable)
                for item in bssidtable1:
                    table.append(item['fields'])
            #如果item=device_id，返回所有session值并去重复
            elif item == 'floor_id':#根据接收到bssid的值返回该bssid值的所有数据
                if data[item] == 'True':
                    bssidtable = TrainingRawData.objects.values('floor_id').distinct()
#                    global table
#                    table = []
                    for item in bssidtable:
                        table.append(item['floor_id'])
    return HttpResponse(json.dumps(table))
'''
'''
#取出所有数据
@csrf_exempt
def alldata (request):
    b_list=[]
    data=[]
    temp=[]
    d=[]
    result=[]
    rssi_list=[]
    xyb_list=TrainingRawData.objects.values('x','y','bssid').distinct()
    b_list=TrainingRawData.objects.values('bssid').distinct()

    for item in xyb_list:
        l1 =
        l2 = [0]*66
        dic_temp = zip(l1,l2)#创建字典存放rssi，并全部设置为0
        for i in TrainingRawData.objects.filter(x=item['x'], y=item['y'], bssid=item['bssid']):
            temp.append(float(i.rssi))
            print temp
            bssid = i.bssid
            r = int(sum(temp)/len(temp))
            print r
            dic_temp[bssid] = r
            print dic_temp
        dic_temp = #加入x与y
        rssi_list.append(dic_temp)
    return HttpResponse('Done')

    flag = request.POST.get('data')
    flag = json.loads(flag)
    #print flag
    table = []
#    global table
    if flag['data'] == 'True':
        btable = serializers.serialize("json",Result.objects.all())
        btable = json.loads(btable)
        for item in btable:
            table.append(item['fields'])
            #print table
    return HttpResponse(json.dumps(table))
'''

