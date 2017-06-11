from __future__ import print_function
modulePath = 'cpl_lib/' # change as appropriate
import sys
import os
sys.path.append(modulePath)
# now you're good to import the modules
import dspUtil
import praatTextGrid
import scipy.io.wavfile as wav 
import myWave
import audioop
import numpy as np

import os
import matplotlib.pyplot as plt
from sklearn import datasets, metrics, linear_model, naive_bayes, neighbors, tree, svm, neural_network, externals
from freq_reaper import FreqReaper


#1 = Anger
#2 = Despair
#3 = Happiness
#4 = Neutral
#5 = Sadness

# ANGER

def calculateFeatures(wav_pathname):
   numChannels, numFrames, fs_rate, sig = myWave.readWaveFile(wav_pathname)
   signal_data = sig[0]
   F0_arr = []
   RMS_arr = []
   utterance = signal_data
   # result =  dspUtil.calculateF0OfSignal(signal_data, fs_rate, tmpDataPath='temp/', \
   #     tStart=start_t, tEnd=end_t)
   F0_result = dspUtil.calculateF0once(utterance, fs_rate)
   #RMS_result = dspUtil.calculateRMSOnce(utterance)
   RMS_result = audioop.rms(utterance, 2)
   F0_arr.append(F0_result)
   RMS_arr.append(RMS_result)
   # print("F0: ", F0_result)
   # print("RMS: ", RMS_result)
   vec = packageFeatures(F0_arr, RMS_arr)
   return vec


def getFeatFromSign(signal_data, fs_rate):
  
  F0_arr = []
  RMS_arr = []
  F0_result = dspUtil.calculateF0once(signal_data, fs_rate)
  #RMS_result = dspUtil.calculateRMSOnce(utterance)
  RMS_result = audioop.rms(signal_data, 2)
  F0_arr.append(F0_result)
  RMS_arr.append(RMS_result)
  # print("F0: ", F0_result)
  # print("RMS: ", RMS_result)
  vec = packageFeatures(F0_arr, RMS_arr)
  return vec

def packageFeatures(F0, RMS):
        F0_min = min(F0)
        F0_max = max(F0)
        FSum = sum(F0)
        F0_mean = FSum/len(F0)
        F0_std = np.std(F0)
        F0_range = F0_max - F0_min


        RMS_min = min(RMS)
        RMS_max = max(RMS)
        RSum = sum(RMS)
        RMS_mean = RSum/len(RMS)
        RMS_std = np.std(RMS)
        RMS_range = RMS_max - RMS_min

        # print(F0_min, F0_max, F0_mean, F0_std, F0_range)
        # print(RMS_min, RMS_max, RMS_mean, RMS_std, RMS_range)
        # (rate,sigData) = wav.read(pathname)
        # print(rate, sigData)
        # numChannels, numFrames, fs, data = myWave.readWaveFile(pathname)
        # print(numChannels, numFrames, fs)
        return [F0_min, F0_max, F0_mean, F0_std, F0_range, RMS_min, RMS_max, RMS_mean, RMS_std, RMS_range]



