import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from keras import backend as K
from sklearn import preprocessing

dataset = pd.read_csv("../data/labeled_frames.csv").values
dataset['split'] = np.random.randn(dataset.shape[0], 1)

msk = np.random.rand(len(dataset)) <= 0.9

train = dataset[msk]
test = dataset[~msk]

trainX = dataset[:, 1:].reshape(dataset.shape[0],1,28, 28).astype( 'float32' )
x_train = trainX / 255.0

y_train = dataset[:,0]

print('Training data shape : ',x_train.shape, y_train.shape)

lb = preprocessing.LabelBinarizer()
y_train = lb.fit_transform(y_train)

model = Sequential()
K.set_image_dim_ordering('th')
model.add(Convolution2D(30, 5, 5, border_mode= 'valid' , input_shape=(1, 28, 28),activation= 'relu' ))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Convolution2D(15, 3, 3, activation= 'relu' ))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(128, activation= 'relu' ))
model.add(Dense(50, activation= 'relu' ))
model.add(Dense(10, activation= 'softmax' ))

model.compile(loss= 'categorical_crossentropy' , optimizer= 'adam' , metrics=[ 'accuracy' ])

model.fit(X_train, y_train,
          epochs=20,
          batch_size= 160)