import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

df =  pd.read_csv('heart.csv')



X = df.drop(['target'], axis=1)
y = df[['target']]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

from sklearn import linear_model
m = linear_model.LogisticRegressionCV()
m.fit(X_train, y_train)
print(m.score(X_test, y_test))


pickle.dump(m, open('heart_new.pkl', 'wb'))

pickled_model = pickle.load(open('heart_new.pkl', 'rb'))



#print(prediction)

#if (prediction[0]== 0):
  #print('The Person does not have a Heart Disease')
#else:
  #print('The Person has Heart Disease')