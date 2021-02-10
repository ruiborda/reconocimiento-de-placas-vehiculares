# -*- coding: utf-8 -*-
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
import random
import numpy
import joblib
import time

vs = None
estado_camara = False

caracter_modelo = joblib.load('modelo_entrenado.pkl')

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(779, 564)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setStyleSheet("")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMaximumSize(QtCore.QSize(402, 16777215))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.activar_camara = QtWidgets.QPushButton(self.frame_3)
        self.activar_camara.setObjectName("activar_camara")
        self.verticalLayout_2.addWidget(self.activar_camara)
        self.textEdit = QtWidgets.QTextEdit(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.registrar_placa = QtWidgets.QPushButton(self.frame_3)
        self.registrar_placa.setObjectName("registrar_placa")
        self.verticalLayout_2.addWidget(self.registrar_placa)
        self.horizontalLayout.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.video = QtWidgets.QLabel(self.frame_4)
        self.video.setStyleSheet("border:none;\n"
                                 "")
        self.video.setObjectName("video")
        self.horizontalLayout_2.addWidget(self.video)
        self.horizontalLayout.addWidget(self.frame_4)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 200))
        self.frame.setStyleSheet("")
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lista_today = QtWidgets.QListView(self.frame)
        self.lista_today.setObjectName("lista_today")
        self.verticalLayout_3.addWidget(self.lista_today)
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 779, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.activar_camara.setText(_translate("MainWindow", "Activar Cámara"))
        self.registrar_placa.setText(_translate("MainWindow", "Registrar Placa"))
        self.video.setText(_translate("MainWindow", "video"))

    def capturar_video(self):
        if estado_camara:
            ret, frame = vs.read()

            # start

            placas, box_letters, letters = self.box_placa(frame)
            print(placas)
            for placa, codigo, letters in zip(placas, box_letters, letters):
                if len(letters) == 8:
                    codigo_placa = ""
                    x, y, w, h = placa
                    cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), 3)
                    # cv2.imshow(str(random.randint(100000000, 999999999)) + "o", image)
                    # cv2.putText(image, codigo[0], (x - 20, y - 10), 1, 2.2, (0, 255, 0), 2)
                    # cv2.imshow('Frame_video', image)

                    for letra in letters[::-1]:
                        codigo_placa += letra[0]

                    self.textEdit.setText(codigo_placa)
                    time.sleep(1)
            # end

            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                             QtGui.QImage.Format_RGB888)
            convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
            pixmap = QPixmap(convertToQtFormat)
            QApplication.processEvents()
            self.video.setPixmap(pixmap)
        else:
            print("enable camara")

    def cambiar_estado_camara(self):
        global vs
        global estado_camara
        if estado_camara == False:
            vs = cv2.VideoCapture(0)
            estado_camara = True
            _translate = QtCore.QCoreApplication.translate
            self.activar_camara.setText(_translate("MainWindow", "Desactivar Cámara"))
            self.activar_camara.setStyleSheet(u"QPushButton {\n"
                                              "  	color: #fff;\n"
                                              "    background-color: #c82333;\n"
                                              "    border-color: #bd2130;\n"
                                              "	border: 1px solid transparent;\n"
                                              " 	  padding: 3px;\n"
                                              "    font-size: 15px;\n"
                                              "    line-height: 1.5;\n"
                                              "    border-radius: 5px;\n"
                                              "}\n"
                                              "\n"
                                              "QPushButton:pressed {\n"
                                              "    background-color: #c82333;\n"
                                              "}\n"
                                              "")

        else:
            vs.release()
            cv2.destroyAllWindows()
            estado_camara = False
            _translate = QtCore.QCoreApplication.translate
            self.activar_camara.setText(_translate("MainWindow", "Activar Cámara"))
            self.activar_camara.setStyleSheet(u"QPushButton {\n"
                                              "  	color: #fff;\n"
                                              "    background-color: #28a745;\n"
                                              "    border-color: #28a745;\n"
                                              "	border: 1px solid transparent;\n"
                                              " 	  padding: 3px;\n"
                                              "    font-size: 15px;\n"
                                              "    line-height: 1.5;\n"
                                              "    border-radius: 5px;\n"
                                              "}\n"
                                              "\n"
                                              "QPushButton:pressed {\n"
                                              "    background-color: green;\n"
                                              "}\n"
                                              "")

    def box_placa(self, image):
        placas = []
        box_letters = []
        letters = []

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur(gray, (3, 3))
        canny = cv2.Canny(gray, 150, 200)
        canny = cv2.dilate(canny, None, iterations=1)

        cnts, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            area = cv2.contourArea(c)
            x, y, w, h = cv2.boundingRect(c)
            # perímetro de contorno
            epsilon = 0.01 * cv2.arcLength(c, True)
            # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html#contour-approximation
            approx = cv2.approxPolyDP(c, epsilon, True)

            if len(approx) == 4 and area > 2000:
                # cv2.drawContours(image, [approx], -1, (0, 255, 0), 3)
                aspect_ratio = float(w) / h
                if aspect_ratio > 2.4:
                    placas.append([x, y, x + w, y + h])
                    b_l, l = self.box_letters_from_placa(image[y:y + h, x:x + w])
                    box_letters.append(b_l)
                    letters.append(l)

        return [placas, box_letters, letters]

    def box_letters_from_placa(self, image):
        box_letters = []
        letters = []
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur(gray, (1, 1))
        canny = cv2.Canny(gray, 150, 200)
        contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            area = cv2.contourArea(c)
            x, y, w, h = cv2.boundingRect(c)
            if 500 > area > 100:
                box_letters.append([x, y, w, h])
                # para dibujar rectangulos de los caracteres detectados
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 1)
                # para dibujar el los bordes de los caracteres encontrados
                #cv2.drawContours(image, [c], -1, (0, 255, 0), 1)
        # cv2.imshow(str(random.randint(100000000, 999999999)), image)
        result = []
        for item in box_letters:
            if item not in result:
                result.append(item)

        if len(result) > 0:
            for box in result:
                x, y, h, w = box
                caracter = image[y:y + w, x:x + h]
                letters.append(self.pred_caracter(caracter))
                # cv2.imshow(str(random.randint(100000000, 999999999)), caracter)
        # box_letters,letters
        return [result, letters]

    def pred_caracter(self, img):
        global caracter_modelo
        out_name = "cache/" + str(random.randint(100000000, 999999999)) + ".jpg"

        gray = cv2.cvtColor(cv2.resize(img, (34, 34)), cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)

        # para generas dataset
        # cv2.imwrite(out_name, gray)

        X = numpy.array(gray).reshape(1, -1)
        vocal = caracter_modelo.predict(X)
        return vocal


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    timer = QTimer()
    timer.timeout.connect(ui.capturar_video)
    timer.start(60)

    ui.activar_camara.clicked.connect(ui.cambiar_estado_camara)

    MainWindow.show()
    sys.exit(app.exec_())
