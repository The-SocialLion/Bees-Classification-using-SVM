# -*- coding: utf-8 -*-
"""BC-CL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16FRLF_7wTkoyCXBghL0mPvDjDOtMr6W7
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import zipfile 
from PIL import Image,ImageOps

zip = zipfile.ZipFile('bee_imgs.zip')
zip.extractall()

df=pd.read_csv("bee_data.csv")
df=df.dropna(how='any')
df['species']=df['subspecies']
df=df.drop(columns=['date','time','zip code','location','caste','subspecies'])
df

df['species'].unique()

from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
le1=LabelEncoder()
df['health']=le.fit_transform(df['health'])
df['pollen_carrying']=le.fit_transform(df['pollen_carrying'])
df['species']=le1.fit_transform(df['species'])

df

import os
cur_path = os.getcwd()
print(cur_path)

path = os.path.join(cur_path,'bee_imgs/')
images = os.listdir(path)

print(images)

f=['.DS_Store']
for i in images:
  if i in f:
    images.remove(i)

len(images)

print(list(set(images)))

len(images)

data = []
labels = []

print(len(df))

for i in range(len(df)):
  #print(df['file'][i])
  if df['file'][i] in images:
    imag = Image.open(path+ '//'+ df['file'][i])
    imag=ImageOps.grayscale(imag)
    imag = imag.resize((64,64))
    imag = np.array(imag)
    imag=imag.flatten()
    data.append(imag)
    labels.append(df['species'][i])
  else:
    print("error no images")

print(labels)

len(labels)

print(data)

len(data)

#Converting lists into numpy arrays
data = np.array(data)
labels = np.array(labels)

print(data.shape, labels.shape)

import tensorflow as tf
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.25, random_state=42)

from sklearn.svm import SVC
svc=SVC(kernel='rbf',random_state=0)
svc.fit(X_train,y_train)

y_pred = svc.predict(X_test)
y_pred=np.round(y_pred)
np.set_printoptions(precision=2)

print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

from sklearn.metrics import accuracy_score
print("Accuracy Score for the algorithm=>{}%".format(round(accuracy_score(y_test,y_pred)*100),2))