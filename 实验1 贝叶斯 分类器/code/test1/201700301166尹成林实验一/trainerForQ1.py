# 编写日期 2019/10/21
# 编写人 尹成林
# 学号 201700301166
# 实验 贝叶斯实验第1问

import numpy as np
from numpy.linalg import cholesky
import matplotlib.pyplot as plt
import math

# 定义数据
c = math.sqrt(2*math.pi)
posim = 10000
antisin  = 20000

def makepodata(m1, m2, s1, s2, s3, s4):
    sampleNo = posim;
    mu = np.array([[m1, m2]])
    Sigma = np.array([[s1, s2], [s3, s4]])
    R = cholesky(Sigma)
    s = np.dot(np.random.randn(sampleNo, 2), R) + mu
    return s

def makeantidata(m1, m2, s1, s2, s3, s4):
    sampleNo = antisin;
    mu = np.array([[m1, m2]])
    Sigma = np.array([[s1, s2], [s3, s4]])
    R = cholesky(Sigma)
    s = np.dot(np.random.randn(sampleNo, 2), R) + mu
    return s

def getu(s):
    h = np.mean(s, axis=0)
    return h

def gets(s):
    h = np.var(s, axis=0)
    return h

# 计算先验概率
def getPxc (num, u, s):
    p = (1/(c*math.sqrt(s)))*pow((math.e),(-(num-u)*(num-u)/(2*s)))
    return p

# 计算后验概率
def getPcx(c,u1,u2,s1,s2,num1,num2):
    p1 = getPxc(num1, u1, s1)
    p2 = getPxc(num2, u2, s2)
    if c == 1:
        return (1/3)*p1
    else:
        return (2/3)*p2

# 最小错误率计算和返回判断
def getminfau(num1, num2, u, s):
    p1 = getPcx(1, u[0], u[1], s[0], s[1], num1, num2)
    p2 = getPcx(2, u[2], u[3], s[2], s[3], num1, num2)
    print("数据为正样本的概率为{}".format(p1))
    print("数据为负样本的概率为{}".format(p2))
    if p1>p2:
        return 1
    else:
        return 2

# 最小风险判断
def getminrisk(num1, num2, u, s, risk):
    p1 = getPcx(1, u[0], u[1], s[0], s[1], num1, num2)*risk[0]
    p2 = getPcx(2, u[2], u[3], s[2], s[3], num1, num2)*risk[1]
    print("数据为正样本的风险为{}".format(p2))
    print("数据为负样本的风险为{}".format(p1))
    if p1>p2:
        return 1
    else:
        return 2

if __name__ == "__main__":
    u = []
    s = []
    for i in range(2):
        for i1 in range(2):
            if i==0:
                uuu = input("请输入正样本第{}维的均值".format(i1+1))
                u.append(int(uuu))
                u1,u2 = input("请输入正样本第{}维的方差".format(i1 + 1)).split()
                s.append(int(u1))
                s.append(int(u2))
            if i==1:
                uuu = input("请输入负样本第{}维的均值".format(i1+1))
                u.append(int(uuu))
                u1, u2 = input("请输入负样本第{}维的方差".format(i1 + 1)).split()
                s.append(int(u1))
                s.append(int(u2))
    risk = [0.6, 0.4]
    print("************************产生样本并训练中***********************")
    data1 = makepodata(
        u[0], u[1], s[0], s[1], s[2], s[3]
    )
    data2 = makeantidata(
        u[2], u[3], s[4], s[5], s[6], s[7]
    )
    U1 = getu(data1)
    U2 = getu(data2)
    S1 = gets(data1)
    S2 = gets(data2)
    print("************************训练完成***********************")
    while 1:
        a, b = input("请输入一个二维向量(输入a a停止)\n").split()
        a = int(a)
        b = int(b)
        UUU = []
        for i in U1:
            UUU.append(i)
        for i in U2:
            UUU.append(i)
        SSS = []
        for i in S1:
            SSS.append(i)
        for i in S2:
            SSS.append(i)
        print("最小风险贝叶斯分类器所作出判断为{}".format(getminrisk(a, b, UUU, SSS, risk)))
        print("最小化错误率贝叶斯分类器做出判断为{}".format(getminfau(a, b, UUU, SSS)))