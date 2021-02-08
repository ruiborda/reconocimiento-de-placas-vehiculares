from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import os
import numpy as np
import cv2
import csv
import pandas as pd
from sklearn import metrics
import seaborn as sns
import matplotlib.pyplot as plt
import joblib  ##C:\Users\LENOVO\Desktop\RECONOCIMIENTO DE PATRONES CURSO\APP\img

dir_dataset = "dataset"
dir_letters = os.listdir(dir_dataset)

print("cargando imagenes")
with open('dataset.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for dir_letter in dir_letters:
        path = os.path.join(dir_dataset, dir_letter)
        print(dir_letter)
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                img = cv2.imread(os.path.join(path, file))
                gris = cv2.cvtColor(cv2.resize(img, (34, 34)), cv2.COLOR_BGR2GRAY)
                fila = gris.reshape(1, -1)
                a = np.append(fila, str(dir_letter)).reshape(1, -1)
                writer.writerows(a)

print("leyendo dataset")
df = pd.read_csv('dataset.csv', header=None)
print(df.count(axis='columns'))
X = np.array(df.drop([1156], axis=1))
y = df[1156]
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.10)
x_train = X
y_train = y
y_train = y_train.astype('category')
regresionL = LogisticRegression(solver='liblinear', max_iter=100)
regresionL.fit(x_train, y_train)
predicciones = regresionL.predict(x_test)
score = regresionL.score(x_test, y_test)
print("El score es: ", score)
# MATRIZ DE CONFUSION
mc = metrics.confusion_matrix(y_test, predicciones)
print(mc)
# representación gráfica de la matriz
plt.figure(figsize=(9, 9))
sns.heatmap(mc, annot=True, cmap='Blues_r')
plt.xlabel('valor predicho')
plt.ylabel('valor real')
plt.title("Puntuación:{0}".format(score), size=15)
plt.show()
# EXTRAYENDO MI MODELO
joblib.dump(regresionL, 'modelo_entrenado.pkl')
