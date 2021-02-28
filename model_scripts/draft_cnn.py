import numpy as np 
import pandas as pd 
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from collections import Counter
import keras
from keras.models import Sequential 
from keras.layers import Activation, MaxPooling1D, Dropout, Flatten, Reshape, Dense, Conv1D, LSTM,SpatialDropout1D
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
import seaborn as sns
import os
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.metrics import precision_score, recall_score, accuracy_score, balanced_accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from random import randrange
from random import seed
from random import random
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import sklearn.metrics as metrics
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
import seaborn as sns
import pickle
from sklearn.metrics import precision_score, recall_score, accuracy_score, balanced_accuracy_score, f1_score
import os
import pandas as pd

df = pd.read_csv("/kaggle/input/1d-labeled-frames/final_labeled_frames.csv", error_bad_lines=False)

print(df.shape)
p = df['Phoneme'].unique()
print(len(p))
from sklearn.preprocessing import LabelEncoder

labelencoder = LabelEncoder()
df['Phoneme'] = labelencoder.fit_transform(df['Phoneme'])


labels = np.asarray(df[['Phoneme']].copy())
print(labels.shape)
labels

df = df.drop(df.columns[0], axis = 1)
X_train, X_test, y_train, y_test = train_test_split(df, labels, random_state = 42, test_size = 0.2, stratify = labels)
X_train = tf.reshape(X_train, (8084, 19200, 1))
X_test = tf.reshape(X_test, (2021, 19200, 1))

model = Sequential()
model.add(Conv1D(filters= 64, kernel_size=3, activation ='relu',strides = 2, padding = 'valid', input_shape= (19200, 1)))
model.add(MaxPooling1D(pool_size=2))
model.add(Conv1D(filters= 128, kernel_size=3, activation ='relu',strides = 2, padding = 'valid'))
model.add(MaxPooling1D(pool_size=2))

model.add(Dropout(0.9))
model.add(MaxPooling1D(pool_size=2))

model.add(Flatten())
model.add(Dense(39)) 
model.add(Activation('softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()


history = model.fit(X_train,y_train, epochs = 30, batch_size = 256, validation_data = (X_test, y_test), shuffle = True)


def plot_acc(h):
    plt.plot(h.history['accuracy'])
    plt.plot(h.history['val_accuracy'])

    plt.title('model accuracy')
    plt.ylabel('accuracy and loss')
    plt.xlabel('epoch')

    plt.legend(['acc', 'val acc' ], loc='upper left')
    plt.show()
#plot the loss and validation loss
def plot_loss(h):
    plt.plot(h.history['loss'][1:])
    plt.plot(h.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('accuracy and loss')
    plt.xlabel('epoch')

    plt.legend(['loss', 'val loss' ], loc='upper left')
    plt.show()


preds = model.predict_classes(X_test)
print("Accuracy = {}".format(accuracy_score(y_test, preds)))
print("Balanced Accuracy = {}".format(balanced_accuracy_score(y_test, preds)))
print("Precision = {}".format(precision_score(y_test, preds, average='macro')))
print("Recall = {}".format(recall_score(y_test, preds, average='macro')))
print("F1 = {}".format(f1_score(y_test, preds, average='weighted')))




model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("model.h5")

preds = model.predict_classes(X_test)

ticks = []
for i in range(len(arr)):
    ticks.append(float(i + 0.5))

label_map = {'0':'aa','1':'ae','2':'ah','3':'ao','4':'aw','5':'ay','6':'b','7':'ch','8':'d','9':'dh','10':'eh','11':'er','12':'ey','13':'f','14':'g','15':'hh','16':'ih','17':'iy','18':'jh','19':'k','20':'l','21':'m','22':'n','23':'ng','24':'ow','25':'oy','26':'p','27':'r','28':'s','29':'sh','30':'t','31':'th','32':'uh','33':'uw','34':'v','35':'w','36':'y','37':'z','38':'zh'}
def plot_confusion_matrix(y_true,y_predicted, ticks):
	cm = metrics.confusion_matrix(y_true, y_predicted)
	l = list(cm)
	#print(l)

	s = 0

	for array in l:
		for value in array:
			s += value

	ooga = []
	counter = 0
	for array in l:
		array = list(array)
		array = [round(x /mapping[counter],3)  for x in array]
		ooga.append(array)
		counter += 1

	write_cm(ooga)
	labels = list(label_map.values())


	df_cm = pd.DataFrame(ooga,index = labels,columns = labels)
	plt.figure(figsize=(20,10)) 

	ax = sns.heatmap(df_cm, annot=True,cmap='Blues', fmt='g')
	print(type(ax))
   
	plt.yticks(ticks, labels,va='center')
	plt.ylabel('True label')
	plt.xlabel('Predicted label')
 
	plt.show()
	plt.close()
