# -*- coding: utf-8 -*-
"""Cars.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15h6jYOflAzXtWd4KIJs6ggFKzrd72SGm

# **Acceptability of Cars**
Have you ever wondered if a car was acceptable or not? It could very well be that you are looking to buy a new car! Thankfully, this process is made easier due to machine learning. In this Colab, we will try to create a model that will help us decide whether or not to buy a car depending on some of its features.

# **Dataset**
The dataset we will be using is from the UCI Machine Learning Repository.

[Car Evaluation](https://archive.ics.uci.edu/ml/datasets/Car+Evaluation)

# **Setup**
Before we begin, we must import tensorflow as well as pandas to extract and manipulate the data in our dataset.
"""

# Commented out IPython magic to ensure Python compatibility.
try:
#   %tensorflow_version 2.x
except:
  Exception
import tensorflow as tf

import pandas as pd

"""# **Load Data**
Okay, now we can read the .data file from the repository and create our own headers following the attributes listed in the .c45-names file. Then we can inspect the dataframe to see what we are dealing with.
"""

car_data = pd.read_csv("/content/car.data", header=None, names=["buying", "maintenance", "doors", "persons", "lug_boot", "safety", "class"])

print(car_data)

"""After inspecting, we can see that all the columns are in the string datatype. It looks like we will need to convert all of the columns into features that our model can understand. Let's first open the .c45-names file to see what values the columns contain."""

attributes = open("/content/car.c45-names", "r")
print(attributes.readlines())

"""Now we can create lists with the labels that the attributes define. We can also import numpy to extract the data as numpy arrays."""

import numpy as np

buy_attr = ["vhigh", "high", "med", "low"]
lug_attr = ["small", "med", "big"]
doors_attr = ["2", "3", "4", "5more"]
ppl_attr = ["2", "4", "more"]
safety_attr = ["low", "med", "high"]
class_lbls = ["unacc", "acc", "good", "vgood"]

"""Here, we can define a function that takes in a column of data along with its specified attributes so that we can encode the attributes as integers. We also have to return a tensor so that our model can use the data. After defining the function, we can call it on every column along with its attribute."""

def convert_to_features(data_col, labels):
  data = data_col.copy()
  for i, info in enumerate(data):
    data[i] = labels.index(info)
  return tf.convert_to_tensor(data.values, np.float32)

buy_features = convert_to_features(car_data["buying"], buy_attr)
maint_features = convert_to_features(car_data["maintenance"], buy_attr)
lug_features = convert_to_features(car_data["lug_boot"], lug_attr)
safety_features = convert_to_features(car_data["safety"], safety_attr)
labels = convert_to_features(car_data["class"], class_lbls)
ppl_features = convert_to_features(car_data["persons"], ppl_attr)
doors_features = convert_to_features(car_data["doors"], doors_attr)

import tensorflow.keras.layers as layers

"""# **Build the Model**
Now, we can begin building the model. Since there are six feature columns, we have to create six input layers which will take in a single integer. Then we concatenate the input layers together to create one layer for our output layer to take in. Lastly, we will use a softmax activation for our last dense layer and 4 units to output the probabilities of each class for our input. Afterwards, we can compile the model with the accuracy metrics so we can evaluate it later. Finally, we can fit the model on our training data.
"""

buy_input = layers.Input(shape=(1,))
maint_input = layers.Input(shape=(1,))
doors_input = layers.Input(shape=(1,))
ppl_input = layers.Input(shape=(1,))
lug_input = layers.Input(shape=(1,))
safety_input = layers.Input(shape=(1,))
input_features = layers.concatenate([buy_input, maint_input, doors_input, ppl_input, lug_input, safety_input])
output = layers.Dense(128, activation="relu")(input_features)
output = layers.Dense(256, activation="relu")(output)
output = layers.Dense(64, activation="relu")(output)
output = layers.Dense(4, activation="softmax")(output)
model = tf.keras.Model(inputs=[buy_input, maint_input, doors_input, ppl_input, lug_input, safety_input], outputs=output)

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

history = model.fit([buy_features, maint_features, doors_features, ppl_features, lug_features, safety_features], labels, epochs=20, batch_size=128)

"""# **Plot the Metrics**
We can see how well our model performed by plotting the accuracy and loss metrics we saved in the history of our model. From what we can see, the model seemed to have performed pretty well on the dataset by reaching and accuracy of over 95% near the end of training.
"""

import matplotlib.pyplot as plt

epochs = range(20)
acc = history.history["accuracy"]
loss = history.history["loss"]

plt.figure(figsize=(16, 12))
plt.subplot(1, 2, 1)
plt.plot(epochs, acc)
plt.title("Model Accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.subplot(1, 2, 2)
plt.plot(epochs, loss)
plt.title("Model Loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")

"""# **Predict**
Now that we have fitted the model, we are able to make some predictions with it. Here, we will create a test input which has high cost, high maintenance, 2 doors, 2 seats, medium lug boots, and medium safety. This input cleary should output unacceptable as there are many more negative features than positive ones.
"""

test_feature = [np.array([0]), np.array([0]), np.array([0]), np.array([0]), np.array([1]), np.array([1])]
prediction = model.predict(test_feature)
predicted_lbl = tf.argmax(prediction, axis=-1)
print(class_lbls[predicted_lbl[0]])

"""Great! It looks like our model predicted correctly! Now, we can use this model to predict other cars for their acceptability with high confidence!"""