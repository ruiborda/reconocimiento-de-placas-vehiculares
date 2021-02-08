import cv2
import random
import numpy
import joblib

caracter_modelo = joblib.load('modelo_entrenado.pkl')


def box_placa(image):
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
                b_l, l = box_letters_from_placa(image[y:y + h, x:x + w])
                box_letters.append(b_l)
                letters.append(l)

    return [placas, box_letters, letters]


def box_letters_from_placa(image):
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
            # cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 1)
            # para dibujar el los bordes de los caracteres encontrados
            # cv2.drawContours(image, [c], -1, (0, 255, 0), 1)
    # cv2.imshow(str(random.randint(100000000, 999999999)), image)
    result = []
    for item in box_letters:
        if item not in result:
            result.append(item)

    if len(result) > 0:
        for box in result:
            x, y, h, w = box
            caracter = image[y:y + w, x:x + h]
            letters.append(pred_caracter(caracter))
            # cv2.imshow(str(random.randint(100000000, 999999999)), caracter)
    # box_letters,letters
    return [result, letters]


def pred_caracter(img):
    out_name = "cache/" + str(random.randint(100000000, 999999999)) + ".jpg"

    gray = cv2.cvtColor(cv2.resize(img, (34, 34)), cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    cv2.imwrite(out_name, gray)

    X = numpy.array(gray).reshape(1, -1)
    vocal = caracter_modelo.predict(X)
    return vocal


image = cv2.imread('out.png')
placas, box_letters, letters = box_placa(image)
print(placas)
for placa, codigo, letters in zip(placas, box_letters, letters):
    codigo_placa=""

    x, y, w, h = placa
    cv2.rectangle(image, (x, y), (w, h), (255, 0, 0), 3)
    # cv2.imshow(str(random.randint(100000000, 999999999)) + "o", image)
    # cv2.putText(image, codigo[0], (x - 20, y - 10), 1, 2.2, (0, 255, 0), 2)
    cv2.imshow('Frame_video', image)

    for letra in letters[::-1]:
        codigo_placa+=letra

    print(codigo_placa)

cv2.waitKey(0)
