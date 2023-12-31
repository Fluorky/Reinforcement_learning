# -*- coding: utf-8 -*-
"""Kopia notatnika CartPole_Q_learning_NN_ER.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aTG9gBNHnVPipGjkeObTaHwJ3kZIlWyF
"""

import numpy as np
import gym
import matplotlib.pyplot as plt

env = gym.make("CartPole-v1")
state = env.reset()
state
# position, velocity, angle, angular velocity

import keras
from keras.models import Sequential
from keras.layers import Dense
from collections import deque
import random
import tensorflow as tf

model = Sequential()
model.add(Dense(units = 50, input_dim=4, activation='relu'))
model.add(Dense(units = 50, activation = "relu"))
model.add(Dense(units = 2, activation = "linear"))

opt = tf.keras.optimizers.Adam(learning_rate=0.001)
#opt = tf.keras.optimizers.SGD(learning_rate=0.001)

model.compile(loss='MSE',optimizer=opt)
model.summary()

"""Parametry:"""

train_episodes = 100
epsilon = 0.16
gamma = 0.99
max_steps = 50

"""Definiujemy **pamięć** jako kolejkę:"""

memory = deque(maxlen=100)

"""Ustalamy rozmiar **batch**:"""

batch_size = 10

def train():
  state_batch, Qs_target_batch = [], []
  
  minibatch = random.sample(memory, batch_size)
      
  for state, action, reward, next_state, done in minibatch:

    if done:
      y = reward
    else:
      y = reward + gamma*np.max(model.predict(next_state)[0])

    Q_target = model.predict(state)
    Q_target[0][action] = y
          
    state_batch.append(state)
    Qs_target_batch.append(Q_target)      
  
  state_batch = np.array(state_batch).reshape(batch_size,4)
  Qs_target_batch = np.array(Qs_target_batch).reshape(batch_size,2)

  h = model.fit(state_batch,Qs_target_batch,epochs=1,verbose=0)

  loss = h.history['loss'][0]

  return loss

Loss = []
Rewards = []

for e in range(1, train_episodes+1):
  total_reward = 0
  t = 0

  state = env.reset()
  state = np.reshape(state, [1, 4])  
  
  done = False
  while t < max_steps and done == False:
      
    Qs = model.predict(state)[0]

    if np.random.rand()<epsilon:
      action = env.action_space.sample()
    else:
      action = np.argmax(Qs)
    
    next_state, reward, done, _ = env.step(action)
    next_state = np.reshape(next_state, [1, 4])
    
    total_reward += reward

    memory.append((state,action,reward,next_state,done))

    if batch_size < len(memory):
      loss = train()
      Loss.append(loss)

    state = next_state
    t+=1
  
  print(e," R=",total_reward)
  Rewards.append(total_reward)

plt.subplot(211)
plt.ylabel('rewards')  
plt.title('Rewards per epoch')
plt.plot(range(len(Rewards)),Rewards,"b")

plt.subplot(212)
plt.xlabel('epoch')
plt.ylabel('loss')  
plt.title('Loss per epoch')
plt.plot(range(len(Loss)),Loss,"r")

plt.show()