# coding:utf-8
'''
from numpy import *
x = [12,12,12,12,12,12]
s = sum(x)
print s
print s/6
'''
from numpy import *
from sklearn.datasets import load_iris
# from matplotlib.pyplot as plt

iris = load_iris()
samples = iris.data
target = iris.target
print "This is samples:", samples
print "This is target:", target

from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
classifier.fit(samples, target)

x = classifier.predict([5, 3, 5, 2.5])
print x
