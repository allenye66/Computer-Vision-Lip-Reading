model = Sequential()
model.add(Conv1D(filters= 64, kernel_size=3, activation ='relu',strides = 2, padding = 'valid', input_shape= (4096, 1)))
model.add(MaxPooling1D(pool_size=2))
model.add(Conv1D(filters= 128, kernel_size=3, activation ='relu',strides = 2, padding = 'valid'))
model.add(MaxPooling1D(pool_size=2))
model.add(Dropout(0.9))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(39)) 
model.add(Activation('softmax'))
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


history = model.fit(X_train,y_train, epochs = 100, batch_size = 512, validation_data = (X_test, y_test), shuffle = True)
