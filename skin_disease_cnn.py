import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from glob import glob
import seaborn as sns
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample

np.random.seed(42)
from sklearn.metrics import confusion_matrix

import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from scipy import stats
from tensorflow.keras.utils import to_categorical

from tensorflow.keras.models import Sequential

import pickle
import joblib


skin_df = pd.read_csv(r'C:\Users\Miran\UNKNOWN\HAM10000_metadata.csv')

SIZE = 32


le = LabelEncoder()
le.fit(skin_df['dx'])
LabelEncoder()

 
skin_df['label'] = le.transform(skin_df["dx"]) 

df_0 = skin_df[skin_df['label'] == 0]
df_1 = skin_df[skin_df['label'] == 1]
df_2 = skin_df[skin_df['label'] == 2]
df_3 = skin_df[skin_df['label'] == 3]
df_4 = skin_df[skin_df['label'] == 4]
df_5 = skin_df[skin_df['label'] == 5]
df_6 = skin_df[skin_df['label'] == 6]

n_samples=500 
df_0_balanced = resample(df_0, replace=True, n_samples=n_samples, random_state=42) 
df_1_balanced = resample(df_1, replace=True, n_samples=n_samples, random_state=42) 
df_2_balanced = resample(df_2, replace=True, n_samples=n_samples, random_state=42)
df_3_balanced = resample(df_3, replace=True, n_samples=n_samples, random_state=42)
df_4_balanced = resample(df_4, replace=True, n_samples=n_samples, random_state=42)
df_5_balanced = resample(df_5, replace=True, n_samples=n_samples, random_state=42)
df_6_balanced = resample(df_6, replace=True, n_samples=n_samples, random_state=42)


skin_df_balanced = pd.concat([df_0_balanced, df_1_balanced, 
                              df_2_balanced, df_3_balanced, 
                              df_4_balanced, df_5_balanced, df_6_balanced])

image_path = {os.path.splitext(os.path.basename(x))[0]: x
                     for x in glob(os.path.join(r'C:\Users\Miran\Downloads\HAM10000_DATASET', '*', '*.jpg'))}


skin_df_balanced['path'] = skin_df['image_id'].map(image_path.get)
#Use the path to read images.
skin_df_balanced['image'] = skin_df_balanced['path'].map(lambda x: np.asarray(Image.open(x).resize((SIZE,SIZE))))

X = np.asarray(skin_df_balanced['image'].tolist())
X = X/255.  # Scale values to 0-1. You can also used standardscaler or other scaling methods.
Y=skin_df_balanced['label']  #Assign label values to Y
Y_cat = to_categorical(Y, num_classes=7) #Convert to categorical as this is a multiclass classification problem
#Split to training and testing
x_train, x_test, y_train, y_test = train_test_split(X, Y_cat, test_size=0.25, random_state=42)


num_classes = 7

model = Sequential()
model.add(layers.Conv2D(256, (3, 3), activation="relu", input_shape=(SIZE, SIZE, 3)))
#model.add(BatchNormalization())
model.add(layers.MaxPool2D(pool_size=(2, 2)))  
model.add(layers.Dropout(0.3))

model.add(layers.Conv2D(128, (3, 3),activation='relu'))
#model.add(BatchNormalization())
model.add(layers.MaxPool2D(pool_size=(2, 2)))  
model.add(layers.Dropout(0.3))

model.add(layers.Conv2D(64, (3, 3),activation='relu'))
#model.add(BatchNormalization())
model.add(layers.MaxPool2D(pool_size=(2, 2)))  
model.add(layers.Dropout(0.3))
model.add(layers.Flatten())

model.add(layers.Dense(32))
model.add(layers.Dense(7, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['acc'])

batch_size = 10 
epochs = 10

history = model.fit(
    x_train, y_train,
    epochs=epochs,
    batch_size = batch_size,
    validation_data=(x_test, y_test),
    verbose=2)

score = model.evaluate(x_test, y_test)
print('Test accuracy:', score[1])



model.save('final_skin_model.h5')


