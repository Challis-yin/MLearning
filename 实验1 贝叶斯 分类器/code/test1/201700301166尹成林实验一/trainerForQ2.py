# 编写日期 2019/10/21
# 编写人 尹成林
# 学号 201700301166
# 实验 贝叶斯实验第2问

import csv
import random
import numpy as np
# import pandas
# 数据导入及分成两份
def loadcsv(name):
    f = csv.reader(open(name,'r'))
    dataset = list(f)
    return dataset

def randDivision(dataset , trainSize):
    copy = list(dataset)
    train = []
    while len(train)<trainSize:
        index = random.randrange(len(copy))
        train.append(copy.pop(index))
    return [train, copy]


#初始化一些数据

data1 = [[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
dataunacc = [[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
dataacc = [[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
datagood = [[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
dataVgood = [[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
datavip = [0,0,0,0]

# 统计函数，将具体个数的多少进行统计
'''
*****************************************
训练器部分
*****************************************
'''

def stat(dataset):
    for i in dataset:
        count = i[0]
        maint = i[1]
        door = i[2]
        persons = i[3]
        lug = i[4]
        safty = i[5]
        vip = i[6]
        addcount(count, data1)
        addmaint(maint, data1)
        adddoor(door, data1)
        addperson(persons, data1)
        addlug(lug, data1)
        addsafty(safty, data1)
        if vip == 'unacc':
            datavip[0] = datavip[0]+1
            addcount(count, dataunacc)
            addmaint(maint, dataunacc)
            adddoor(door, dataunacc)
            addperson(persons, dataunacc)
            addlug(lug, dataunacc)
            addsafty(safty, dataunacc)
        elif vip == 'acc':
            datavip[1] = datavip[1] + 1
            addcount(count, dataacc)
            addmaint(maint, dataacc)
            adddoor(door, dataacc)
            addperson(persons, dataacc)
            addlug(lug, dataacc)
            addsafty(safty, dataacc)
        elif vip == 'good':
            datavip[2] = datavip[2] + 1
            addcount(count, datagood)
            addmaint(maint, datagood)
            adddoor(door, datagood)
            addperson(persons, datagood)
            addlug(lug, datagood)
            addsafty(safty, datagood)
        elif vip == 'vgood':
            datavip[3] = datavip[3] + 1
            addcount(count, dataVgood)
            addmaint(maint, dataVgood)
            adddoor(door, dataVgood)
            addperson(persons, dataVgood)
            addlug(lug, dataVgood)
            addsafty(safty, dataVgood)


##上面函数的仔函数

def addcount(count,data):
    if count == 'vhigh':
        data[0][0] = data[0][0]+1
    elif count == 'high':
        data[0][1] = data[0][1]+1
    elif count == 'med':
        data[0][2] = data[0][2] + 1
    elif count == 'low':
        data[0][3] = data[0][3] + 1
def addmaint(maint,data):
    if maint == 'vhigh':
        data[1][0] = data[1][0]+1
    elif maint == 'high':
        data[1][1] = data[1][1] + 1
    elif maint == 'med':
        data[1][2] = data[1][2] + 1
    elif maint == 'low':
        data[1][3] = data[1][3] + 1
def adddoor(door,data):
    if door == '2':
        data[2][0] = data[2][0] + 1
    elif door == '3':
        data[2][1] = data[2][1] + 1
    elif door == '4':
        data[2][2] = data[2][2] + 1
    elif door == '5more':
        data[2][3] = data[2][3] + 1
def addperson(persons,data):
    if persons == '2':
        data[3][0] = data[3][0] + 1
    elif persons == '4':
        data[3][1] = data[3][1] + 1
    elif persons == 'more':
        data[3][2] = data[3][2] + 1
def addlug(lug,data):
    if lug == 'small':
        data[4][0] = data[4][0] + 1
    elif lug == 'med':
        data[4][1] = data[4][1] + 1
    elif lug == 'big':
        data[4][2] = data[4][2] + 1
def addsafty(safty,data):
    if safty == 'low':
        data[5][0] = data[5][0] + 1
    elif safty == 'med':
        data[5][1] = data[5][1] + 1
    elif safty == 'high':
        data[5][2] = data[5][2] + 1

# 将具体的个数转化为概率
def getP(num, data):
    for k in range(len(data)):
        for ii in range(len(data[k])):
            data[k][ii] = data[k][ii]/num


'''
*****************************************
测试部分
*****************************************
'''

# 以下的函数为概率返回函数，再检验时起到查表的作用
def getR0(data, t):
        if t == 'vhigh':
            return data[0][0]
        elif t == 'high':
            return data[0][1]
        elif t == 'med':
            return data[0][2]
        elif t == 'low':
            return data[0][3]


def getR1(data, maint):
    if maint == 'vhigh':
        return data[1][0]
    elif maint == 'high':
        return data[1][1]
    elif maint == 'med':
        return data[1][2]
    elif maint == 'low':
        return data[1][3]
    return 0


def getR2(data, door):
    if door == '2':
        return data[2][0]
    elif door == '3':
        return data[2][1]
    elif door == '4':
        return data[2][2]
    elif door == '5more':
        return data[2][3]


def getR3(data, persons):
    if persons == '2':
        return data[3][0]
    elif persons == '4':
        return data[3][1]
    elif persons == 'more':
        return data[3][2]


def getR4(data, lug):
    if lug == 'small':
        return data[4][0]
    elif lug == 'med':
        return data[4][1]
    elif lug == 'big':
        return data[4][2]


def getR5(data, safty):
    if safty == 'low':
        return data[5][0]
    elif safty == 'med':
        return data[5][1]
    elif safty == 'high':
        return data[5][2]


def getR6(num):
    if num == 0:
        return "unacc"
    if num == 1:
        return "acc"
    if num == 2:
        return "good"
    if num == 3:
        return "vgood"

rate = [0,0]

# 检验函数
def test(testset):
    for line in testset:
        rate0 = datavip[0]*getR0(dataunacc,line[0])*getR1(dataunacc,line[1])*getR2(dataunacc,line[2])*getR3(dataunacc,line[3])*getR4(dataunacc,line[4])*getR5(dataunacc,line[5])
        rate1 = datavip[1]*getR0(dataacc,line[0])*getR1(dataacc,line[1])*getR2(dataacc,line[2])*getR3(dataacc,line[3])*getR4(dataacc,line[4])*getR5(dataacc,line[5])
        rate2 = datavip[2]*getR0(datagood,line[0])*getR1(datagood,line[1])*getR2(datagood,line[2])*getR3(datagood,line[3])*getR4(datagood,line[4])*getR5(datagood,line[5])
        rate3 = datavip[3]*getR0(dataVgood,line[0])*getR1(dataVgood,line[1])*getR2(dataVgood,line[2])*getR3(dataVgood,line[3])*getR4(dataVgood,line[4])*getR5(dataVgood,line[5])
        k = getbig(rate0,rate1,rate2,rate3)
        if line[6] != getR6(k):
            rate[0] = rate[0]+1
        else:
            rate[1] = rate[1]+1

'''
*****************************************
总控函数和一些轮子函数
*****************************************
'''

##返回四个数中的最大值的下表
def getbig(r1,r2,r3,r4):
    k = max(r1, r2, r3, r4)
    if k == r1:
        return 0
    if k == r2:
        return 1
    if k == r3:
        return 2
    if k == r4:
        return 3

# 初始化函数，初始化数组中的值
def renum():
    data1 = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0]]
    dataunacc = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0]]
    dataacc = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
               [0.0, 0.0, 0.0]]
    datagood = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0]]
    dataVgood = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
                 [0.0, 0.0, 0.0]]
    datavip = [0, 0, 0, 0]

##总函数，调用上面的所有函数
def training(size):
    renum()
    trainSet, testSet = randDivision(dataset, size)
    stat(trainSet)
    getP(datavip[0], dataunacc)
    getP(datavip[1], dataacc)
    getP(datavip[2], datagood)
    getP(datavip[3], dataVgood)
    test(testSet)
    Rate = rate[1] / (rate[0] + rate[1])
    print("当训练数据大小为{0}个时，剩余数据的检测正确率为{1}".format(size, Rate))

# 返回合并后的训练集
def getTrainTest(kkk, datas):
    kkkk = 0
    traindata = []
    for i in datas:
        if kkkk == kkk:
            continue
        kkkk = kkkk+1
        traindata = traindata + i
    return traindata

# 求平均值函数

# 十折交叉验证函数
def TenFordCV(size,nums):
    renum()
    s = int(size/nums)
    dataForTfcv = []
    kkk = 0
    Rate = []
    testSet = dataset
    for i in range(nums-1):
        trainSet, testSet = randDivision(testSet, s)
        dataForTfcv.append(trainSet)
    dataForTfcv.append(testSet)
    for i in dataForTfcv:
        renum()
        testSetForTen = getTrainTest(kkk, dataForTfcv)
        kkk = kkk+1
        stat(testSetForTen)
        getP(datavip[0], dataunacc)
        getP(datavip[1], dataacc)
        getP(datavip[2], datagood)
        getP(datavip[3], dataVgood)
        test(i)
        Rate.append(rate[1] / (rate[0] + rate[1]))
        #print("第{}次正确率为{}".format(kkk,rate[1] / (rate[0] + rate[1])))
    return np.mean(Rate)



if __name__=="__main__":
    name = "..\..\data\car.csv"
    dataset = loadcsv(name)
    training(100)
    training(200)
    training(500)
    training(700)
    training(1350)
    ppp = input("想要进行多少层十折交叉验证")
    r = []
    for i in range(int(ppp)):
        r.append(TenFordCV(1728, 10))
    print("经{}层十折交叉验证，该朴素贝叶斯分类器平均分类正确率为{}".format(ppp, np.mean(r)))