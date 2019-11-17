import csv
import random
from math import log
import numpy as np

dict_iris = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
dict_siri = {0: 'Iris-setosa', 1: 'Iris-versicolor', 2: 'Iris-virginica'}


class treenode:
    def __init__(self, FenLei, FenLeiZhi, YeziPanDuan, node_id):
        self.FenLei = FenLei
        self.FenLeiZhi = FenLeiZhi
        self.YeziPanDuan = YeziPanDuan
        self.fenleiindex = [0, 1, 2]
        self.node_id = node_id
        if int(YeziPanDuan) == -1:
            print("产生中间节点{}，为第{}特征，分类值为{}".format(node_id, FenLei, FenLeiZhi))
        else:
            print("产生叶子节点{}，判断结果为{}".format(node_id, dict_siri[YeziPanDuan]))
    def popfenlei(self, fenlei):
        ii = 0
        for i in self.fenleiindex:
            if int(i) == int(fenlei):
                self.fenleiindex.pop(ii)
                return
            ii = ii+1

# 建立用来储存我们的树节点的
nodes = []


# 构建一个树
def buildTree(dataset, node_id):
    if get_ent(dataset) > 0.3:
        fenlei, fenleizhi = get_fenleidian(dataset)
        trnode = treenode(fenlei, fenleizhi, -1, node_id)
        trnode.popfenlei(fenlei)
        nodes.append(trnode)
        datasmall, databig = divide(dataset, fenlei, fenleizhi)
        #print(get_ent(datasmall))
        #print(get_ent(databig))
        buildTree(datasmall, 2 * node_id)
        #print("hhhhhhhhhhhh{}".format(dataset[0][4]))
        buildTree(databig, 2 * node_id + 1)
    else:
        #print("hhhhhhhhhhhh{}".format(dataset[0][4]))
        if len(dataset) == 0:
            #print("ffff")
            return
        panduan = dataset[0][4]
        trnode = treenode(0, 0, panduan, node_id)
        nodes.append(trnode)


# 加载函数
def loadcsv(name):
    f = csv.reader(open(name, 'r'))
    dataset = list(f)
    return dataset


# 把数据数字化
def digital(dataset):
    for i in range(len(dataset)):
        dataset[i][4] = dict_iris[dataset[i][4]]

# 把第num个数据进行排列,并取出可能的分割点
def get_mid(dataset,num):
    l1 = []
    l2 = []
    for i in range(len(dataset)):
        l1.append(dataset[i][num])
    l1 = list(set(l1))
    l1.sort()
    for i in range(len(l1)-1):
        l2.append(((float)(l1[i])+(float)(l1[i+1]))/2)
    return l2


# 分割函数
def randDivision(dataset , trainSize):
    copy = list(dataset)
    train = []
    while len(train)<trainSize:
        index = random.randrange(len(copy))
        train.append(copy.pop(index))
    return [train, copy]


'''
计算信息熵和信息增益
'''


# 划分数据集方便计算条件信息熵
def divide(dataset, index, dnum):
    dataset2 = list(dataset)
    dataset1 = []
    ii  = 0
    for i in dataset:
        if (float)(i[index])<(float)(dnum):
            dataset1.append(i)
            dataset2.pop(ii)
            ii = ii-1
        ii = ii+1
    return [dataset1, dataset2]


# 计算信息熵
def getP(dataset,num):
    p = 0.0
    a = len(dataset)
    if a == 0:
        return 0
    b = 0
    for i in dataset:
        if i[4] == num:
            b = b+1
    p = b/a
    #print(p)
    return p


def get_ent(dataset):
    p = []
    ent = 0.0
    for i in range(3):
        pp = getP(dataset, i)
        p.append(pp)
    for i in p:
        if i != 0:
            ent = ent - i*log(i, 2)
    return ent


# 计算信息增益
def get_gain(dataset, index, dnum):
    entD = get_ent(dataset)
    data1, data2 = divide(dataset, index, dnum)
    a1 = 0.0
    a2 = 0.0
    gain = 0.0
    '''print("data的熵{}".format(entD))
    print("data1的熵{}".format(get_ent(data1)))
    print("data2的熵{}".format(get_ent(data2)))'''
    a2 = len(data2)/len(dataset)
    a1 = len(data1)/len(dataset)
    gain = entD - a1*get_ent(data1) - a2*get_ent(data2)
    return gain


