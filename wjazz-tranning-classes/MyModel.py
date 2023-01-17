import tensorflow as tf
import numpy as np

class MyModel:

  def __init__(self, input_shape, output_shape, opts):
    self.hidden_dim = opts["hidden_dim"]
    self.winsize = opts["winsize"]
    self.division = opts["division"]
    self.model = self.make_model(input_shape, output_shape, self.division, 
                                 self.winsize, self.hidden_dim)

  @staticmethod
  def myaccuracy(x, y):
    xx = tf.math.argmax(x, axis=2)
    yy = tf.math.argmax(y, axis=2)
    return tf.math.divide(tf.math.count_nonzero(tf.math.equal(xx, yy)), 
                          tf.math.count_nonzero(tf.math.equal(yy, yy)))

  def make_model(self, shape, out_shape, div, winsize, hidden_dim):
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Conv2D(hidden_dim, (1, shape[1]), 
                                     input_shape=(shape[0], shape[1], 1), 
                                     strides=1, padding="valid", activation="relu"))
    model.add(tf.keras.layers.Dropout(0.25))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Conv2D(hidden_dim, (div*winsize, 1), strides=(div*winsize, 1), 
                                     padding="valid", activation="relu"))
    model.add(tf.keras.layers.Dropout(0.25))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Conv2DTranspose(hidden_dim, (div*winsize, 1), strides=(div*winsize, 1), 
                                              padding="valid", activation="relu"))
    model.add(tf.keras.layers.Dropout(0.25))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Conv2DTranspose(1, (1, out_shape[1]), strides=1, 
                                              padding="valid"))
    model.add(tf.keras.layers.Softmax(axis=2))
    model.compile(optimizer="adam", loss=tf.keras.losses.CategoricalCrossentropy(axis=2))
#    model.compile(optimizer="adam", loss=tf.keras.losses.CategoricalCrossentropy(axis=2), 
#                  metrics=MyModel.myaccuracy)
    model.summary()
    return model

  def fit(self, x_train, y_train, x_test, y_test):
    return self.model.fit(x_train, y_train, epochs=250, batch_size=16, 
              validation_data=(x_test, y_test))
    
  def predict(self, x_test):
    return self.model.predict(x_test)

  def save(self, filename):
    self.model.save(filename)