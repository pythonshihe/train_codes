# encoding:utf-8
# Author:shi
# @Time:2020/6/2 11:01

import settings
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
# from sklearn.externals import joblib
import joblib
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn import svm


def trainModel(data, label):
    print("trainning process >>>>>>>>>>>>>>>>>>>>>>")
    rbf = svm.SVC(decision_function_shape='ovo', kernel='rbf')
    scores = cross_val_score(rbf, data, label, cv=10)
    print("rbf: ", scores.mean())

    linear = svm.SVC(decision_function_shape='ovo', kernel='linear')
    scores = cross_val_score(linear, data, label, cv=10)
    print("linear: ", scores.mean())
    linear.fit(data, label)

    rf = RandomForestClassifier(n_estimators=100, max_depth=None, min_samples_split=2, random_state=0)
    scores = cross_val_score(rf, data, label, cv=10)
    print("rf: ", scores.mean())
    rf.fit(data, label)

    predict = rf.predict(data)
    acc = 0
    for num in range(len(label)):
        if predict[num] == label[num]:
            acc += 1
            # print("predict:", predict[num], "\tlabel: ", label[num])
    print("model acc: ", acc / len(label))

    # 持久化
    joblib.dump(rf, settings.MODAL_PATH)
    print("model save success!")

    return rbf


# 测试模型
def testModel(data, label):
    # 读取模型
    model = joblib.load(settings.MODAL_PATH)
    # 预测
    predict_list = model.predict(data)
    # print classification_report(label, predict_list)#按类别分类的各种指标
    print(r"\ntest process >>>>>>>>>>>>>>>>>>>>>>>>")
    print("test precision: ", metrics.precision_score(label, predict_list))  # precision
    print("test recall: ", metrics.recall_score(label, predict_list))  # recall
    print("test f1 score: ", metrics.f1_score(label, predict_list))  # f1 score
    print("confusion matrix:")
    print(confusion_matrix(label, predict_list))  # 混淆矩阵


if __name__ == '__main__':
    pass