# 得到单个特征最高的信息增益所在的分类点
def get_maxgain(dataset, index):
    max = -10000
    iii = 0
    dnums = get_mid(dataset, index)
    for i in dnums:
        gg = get_gain(dataset, index, i)
        if gg>=max:
            max = gg
            iii = i
    return iii


# 多个特征中选择一个分类点
'''
输入：数据集，各个特征的最佳分类点
输出：排序list
'''
def get_maxtezheng(dataset,node):
    max = 0
    max_i = 0
    max_list = []
    for i in range(len(node)):
        a = get_gain(dataset, i, node[i])
        max_list.append(a)
        if max<a:
            max_i = i
            max = a
    return [max_list, max_i]


def get_fenleidian(dataset):
    divide_node = []
    for tezheng in range(4):
        divide_node.append(get_maxgain(dataset, tezheng))
        #print("*********************")
        #print("所以应该第{}个特征选择{}作为分割点".format(tezheng, get_maxgain(dataset, tezheng)))
        #print("*********************")
    max_list, max_i = get_maxtezheng(trainSet, divide_node)
    #print(max_i)
    #print(max_list)
    return [max_i, divide_node[max_i]]


# 按照树节点的编号找到节点在数组中的位置
def find_(node_id):
    for node in range(len(nodes)):
        if nodes[node].node_id == node_id:
            return node+1
    return -1


# 验证函数
def classify(dataset):
    corr = 0    # 记录正确的数目

    allof = len(dataset)    # 总数
    for item in dataset:
        aa = 1
        #print(aa)
        nnn = nodes[aa-1]
        while int(nnn.YeziPanDuan) == int(-1):  # 在主节点之间遨游
            if float(item[int(nnn.FenLei)]) <= float(nnn.FenLeiZhi):
                aa = 2*aa
                #print("左")
                nnn = nodes[find_(aa)-1]   # 左子树
            else:
                #print("👉")
                aa = 2*aa+1
                nnn = nodes[find_(aa)-1]     # 右子树
        #print("树结果为{}， 实际为{}".format(nnn.YeziPanDuan, item[4]))
        if nnn.YeziPanDuan == item[4]:  # 判断是否正确
            #print("树结果为{}， 实际为{}".format(nnn.YeziPanDuan, item[4]))
            corr = corr+1
        aa = 1
    bibi = 0.0
    bibi = corr/allof
    return bibi


# 五折交叉验证划分训练集
def getTrainTest(kkk, datas):
    kkkk = 0
    traindata = []
    for i in datas:
        #print("12112121")
        if kkkk == kkk:
            #print("kkk:{}, kkkk:{}".format(kkk, kkkk))
            kkkk = kkkk + 1
            continue
        kkkk = kkkk+1
        traindata = traindata + i
        #print(len(traindata))
    return traindata


# 五折交叉验证
def FiveFordCV(dataset, size, nums):
    s = int(size/nums)
    print(s)
    dataForTfcv = []
    kkk = 0
    Rate = []
    testSet = dataset
    for i in range(nums-1):
        trainSet, testSet = randDivision(testSet, s)
        dataForTfcv.append(trainSet)
    dataForTfcv.append(testSet)
    # print(len(dataForTfcv))
    for i in dataForTfcv:
        # print(kkk)
        testSetForTen = getTrainTest(kkk, dataForTfcv)
        kkk = kkk+1
        buildTree(testSetForTen, 1)
        # print(len(testSetForTen))
        aaa = classify(i)
        Rate.append(aaa)
        #print("第{}次正确率为{}".format(kkk,rate[1] / (rate[0] + rate[1])))
    return np.mean(Rate)


# main function
if __name__=="__main__":
    name = "..\data\iris.csv"
    dataset = loadcsv(name)
    digital(dataset)
    trainSet, testSet = randDivision(dataset, 100)
    #print(get_fenleidian(trainSet))
    #set1, set2 = divide(trainSet, 3, 0.8)
    #tr = treenode(0,0,0,0)
    #buildTree(trainSet, 1)
    #a = classify(testSet)
    #print("验证得知，正确率为{}%".format(a*100))
    aaaaa = FiveFordCV(dataset, 150, 5)
    print("经预剪枝五折交叉验证后得知，正确率为{}%".format(aaaaa*100))