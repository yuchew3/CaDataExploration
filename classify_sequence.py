import numpy as np
import matplotlib.pyplot as plt
import ca_data_utils
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedShuffleSplit
from sklearn.svm import SVC
from sklearn.gaussian_process.kernels import RBF
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.preprocessing import StandardScaler

def select_k(X, y, k):
    print('k = ', k)
    X = [X[x:x+k].flatten() for x in range(X.shape[0]-k+1)]
    y = y[k-1:]

    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    C_range = np.logspace(-1, 2, 4)
    print('C range: ', C_range)
    gamma_range = np.logspace(-1, 2, 4) * 1. / X.shape[1]
    print('gamma range: ', gamma_range)
    param_grid = dict(gamma=gamma_range, C=C_range)

    # cv = StratifiedShuffleSplit(n_splits=4, test_size=0.25)
    grid = GridSearchCV(SVC(), param_grid=param_grid, n_jobs=20)

    print('start to train...')
    grid.fit(X, y)
    print('finished')
    df = pd.DataFrame.from_dict(grid.cv_results_)
    filename = 'result_' + str(k)
    df.to_csv(filename)
    print('done with k = ', k)
    print("The best parameters are %s with a score of %0.2f"
        % (grid.best_params_, grid.best_score_))



def select_models(X, y, k):
    # assume X.shape[0] > k
    print('k = ', k)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=False) # random state?
    X_train = [X_train[x:x+k].flatten() for x in range(X_train.shape[0]-k+1)]
    X_test = [X_test[x:x+k].flatten() for x in range(X_test.shape[0]-k+1)]
    y_train = y_train[k-1:]
    y_test = y_test[k-1:]
    classifiers = [
        SVC(gamma=2, C=0.001),
        RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        AdaBoostClassifier()
    ]
    names = ['RBF SVM', 'Random Forest', 'AdaBoost']
    train = []
    test = []
    for name, clf in zip(names, classifiers):
        print('starting to train with ', name)
        clf.fit(X_train, y_train)
        print('---> calculating training set accuracy:')
        train_accu = clf.score(X_train, y_train)
        train.append(train_accu)
        print('---> training set accuracy: ', train_accu)
        print('---> calculating testing set accuracy:')
        test_accu = clf.score(X_test, y_test)
        test.append(test_accu)
        print('---> testing set accuracy: ', test_accu)
    np.save('../data/clf_results/clf_names', names)
    np.save('../data/clf_results/train_accuracy'+'_'+str(k), np.array(train))
    np.save('../data/clf_results/test_accuracy'+'_'+str(k), np.array(test))

def tune_rbf_svm():
    vid = ca_data_utils.load_v_matrix()[:,9:39992]
    ddlabels = ca_data_utils.load_labels()[9:39992]

    scaler = StandardScaler()
    X = scaler.fit_transform(vid.T)

    C_range = np.logspace(-2, 10, 13)
    print('C range: ', C_range)
    gamma_range = np.logspace(-9, 3, 13) * 1. / x.shape[1] #(-3,3,7)
    print('gamma range: ', gamma_range)
    param_grid = dict(gamma=gamma_range, C=C_range)

    cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
    grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
    print('start to train...')
    grid.fit(X, labels)

    print("The best parameters are %s with a score of %0.2f"
        % (grid.best_params_, grid.best_score_))
    
    print('The results are:')
    print(grid.cv_results_)



if __name__ == '__main__':
    vid = ca_data_utils.load_v_matrix().T[9:39992]
    labels = ca_data_utils.load_labels()[9:39992]

    for k in range(5, 11):
        select_models(vid, labels, k)
        # select_k(vid, labels, k)


    # clf = SVC(gamma=0.001, C=10)

    # scaler = StandardScaler()
    # X = scaler.fit_transform(vid)
    # X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.25)
    # print('start to train')
    # clf.fit(X_train, y_train)
    # print('finally finished tada~~')
    # y_pred = clf.predict(X)
    # print('saving y_pred for whole video, the accuracy for test data is ', clf.score(X_test, y_test))
