# -*- coding: utf-8 -*-
"""FrozenLake_Q_learning_NN_MB.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t0yv71aagElEIsuuVlBPBze2cuFtEII4
"""

import numpy as np
import gym
import matplotlib.pyplot as plt
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense

env = gym.make("FrozenLake-v0", map_name='4x4', is_slippery=False)

"""W srodowisku FrozenLake **stany** reprezentowane są za pomocą cyfr **0,1,2,...,15**. Na wejście sieci możemy podać **tensor o kształcie (1,16)**. W związku z tym musimy przekszatałcić stany do odpowieniej postaci. Robimy to w sposób opisany poniżej.

Wykorzystamy **macierz jednostkową o wymiarach 16x16**:
"""

np.identity(16)

state = 0 #dowolna wartość 0,1,2,...,15
state = np.identity(16)[state]
state

"""Wiersze z powyższej macierzy po **zmianie kształtu na (1,16)** będą odpowiednią reprezentacją **stanu**:"""

state = state.reshape(1,16)
state

"""Sień neuronowa **aproksymująca funkcję Q** na wejściu otrzymuje **tensor o kształcie (1,16)**. UWAGA: neurony w warstwie wyjściowej mają **funkcję aktywacji f(x)=x** (DLACZEGO?):"""

model = Sequential()
model.add(Dense(units = 50, input_dim=16, activation='relu'))
model.add(Dense(units = 50, activation = "relu"))
model.add(Dense(units = 4, activation = "linear"))

"""Na wyjściu sieć **zwraca tensor o kształcie (1,4)**. Każda z czterech wartości to wartość **Q** dla stanu **s** i **każdej z możliwych akcji** (0-lewo,1-dół,2-prawo,3-góra):

![image.png](data:image/png;base64,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)
"""

opt = tf.keras.optimizers.Adam(learning_rate=0.001)
#opt = keras.optimizers.SGD(learning_rate=0.001)

model.compile(loss='MSE',optimizer=opt)
model.summary()

"""Parametry uczenia:"""

train_episodes = 100
epsilon = 0.5
gamma = 0.99

epsilon = 1

"""Pętla treningowa:"""

Loss = []
Rewards = []
for e in range(train_episodes):
  
  total_reward = 0
  t = 0
  #epsilon zmieniany po kazdyn epizodzie
  #epsilon = epsilon - (1/train_episodes)

  state = env.reset()
  state = np.identity(16)[state]
  state = np.reshape(state,[1,16])  

  done = False
  while done == False:
    
    Qs = model.predict(state)[0]

    if np.random.rand()<epsilon:
      action = env.action_space.sample()
    else:
      action = np.argmax(Qs)
    
    next_state, reward, done, _ = env.step(action)

    if done:
      if reward == 1:
        reward = 5
      else:
        reward = -5
    else:
      reward = -1

    next_state = np.identity(16)[next_state]
    next_state = np.reshape(next_state, [1, 16])

    Qs_next = model.predict(next_state)[0]

    Qs = np.reshape(Qs,[1,4])    
  
    Qs_target = np.copy(Qs)

 
    if done:
      y = reward
    else:
      y = reward + gamma*np.max(Qs_next)

    Qs_target[0][action] = y


    h = model.fit(state,Qs_target,epochs=1,verbose=0)

  
    loss = h.history['loss'][0]

    state = next_state
    total_reward += reward
    t+=1
  
  if e%10==0:
    print("R=",total_reward," L=",loss)
  
  Rewards.append(total_reward)
  Loss.append(loss)

plt.subplot(211)
plt.ylabel('Suma nagród')  
plt.title('Suma nagród w epizodzie')
plt.plot(list(range(train_episodes)),Rewards,"b")

plt.subplot(212)
plt.xlabel('epizod')
plt.ylabel('błąd')  
plt.title('Loss per epoch')
plt.plot(list(range(train_episodes)),Loss,"r")

plt.show()