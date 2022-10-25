import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
import math
import seaborn as sns
from sklearn import ensemble
from sklearn import gaussian_process
from sklearn import svm
from sklearn import tree
from sklearn import naive_bayes
from sklearn import neighbors
import sklearn.metrics as metrics
import pickle


df = pd.read_csv('diabetes.csv')
X = df.drop(['Outcome'], axis=1)

y = df[['Outcome']]

reg = linear_model.LinearRegression()

reg.fit(X, y)

pickle.dump(reg, open('diabetes_new.pkl', 'wb'))

pickled_model = pickle.load(open('diabetes_new.pkl', 'rb'))

