# coding:utf-8
from numpy import *
from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB
import numpy as np
import math
# from matplotlib.pyplot as plt

iris = load_iris()
samples = iris.data
target = iris.target
# print "This is samples:", samples
# print "This is target:", target

# from sklearn.linear_model import LogisticRegression
# classifier = LogisticRegression()
'''
# sklearn bayes
classifier = GaussianNB()
classifier.fit(samples, target)
x = classifier.predict([5, 3, 5, 2.5])
print x
'''

class MyBayes(object):
    @classmethod
    def gaussion(self, a, mean ,std):
        return (1/(sqrt(2*pi)*std))*exp(-((a-mean)**2)/(2*std**2))

    @classmethod
    def choose_max(self, a, b ,c):
        key = 4
        if a>b and a>c:
            key = 0
        elif b>a and b>c:
            key = 1
        elif c>a and c>b:
            key = 2
        return key

    @classmethod
    def MainProcess(self):
        #列分割
        training_a1 = []
        training_a2 = []
        training_a3 = []
        training_a4 = []
        for item in samples:
            training_a1.append(float(item[0]))
            training_a2.append(float(item[1]))
            training_a3.append(float(item[2]))
            training_a4.append(float(item[3]))
        training_a1 = array(training_a1)
        training_a2 = array(training_a2)
        training_a3 = array(training_a3)
        training_a4 = array(training_a4)

        #3轮50个a,分别求y=0,1,2时a1,a2,a3,a4的均值与标准差
        #组成一个二维数组,行为y，列为ai_mean/std, 3行8列
        y1_mean_1 = np.mean(training_a1[:50])
        y1_mean_2 = np.mean(training_a2[:50])
        y1_mean_3 = np.mean(training_a3[:50])
        y1_mean_4 = np.mean(training_a4[:50])
        y1_std_1 = np.std(training_a1[:50])
        y1_std_2 = np.std(training_a2[:50])
        y1_std_3 = np.std(training_a3[:50])
        y1_std_4 = np.std(training_a4[:50])
        y2_mean_1 = np.mean(training_a1[50:100])
        y2_mean_2 = np.mean(training_a2[50:100])
        y2_mean_3 = np.mean(training_a3[50:100])
        y2_mean_4 = np.mean(training_a4[50:100])
        y2_std_1 = np.std(training_a1[50:100])
        y2_std_2 = np.std(training_a2[50:100])
        y2_std_3 = np.std(training_a3[50:100])
        y2_std_4 = np.std(training_a4[50:100])
        y3_mean_1 = np.mean(training_a1[100:150])
        y3_mean_2 = np.mean(training_a2[100:150])
        y3_mean_3 = np.mean(training_a3[100:150])
        y3_mean_4 = np.mean(training_a4[100:150])
        y3_std_1 = np.std(training_a1[100:150])
        y3_std_2 = np.std(training_a2[100:150])
        y3_std_3 = np.std(training_a3[100:150])
        y3_std_4 = np.std(training_a4[100:150])

        #待分类样本为[5, 3, 5, 2.5]
        #分别计算P(a1|y1), P(a1|y2), P(a1|y3)
        #data = [5, 3, 5, 2.5] # test data
        #data = [4.9, 2.8, 4.6, 1.5] #type 0
        data = [5.4, 3.4, 1.7, 0.2] #type 0
        #data = [6.5, 2.8, 4.6, 1.5] #type 1
        #data = [6.2, 3.4, 5.4, 2.3] #type 2

        P_a1_y1 = self.gaussion(data[0], y1_mean_1, y1_std_1)
        # P_a1_y1 = (1/(sqrt(2*pi)*y1_std_1))*exp(-((data[0]-y1_mean_1)**2)/(2*y1_std_1**2))
        P_a1_y2 = (1/(sqrt(2*pi)*y2_std_1))*exp(-((data[0]-y2_mean_1)**2)/(2*y2_std_1**2))
        P_a1_y3 = (1/(sqrt(2*pi)*y3_std_1))*exp(-((data[0]-y3_mean_1)**2)/(2*y3_std_1**2))

        P_a2_y1 = (1/(sqrt(2*pi)*y1_std_2))*exp(-((data[1]-y1_mean_2)**2)/(2*y1_std_2**2))
        P_a2_y2 = (1/(sqrt(2*pi)*y2_std_2))*exp(-((data[1]-y2_mean_2)**2)/(2*y2_std_2**2))
        P_a2_y3 = (1/(sqrt(2*pi)*y3_std_2))*exp(-((data[1]-y3_mean_2)**2)/(2*y3_std_2**2))

        P_a3_y1 = (1/(sqrt(2*pi)*y1_std_3))*exp(-((data[2]-y1_mean_3)**2)/(2*y1_std_3**2))
        P_a3_y2 = (1/(sqrt(2*pi)*y2_std_3))*exp(-((data[2]-y2_mean_3)**2)/(2*y2_std_3**2))
        P_a3_y3 = (1/(sqrt(2*pi)*y3_std_3))*exp(-((data[2]-y3_mean_3)**2)/(2*y3_std_3**2))

        P_a4_y1 = (1/(sqrt(2*pi)*y1_std_4))*exp(-((data[3]-y1_mean_4)**2)/(2*y1_std_4**2))
        P_a4_y2 = (1/(sqrt(2*pi)*y2_std_4))*exp(-((data[3]-y2_mean_4)**2)/(2*y2_std_4**2))
        P_a4_y3 = (1/(sqrt(2*pi)*y3_std_4))*exp(-((data[3]-y3_mean_4)**2)/(2*y3_std_4**2))

        #P(y1|x),P(y2|x),P(y3|x)
        P_y1_x = P_a1_y1 * P_a2_y1 * P_a3_y1 * P_a4_y1
        P_y2_x = P_a1_y2 * P_a2_y2 * P_a3_y2 * P_a4_y2
        P_y3_x = P_a1_y3 * P_a2_y3 * P_a3_y3 * P_a4_y3

        return self.choose_max(P_y1_x, P_y2_x, P_y3_x)
        # return key


my = MyBayes()
print my.MainProcess()
