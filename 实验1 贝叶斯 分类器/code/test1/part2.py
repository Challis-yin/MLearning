import sys
import numpy as np
from sklearn.model_selection import KFold

data_file = '../dataset/car evaluation dataset.txt'


# 加载数据，将原来的字符数据向量化
def load_data(data_file):
    Xt = np.genfromtxt(data_file, delimiter=',', dtype=[
        'U15', 'U15', 'U15', 'U15', 'U15', 'U15', 'U15'], names=(
        'buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety',
        'class'))

    dict_buying = {'low': 0, 'med': 1, 'high': 2, 'vhigh': 3}
    dict_maint = {'low': 0, 'med': 1, 'high': 2, 'vhigh': 3}
    dict_doors = {'2': 0, '3': 1, '4': 2, '5more': 3}
    dict_persons = {'2': 0, '4': 1, 'more': 2}
    dict_lug_boot = {'small': 0, 'med': 1, 'big': 2}
    dict_safety = {'low': 0, 'med': 1, 'high': 2}
    dict_class = {'unacc': 0, 'acc': 1, 'good': 2, 'vgood': 3}

    data = np.zeros((Xt.shape[0], 7), dtype=np.int)

    rr = 0
    for row in Xt:
        data[rr, :] = np.array([dict_buying[row[0]], dict_maint[row[1]],
                                dict_doors[row[2]], dict_persons[row[3]], dict_lug_boot[row[4]],
                                dict_safety[row[5]], dict_class[row[6]]])
        rr = rr + 1

    return data


def cal_prob(data_matrix):
    prob_buying = np.zeros((4, 4))
    prob_maint = np.zeros((4, 4))
    prob_doors = np.zeros((4, 4))
    prob_persons = np.zeros((3, 4))
    prob_lug_boot = np.zeros((3, 4))
    prob_safety = np.zeros((3, 4))
    classes_nums = np.zeros(4)

    feature_nums = list()
    feature_nums.append(prob_buying)
    feature_nums.append(prob_maint)
    feature_nums.append(prob_doors)
    feature_nums.append(prob_persons)
    feature_nums.append(prob_lug_boot)
    feature_nums.append(prob_safety)

    probs = list()

    # 统计数据
    for i in range(data_matrix.shape[0]):
        # 统计 class 的数量
        class_index = data_matrix[i][6]
        classes_nums[class_index] = classes_nums[class_index] + 1
        for feature_index in range(6):
            # 统计每个 feature 的数据
            current_feature_num = feature_nums[feature_index]
            # 在某个 class 出现的条件下某个 feature 出现的次数
            current_feature_num[data_matrix[i][feature_index]][class_index] = \
                current_feature_num[data_matrix[i][feature_index]][class_index] + 1

    # 对每个 feature 的概率进行计算
    for current_feature_num in feature_nums:
        tmp_sum = np.sum(current_feature_num, axis=0)
        current_feature_num = current_feature_num
        tmp_sum = tmp_sum
        current_feature_prob = current_feature_num / tmp_sum
        probs.append(current_feature_prob)

    classes_probs = classes_nums / (np.sum(classes_nums))

    return probs, classes_probs


# 计算最大的概率
def classify(vec2classify, probs, prob_classes):
    predict_probs = np.ones(4)
    for feature_i in range(5):
        specific_feature = vec2classify[feature_i]
        current_feature_prob = probs[feature_i]
        predict_probs = predict_probs * current_feature_prob[specific_feature]

    predict_probs = predict_probs * prob_classes

    max_prob = 0
    max_prob_class = -1
    for class_i in range(len(predict_probs)):
        predict_prob = predict_probs[class_i]
        if predict_prob >= max_prob:
            max_prob = predict_prob
            max_prob_class = class_i

    return max_prob_class


def predict(test_data, probs, prob_classes):
    wrong_num = 0
    correct_num = 0
    predict_results = list()
    for vec2classify in test_data:
        expected_result = vec2classify[6]
        vec2classify = vec2classify[:5]
        result = classify(vec2classify, probs, prob_classes)
        predict_results.append(result)
        if (result != expected_result):
            wrong_num = wrong_num + 1
        else:
            correct_num = correct_num + 1

    return predict_results, correct_num, wrong_num


# 打乱数据
def shuffle(data):
    indicies = np.arange(data.shape[0])
    np.random.shuffle(indicies)
    data = data[indicies]
    return data


# 训练 + 预测
def fit(data):
    correct_num_list = list()
    wrong_num_list = list()
    kf = KFold(n_splits=10)
    for train_data, test_data in kf.split(data):
        train_data = data[train_data]
        test_data = data[test_data]
        probs, prob_classes = cal_prob(train_data)
        predict_results, correct_num, wrong_num = predict(test_data, probs, prob_classes)
        correct_num_list.append(correct_num)
        wrong_num_list.append(wrong_num)

    correct_all = np.sum(np.array(correct_num_list))
    results_all = np.sum(np.array(wrong_num_list)) + correct_all

    print("平均正确率为", correct_all / results_all)


if __name__ == '__main__':
    data = load_data(data_file)
    data = shuffle(data)
    fit(data)
