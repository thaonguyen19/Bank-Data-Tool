#from data_processing import *
from input_processing import *

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD
from sklearn.cross_validation import train_test_split

Dx = 50
Dy = 5
N = 239232
batch_size = 64
lr = 0.0001
Dh = 10
nb_epoch = 10

#momentum

#input: N x Dx
#hidden: N x Dh
#output: N x Dy


def NN_model(Dx=50, Dy=5, Dh=30, lr=0.001):
    model = Sequential()
    model.add(Dense(Dh, input_dim=Dx, init='uniform', bias=True))
    model.add(Activation("sigmoid"))
    model.add(Dense(output_dim=Dy, init='uniform', bias=True))
    model.add(Activation("softmax"))
    model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=lr), metrics=['accuracy']) #momentum=0.9, nesterov=True
    return model



# class TextNN:
#     def __init__(self, Dx=50, Dy=5, Dh=30, lr=0.001):	# need to input N as well?
#         self.dx = Dx
#         self.dy = Dy
#         self.dh = Dh
#         self.lr = lr

#         model = Sequential()
#         model.add(Dense(Dh, input_dim=Dx, init='uniform', bias=True))
#         model.add(Activation("relu"))
#         model.add(Dense(output_dim=Dy, init='uniform', bias=True))
#         model.add(Activation("softmax"))
#         model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=lr, momentum=0.9, nesterov=True))
#         self.model = model

#     def fit(self, X_train, Y_train, X_test, Y_test, batch_size=64, nb_epoch=10):
#         #batch_size: number of samples per gradient update
#         self.model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch, verbose=1, validation_split=0.2)

#     # def save_weights(self, fname='../data/model.h5'):
#     #     self.model.save_weights(fname)

#     def evaluate(self, batch_sz=64):
#         return self.model.evaluate(X_test, Y_test, batch_size=batch_sz, verbose=1)

#     def predict(self, X):
#         return self.model.predict(X, verbose=1)



#if __name__ == "__main__":
print("Processing data...")

print("Train test split...")
X_train, X_test, Y_train, Y_test = train_test_split(inputs, outputs, test_size=0.2, random_state=42)

print("Training...")
clf = NN_model(Dx, Dy, Dh, lr)
history = clf.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=10, verbose=1, validation_split=0.2)
print ("History_clf: ", history.history)

print("Evaluation on test set...")
scores = clf.evaluate(X_test, Y_test, batch_size=batch_size, verbose=1)
print("Accuracy: %.2f%%" % (scores[1]*100))


# print("Dumping the model...")
# clf.save_weights(fname='../data/cnn_diff_filter.h5')









