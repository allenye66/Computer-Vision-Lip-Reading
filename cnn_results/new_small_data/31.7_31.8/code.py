with tpu_strategy.scope():

    model = Sequential()
    
    model.add(Conv1D(filters= 128, kernel_size=3, activation ='relu',strides = 2, padding = 'valid', input_shape= (4096, 1)))
    model.add(MaxPooling1D(pool_size=2))
    
    model.add(Dropout(0.2))
    model.add(MaxPooling1D(pool_size=2))
    
    model.add(Conv1D(filters= 256, kernel_size=3, activation ='relu',strides = 2, padding = 'valid'))
    model.add(MaxPooling1D(pool_size=2))

    model.add(Dropout(0.2))
    model.add(MaxPooling1D(pool_size=2))
    
    model.add(Conv1D(filters= 512, kernel_size=3, activation ='relu',strides = 2, padding = 'valid'))
    model.add(MaxPooling1D(pool_size=2))

    model.add(Dropout(0.2))
    model.add(MaxPooling1D(pool_size=2))
    
    model.add(Conv1D(filters= 1024, kernel_size=3, activation ='relu',strides = 2, padding = 'valid'))
    model.add(MaxPooling1D(pool_size=2))

    
    model.add(Flatten())
    model.add(Dense(39)) 
    model.add(Activation('softmax'))

    optimizer = keras.optimizers.Adam(lr=0.01)

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


history = model.fit(X_train,y_train, epochs = 200, batch_size = 128, validation_data = (X_test, y_test), shuffle = True)
