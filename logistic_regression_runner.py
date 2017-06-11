import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, metrics, linear_model, naive_bayes, neighbors, tree, svm, neural_network, externals
import csv
from freq_reaper import FreqReaper
import pandas as pandas
#import tensorflow as tf


freq_reaper = FreqReaper()

X = pandas.read_csv('prosody_features_np.csv')
# X_append = freq_reaper.runAll()
emotion_model = externals.joblib.load('models/emotions/k_neighbors.pkl')
X_emotions = emotion_model.predict(X)
X_emotions = np.atleast_2d(X_emotions).transpose()
# X = np.hstack((X, X_append))
# X = np.hstack((X, X_emotions))

y = pandas.read_csv('all_outcomes.csv')

y = y['label']

X_test = X[X.shape[0] - 41: X.shape[0] - 1][:]
y_test = y[len(y) - 41:len(y) - 1]

X = X[: X.shape[0] - 41][:]
y = y[:len(y) - 41]

# LOGISTIC REGRESSION

# fit a logistic regression model to the data
logistic = linear_model.LogisticRegression()
logistic.fit(X,y)
externals.joblib.dump(logistic, 'models/logistic2.pkl')
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
externals.joblib.dump(gaussian, 'models/gaussian2.pkl')
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
externals.joblib.dump(k_neighbors, 'models/k_neighbors2.pkl')
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
externals.joblib.dump(decision_tree, 'models/decision2_tree.pkl')
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
externals.joblib.dump(svm, 'models/svm2.pkl')
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

nn = neural_network.MLPClassifier(shuffle=False, random_state=4)
nn.fit(X, y)
externals.joblib.dump(nn, 'models/nn2.pkl')
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


#TENSORFLOW NEURAL NETWORK
#feature_columns = [tf.contrib.layers.real_valued_column("", dimension = 4)]
#tf_nn = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns, hidden_units=[10, 20, 10])
#tf_nn.fit(input_fn=(X, y), steps=2000)

