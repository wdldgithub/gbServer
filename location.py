# coding:utf-8
################## Bayes算法优化过程 ###################
#有两个类，PreProcess, LocationMethod
#类说明：ProProcess:预处理, LocationMethod:定位方法
########################################################
from numpy import *
from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB
from sklearn import cross_validation
import numpy as np
import math

################# 预处理 ##############################
class PreProcess(object):
    @classmethod
    ##### 函数说明:从文件中读取数据 #####
    def get_file(self):
        data_list = []
        fp = open('data.txt', 'r+')
        for item in fp:
            item = eval(item)
            data_list.append(list(item))
        return data_list

    ##### 函数说明:将数据分成训练数据与测试数据 #####
    ##### data_list:原始数据 #####
    def split(self):
        data_list = self.get_file()
        num = len(data_list)
        data_value = [[]]*num #rssi数值
        data_pos_xy = [[]]*num #x, y坐标
        # 将66个bssid与xy分开
        i = 0
        for item in data_list:
            data_value[i] = item[:66] #前66个为rssi
            data_pos_xy[i] = [item[66],item[67]] #后2个为x，y
            i = i + 1
        # 转换成array
        data_list = array(data_list)
        data_value = array(data_value)
        data_pos_xy = array(data_pos_xy)
        # 进行随即分组，分成taining组，和test组
        training_value, test_value, training_pos_xy, test_pos_xy = cross_validation.train_test_split(data_value, data_pos_xy, test_size = 0.001,random_state=3)
        # 将xy分离
        test_num = len(test_pos_xy)
        train_num = len(training_value)
        # 将x，y分离
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
        return (training_value, test_value, test_pos_x, test_pos_y, training_pos_x, training_pos_y)

################# 定位方法 #############################
class LocationMethod(object):
    @classmethod
    def MyNaiveBayes(object):
        pre = PreProcess()
        (training_value, test_value, test_pos_x, test_pos_y, training_pos_x, training_pos_y) = pre.split()
        # 模型初始化
        clf_x = GaussianNB()
        clf_y = GaussianNB()
        # 进行模型的训练
        clf_x.fit(training_value, training_pos_x)
        clf_y.fit(training_value, training_pos_y)
        # 计算结果
        result_pos_x = clf_x.predict(test_value)
        result_pos_y = clf_y.predict(test_value)
        '''
        print result_pos_x
        print test_pos_x
        print result_pos_y
        print test_pos_y
        '''
        # 计算误差
        x_dis = []
        y_dis = []
        d_dis = []
        for i in range(len(result_pos_x)):
            x_dis.append(abs(result_pos_x[i] - test_pos_x[i]))
            y_dis.append(abs(result_pos_y[i] - test_pos_y[i]))
            d_dis.append(math.sqrt((result_pos_x[i]-test_pos_x[i])**2+(result_pos_y[i]-test_pos_y[i])**2))
        x = (sum(x_dis))/len(result_pos_x)
        y = (sum(y_dis))/len(result_pos_y)
        d = (sum(d_dis))/len(d_dis)
        print x, y, d
        return x, y, d

lo = LocationMethod()
lo.MyNaiveBayes()
