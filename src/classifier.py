#!/usr/bin/env python

import warnings
from xgboost import XGBClassifier 
from sklearn.metrics import accuracy_score, classification_report, f1_score 
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import ExtraTreesClassifier
from itertools import combinations
import csv
import sys
import numpy as np
import os
from config import featuresFilePath, numIterations
import argparse
from statistics import mean

compressor = {
    0:"bzip2",
    1:"JARVIS",
    2:"MFCompress",
    3:"NUHT",
    4:"zstd"
}

def warn(*args, **kwargs):
    pass
warnings.warn = warn

def ReadData(filename, columns):
    domains = {
        "viral":0, 
        "bacteria":1,
        "archaea":2, 
        "fungi":3,
        "protozoa":4,
    }
    
    X_test, y_test = [], []
    with open(filename, 'r') as file:
        samples = csv.reader(file)
        next(samples)
        for row in samples:
            #X_test.append([float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5])])
            tmp = []
            for column in columns:
                tmp.append(float(row[column+1]))
            X_test.append(tmp)
            y_test.append(domains[row[0]])
    return np.array(X_test).astype('float32'), np.array(y_test).astype('int32')


def Classify(args, columns):
    domains = ["Viral", "Bacteria", "Archaea", "Fungi", "Protozoa"]
    accuracy_XGB = []
    f1score_XGB = []
    data, labels = ReadData(args.filename, columns)

    if args.features_selection:
        clf = ExtraTreesClassifier(n_estimators=50)
        clf = clf.fit(data, labels)
        model = SelectFromModel(clf, prefit=True)
        print(data.shape)
        data = model.transform(data)
        print(data.shape)

    for a in range(numIterations):
        X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.20, stratify=labels, random_state=a)
        model = XGBClassifier(max_depth=12, learning_rate=0.89, n_estimators=500, eval_metric='mlogloss')
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        predictions = [round(value) for value in y_pred]
        accuracy_XGB.append(accuracy_score(y_test, predictions))
        f1score_XGB.append(f1_score(y_test, y_pred, average='weighted'))
        if args.classification_report:
            print("Classification report, using:", end=" ")
            print(" ".join([compressor[x] for x in columns]))
            print(classification_report(y_test, y_pred, target_names=domains, digits=4))
            break

    if args.accuracy:
        print("Accuracy of XGB, using:", end=" ")
        print(" ".join([compressor[x] for x in columns]))
        print(sum(accuracy_XGB)/len(accuracy_XGB))

    elif args.f1_score:
        print("F1 score of XGB, using:", end=" ")
        print(" ".join([compressor[x] for x in columns]))
        print(sum(f1score_XGB)/len(f1score_XGB))
    
    elif args.both:
        print("Accuracy of XGB, using:", end=" ")
        print(" ".join([compressor[x] for x in columns]))
        print(sum(accuracy_XGB)/len(accuracy_XGB))
        print("F1 score of XGB, using:", end=" ")
        print(" ".join([compressor[x] for x in columns]))
        print(sum(f1score_XGB)/len(f1score_XGB))
    print()
        


def help(show=False):
    parser = argparse.ArgumentParser(description="")
    helper = parser.add_argument_group('System settings', 'System parameters to run the classifier in the different modes')
    helper.add_argument('-f', '--filename', dest='filename', \
                        type=str, default=featuresFilePath, \
                        help=f'The system settings file (default: {featuresFilePath})')   
    helper.add_argument('-f1', '--f1-score', default=False, action='store_true', \
                            help='This flag produces the classificarion report using the F1-score (default: False)')
    helper.add_argument('-a', '--accuracy', default=False, action='store_true', \
                            help='This flag produces the classificarion report using the Accuracy metric (default: False)')
    helper.add_argument('-b', '--both', default=False, action='store_true', \
                            help='This flag produces the classificarion report using the both metrics (default: False)') 
    helper.add_argument('-fs', '--features-selection', default=False, action='store_true', \
                            help='This flag performs feature selection (default: False)') 
    helper.add_argument('-ac', '--all-columns', default=False, action='store_true', \
                            help='This flag classifies using all features (default: False)') 
    helper.add_argument('-cr', '--classification-report', default=False, action='store_true', \
                            help='This flag generates the classification report (default: False)') 
    helper.add_argument('-bf', '--brute-force', default=False, action='store_true', \
                            help='This flag performs brute force classification of all possible combination of features (default: False)') 
    if show:
        parser.print_help()
    return parser.parse_args()
    

if __name__ == "__main__":
    args = help()
    if args.accuracy or args.f1_score or args.both or args.classification_report:
        if args.all_columns:
            Classify(args, [0,1,2,3,4])
        
        elif args.brute_force:
            all_comb_list=[]
            for x in range(1,5,1):
                com_list = list(combinations(range(5), x+1))
                [Classify(args,list(ele)) for ele in com_list]
        else:
            for column in range(5):
                Classify(args, [column])
    else:
        help(True)