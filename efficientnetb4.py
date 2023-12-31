# -*- coding: utf-8 -*-
"""EfficientNetB4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b_0NUftn9PrQ6OqN9ZoTFxbgQjHgj5eu

Import **Dataset** file and unzip it...
"""

from google.colab import drive
drive.mount('/content/drive', force_remount=True)

# !unzip '/content/dataset.zip'
from zipfile import ZipFile
file_name = "/content/drive/MyDrive/Data Analysis/dataset2.zip"
with ZipFile(file_name, 'r') as zip:
  zip.extractall()
  print('Done')

"""**Data Pre Processing**"""

import numpy as np
import matplotlib.pyplot as plt
import os
import tensorflow as tf
import pandas as pd

dataset_path = os.listdir('dataset')
print(dataset_path) # what kind classes in this dataset

print('Folder: ', len(dataset_path))

class_lebels = []

for items in dataset_path:
  # get all the file names
  all_classes = os.listdir('dataset' + '/' + items)
  # print(all_classes[:10])

  for room in all_classes:
    class_lebels.append((items, str('dataset_path'+'/'+items)+'/'+room))
    # print(class_lebels[:5])

# Build a DataFrame

df = pd.DataFrame(data=class_lebels, columns=['labels', 'image'])
print(df.head())
print(df.tail())

print('Total Images: ', len(df))
lebel_count = df['labels'].value_counts()
print(lebel_count)

# resize image to EfficiencyNetB4 = 380
import cv2
path = 'dataset/'
dataset_path = os.listdir('dataset')

im_size = 380

images = []
labels = []

for i in dataset_path:
  data_path = path + str(i)
  filenames = [i for i in os.listdir(data_path)]

  for f in filenames:
    img = cv2.imread(data_path + '/' + f)
    img = cv2.resize(img, (im_size, im_size))
    images.append(img)
    labels.append(i)

"""Put the image into Array using Numpy."""

# This model takes image into shape (380, 380, 3) and the input data should range (0:255)

images = np.array(images)

images = images.astype('float32') / 255.0
print('Image No, image size, color')
images.shape

"""Convert value to Binary"""

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
y = df['labels'].values
print(y)

y_labelencoder = LabelEncoder()
y = y_labelencoder.fit_transform(y)
print(y)

y = y.reshape(-1,1)

from sklearn.compose import ColumnTransformer
ct = ColumnTransformer([('my_ohe', OneHotEncoder(), [0])], remainder = 'passthrough')
Y = ct.fit_transform(y)
print(Y[:5])
print(Y[35:])

"""**Train and Test the Data**"""

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

images, Y = shuffle(images, Y, random_state=1)
train_x, test_x, train_y, test_y = train_test_split(images, Y, test_size = 0.05, random_state=415)

# inspect the train and test shape
print(train_x.shape)
print(train_y.shape)
print(test_x.shape)
print(test_y.shape)

from tensorflow import keras
from keras import layers
from keras.applications import EfficientNetB4

num_classes = 2
img_size = 380
size = (img_size, img_size)

inputs = layers.Input(shape=(img_size, img_size, 3))

# using model without transfer learning
outputs = EfficientNetB4(include_top=True, weights=None, classes=num_classes)(inputs)

model = tf.keras.Model(inputs, outputs)
# learning_rate = 0.01
# optimizer = tf.keras.optimizers.Adam(lr=learning_rate)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()
hist = model.fit(train_x, train_y, epochs=5, verbose=2, batch_size=6)

def plot_hist(hist):
  plt.plot(hist.history['accuracy'])
  plt.title('Model Accuracy')
  plt.ylabel('Accuracy')
  plt.xlabel('epoch')
  plt.legend(['train','validation'], loc='upper left')
  plt.show

plot_hist(hist)

preds = model.evaluate(test_x, test_y)
print("Loss = ", str(preds[0]))
print("Accuracy = ", str(preds[1]))

import tensorflow as tf
from tensorflow import keras
from keras.preprocessing import image
from keras.applications.efficientnet import preprocess_input
from matplotlib.pyplot import imread
from matplotlib.pyplot import imshow


img_path = "/content/drive/MyDrive/Data Analysis/image_1.png"

img = cv2.imread(img_path)
img = cv2.resize(img, (380, 380))
x = tf.keras.preprocessing.image.img_to_array(img)

# x = np.array(img)
x = np.expand_dims(img, axis=0)
x = preprocess_input(x)
print("Input image: ", x.shape)

my_image = imread(img_path)
imshow(my_image)

preds = model.predict(x)


# predicted_class = np.argmax(preds)
print("cancer[0], non cancer[1]")
# predicted_class
preds

"""Succesfully Done"""