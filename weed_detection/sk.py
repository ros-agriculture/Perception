from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from matplotlib import pyplot as plt
from typing import Tuple


def load_data():
    digits = load_digits()
    data = digits['data']
    target = digits['target']
    return data, target

data, target = load_data()

X_train = data[:1500]
y_train = target[:1500]

X_test = data[1500:]
y_test = target[1500:]

model = LogisticRegression()
model.fit(X_train, y_train)

pred = model.predict(X_test)

#metrics

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, pred)
a = accuracy_score(y_test,pred)

#Visualize
fig, ax = plt.subplots()
colorbar = ax.matshow(cm)
fig.colorbar(colorbar)
fig.suptitle("Confusion")
fig.savefig('cm.png')