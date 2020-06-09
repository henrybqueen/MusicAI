from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.callbacks import ModelCheckpoint
import numpy as np
import pandas as pd

seq_length = 60
n_features = 1


x = np.load("X.npy")
y = np.load("Y.npy")

vocab = np.unique(y)
n_vocab = len(vocab)
y = pd.get_dummies(y)

char2idx = {u:i for i, u in enumerate(vocab)}
idx2char = np.array(vocab)

x = np.vectorize(char2idx.get)(x)


model = Sequential()

model.add(LSTM(256, input_shape=(seq_length, n_features), return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(512, return_sequences=True))
model.add(LSTM(256))
model.add(Dense(256))
model.add(Dropout(0.3))
model.add(Dense(n_vocab, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop')


filepath = "MODEL.hdf5"
checkpoint = ModelCheckpoint(
    filepath, monitor='loss',
    verbose=0,
    save_best_only=True,
    mode='min'
)
callbacks_list = [checkpoint]
model.fit(x, y, epochs=200, batch_size=32, callbacks=callbacks_list)