def main():
  labels_train = []
  features_train = []
  labels_test = []
  features_test = []

  for filename in os.listdir("Emotional Data/train/anger"):
      if filename.endswith(".wav"):
          feature_list = calculateFeatures("Emotional Data/train/anger/" + filename)
          features_train.append(feature_list)
          labels_train.append(1)

  for filename in os.listdir("Emotional Data/train/despair"):
      if filename.endswith(".wav"):
          feature_list = calculateFeatures("Emotional Data/train/despair/" + filename)
          features_train.append(feature_list)
          labels_train.append(2)

  for filename in os.listdir("Emotional Data/train/happiness"):
      if filename.endswith(".wav"):
          feature_list = calculateFeatures("Emotional Data/train/happiness/" + filename)
          features_train.append(feature_list)
          labels_train.append(3)

  for filename in os.listdir("Emotional Data/train/neutral"):
      if filename.endswith(".wav"):
          feature_list = calculateFeatures("Emotional Data/train/neutral/" + filename)
          features_train.append(feature_list)
          labels_train.append(4)

  for filename in os.listdir("Emotional Data/train/sadness"):
      if filename.endswith(".wav"):
          feature_list = calculateFeatures("Emotional Data/train/sadness/" + filename)
          features_train.append(feature_list)
          labels_train.append(5)

  for filename in os.listdir("Emotional Data/test/anger"):
      if filename.endswith(".wav"):
          feature_list = calculateFeatures("Emotional Data/test/anger/" + filename)
          features_test.append(feature_list)
          labels_test.append(1)

  for filename in os.listdir("Emotional Data/test/despair"):
      if filename.endswith(".wav"):
          feature_list = calculateFeatures("Emotional Data/test/despair/" + filename)
          features_test.append(feature_list)
          labels_test.append(2)

  for filename in os.listdir("Emotional Data/test/happiness"):
      if filename.endswith(".wav"):
          feature_list = calculateFeatures("Emotional Data/test/happiness/" + filename)
          features_test.append(feature_list)
          labels_test.append(3)

  for filename in os.listdir("Emotional Data/test/neutral"):
      if filename.endswith(".wav"):
          feature_list = calculateFeatures("Emotional Data/test/neutral/" + filename)
          features_test.append(feature_list)
          labels_test.append(4)

  for filename in os.listdir("Emotional Data/test/sadness"):
      if filename.endswith(".wav"):
          feature_list = calculateFeatures("Emotional Data/test/sadness/" + filename)
          features_test.append(feature_list)
          labels_test.append(5)

  X = features_train
  y = labels_train

  X_test = features_test
  y_test = labels_test

  # LOGISTIC REGRESSION

  # fit a logistic regression model to the data
  logistic = linear_model.LogisticRegression()
  logistic.fit(X,y)
  externals.joblib.dump(logistic, 'models/emotions/logistic.pkl')
  print(logistic)

  # make predictions
  expected = y
  predicted = logistic.predict(X)

  # summarize the fit of the model
  print(metrics.classification_report(expected, predicted))
  print(metrics.confusion_matrix(expected, predicted))

  expected = y_test
  predicted = logistic.predict(X_test)
  print(metrics.classification_report(expected, predicted))
  print(metrics.confusion_matrix(expected, predicted))


  # GAUSSIAN NAIVE BAYES

  # fit a Naive Bayes model to the data
  gaussian = naive_bayes.GaussianNB()
  gaussian.fit(X, y)
  externals.joblib.dump(gaussian, 'models/emotions/gaussian.pkl')
  print(gaussian)

  # make predictions
  expected = y
  predicted = gaussian.predict(X)

  # summarize the fit of the model
  print(metrics.classification_report(expected, predicted))
  print(metrics.confusion_matrix(expected, predicted))

  expected = y_test
  predicted = gaussian.predict(X_test)
  print(metrics.classification_report(expected, predicted))
  print(metrics.confusion_matrix(expected, predicted))


  # K-NEAREST NEIGHBORS

  # fit a k-nearest neighbor model to the data
  k_neighbors = neighbors.KNeighborsClassifier()
  k_neighbors.fit(X, y)
  externals.joblib.dump(k_neighbors, 'models/emotions/k_neighbors.pkl')
  print(k_neighbors)

  # make predictions
  expected = y
  predicted = k_neighbors.predict(X)

  # summarize the fit of the model
  print(metrics.classification_report(expected, predicted))
  print(metrics.confusion_matrix(expected, predicted))

  expected = y_test
  predicted = k_neighbors.predict(X_test)
  print(metrics.classification_report(expected, predicted))
  print(metrics.confusion_matrix(expected, predicted))


  # DECISION TREE CLASSIFIER

  # fit a CART model to the data
  decision_tree = tree.DecisionTreeClassifier()
  decision_tree.fit(X, y)
  externals.joblib.dump(decision_tree, 'models/emotions/decision_tree.pkl')
  print(decision_tree)

  # make predictions
  expected = y
  predicted = decision_tree.predict(X)

  # summarize the fit of the model
  print(metrics.classification_report(expected, predicted))
  print(metrics.confusion_matrix(expected, predicted))

  expected = y_test
  predicted = decision_tree.predict(X_test)
  print(metrics.classification_report(expected, predicted))
  print(metrics.confusion_matrix(expected, predicted))


  # SUPPORT VECTOR MACHINES

  # fit a SVM model to the data
  svm = svm.SVC()
  svm.fit(X, y)
  externals.joblib.dump(svm, 'models/emotions/svm.pkl')
  print(svm)

  # make predictions
  expected = y
  predicted = svm.predict(X)

  # summarize the fit of the model
  print(metrics.classification_report(expected, predicted))
  print(metrics.confusion_matrix(expected, predicted))

  expected = y_test
  predicted = svm.predict(X_test)
  print(metrics.classification_report(expected, predicted))
  print(metrics.confusion_matrix(expected, predicted))


  #NEURAL NETWORK

  nn = neural_network.MLPClassifier()
  nn.fit(X, y)
  externals.joblib.dump(nn, 'models/emotions/nn.pkl')
  print(nn)

  # make predictions
  expected = y
  predicted = nn.predict(X)

  # summarize the fit of the model
  print(metrics.classification_report(expected, predicted))
  print(metrics.confusion_matrix(expected, predicted))

  expected = y_test
  predicted = nn.predict(X_test)
  print(metrics.classification_report(expected, predicted))
  print(metrics.confusion_matrix(expected, predicted))

if __name__ == '__main__':
  main()