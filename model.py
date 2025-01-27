from typing import Dict, Text
import pandas as pd
import numpy as np
import tensorflow as tf
from keras import layers

np.set_printoptions(precision=3, suppress=True)


mastery_train = pd.read_csv(
    "data.csv",
    names = ["user_id", "champion_id", "mastery_points"])

# 

mastery_features = mastery_train.copy()
mastery_labels = mastery_features.pop('mastery_points')

inputs = {}
for name, column in mastery_features.items():
    dtype = column.dtype
    if dtype == object:
        dtype = tf.string
    else:
        dtype = tf.float32

    inputs[name] = tf.keras.Input(shape=(1,), name=name, dtype=dtype)

numeric_inputs = {name:input for name,input in inputs.items()
                  if input.dtype==tf.float32}

x = layers.Concatenate()(list(numeric_inputs.values()))
norm = layers.Normalization()
norm.adapt(np.array(mastery_train[numeric_inputs.keys()]))
all_numeric_inputs = norm(x)

preprocessed_inputs = [all_numeric_inputs]

preprocessed_inputs_cat = layers.Concatenate()(preprocessed_inputs)

mastery_preprocessing = tf.keras.Model(inputs, preprocessed_inputs_cat)

tf.keras.utils.plot_model(model = mastery_preprocessing , rankdir="LR", dpi=72, show_shapes=True)

mastery_features_dict = {name: np.array(value) 
                         for name, value in mastery_features.items()}

features_dict = {name:values[:1] for name, values in mastery_features.items()}
mastery_features(features_dict)

def mastery_model(preprocessing_head, inputs):
  body = tf.keras.Sequential([
    layers.Dense(64),
    layers.Dense(1)
  ])

  preprocessed_inputs = preprocessing_head(inputs)
  result = body(preprocessed_inputs)
  model = tf.keras.Model(inputs, result)

  model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                optimizer=tf.keras.optimizers.Adam())
  return model

mastery_model = mastery_model(mastery_preprocessing, inputs)

mastery_model.fit(x=mastery_features, y=mastery_labels, epochs=10)
