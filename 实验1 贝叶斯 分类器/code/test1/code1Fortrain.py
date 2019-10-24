import csv
import random
import pandas

def loadcsv(name):
    f = csv.reader(open(name,'r'))
    dataset = list(f)
    for i in range(len(dataset)):
        continue
    print ('ok')
    return dataset

def randDivision(dataset , trainSize):
    copy = list(dataset)
    train = []
    while len(train)<trainSize:
        index = random.randrange(len(copy))
        train.append(copy.pop(index))
    return [train, copy]

#主函数
if __name__=="__main__":
    name = "..\..\data\car.csv"
    dataset = loadcsv(name)
    print(len(dataset))
    trainSet , testSet = randDivision(dataset,100)

    path1 = "../../data/100/train.csv"
    path2 = "../../data/100/test.csv"
    writer1 = csv.writer(path1)
    writer2 = csv.writer(path2)
    writer1.writerow(trainSet)
    writer2.writerow(testSet)
    print(len(trainSet))