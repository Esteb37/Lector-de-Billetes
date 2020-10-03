#Proyecto para la materia de Pensamiento Computacional para la Ingeniería
#Esteban Padilla Cerdio
#Última versión - 2/10/2020


import numpy as np
import math
import cv2 #Librería de OpenCV para python
from matplotlib import pyplot as plt



def get_outlines(img): #Función para obtener todos los contornos

    img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Transformar imagen a escala de grises
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(img_grey,(kernel_size, kernel_size),0) #Aplicar desenfoque gausiano para suavizar
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold) #Utilizar el algoritmo Canny para resaltar contornos
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #Extraer todos los contornos continuos
    #cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
    return edges

def get_corners(img): #Función mejorada para obtener las esquinas basada en la función de Harris
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    dst = cv2.dilate(dst,None)

    height, width, channels = img.shape
    blank_image = np.zeros((height,width,3), np.uint8)
    blank_image[dst>0.01*dst.max()]=[0,0,255]

    return blank_image

def delete_clumps(corners,shape): #Función para eliminar puntos acumulados
    radius = 5 #Radio de "soledad" de un punto
    height, width, channels = shape
    positions = [[0]*(width+radius*2)]*(height+radius*2)  #Matriz de posiciones de todos los puntos
    for corner in corners: #Llenamos la matriz con 1 si hay un punto ahí
        if(len(corner)>0):
            positions[corner[1]][corner[0]] = 1
    clean = [] #Lista de puntos no acumulados
    for p in corners:
        quadrants = [0,0,0,0] #Se utilizan los cuadrantes para detectar acumulación
                              #Porque un punto con puntos en más de dos cuadrantes ya
                              #Puede ser considerado un conjunto, si solo es uno
                              #O dos cuadrantes puede ser simplemente una línea
        if(len(p)>0):
            for y in range(p[1]-radius,p[1]+radius+1): #Buscamos las coordenadas dentro del radio
                for x in range(p[0]-radius,p[0]+radius+1):
                    if positions[y][x]!=0 and (y!=p[1] and x!=p[0]): #Si se encuentra un punto
                                                              #Se marca ese cuadrante como "ocupado"
                        if x>=p[0] and y>=p[1]:
                            quadrants[0] = 1
                        elif x<p[0] and y>=p[1]:
                            quadrants[1] = 1
                        elif x<p[0] and y<p[1]:
                            quadrants[2] = 1
                        elif x>=p[0] and y<p[1]:
                            quadrants[3] = 1
            clumps = 0
            for i in range(4):
                clumps+=quadrants[i]
            if(clumps<=2): #Si hay menos de dos cuadrantes ocupados, puede no ser considerado
                            #Una acumulación
                clean.append(p)
    return clean

def getAngle(a,b): #Función para obtener los ángulos entre dos puntos
    if(a[1]-b[1]==0):
        return 0
    elif(a[0]-b[0]==0):
        return 90
    else:
        return math.degrees(math.atan((a[1]-b[1])/(a[0]-b[0])))

def rectangles(img): #Función para encontrar los rectángulos
    corners = get_corners(img) #Conseguimos las esquinas
    diagonals = [] #Lista de puntos con distancias mayores a un mínimo
    for i in range(len(corners)):
        a = corners[i]
        if(len(a)>0                             #Hacemos todos los pares posibles
            for j in range(i+1,len(corners)):
                b = corners[j]
                if(len(b)>0):
                    dist = ((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)

                    if(dist>200): #Si la distancia del par es mayor, puede ser considerada una diagonal
                        angle = getAngle(a,b) #Se guarda el ángulo para después buscar diagonales no paralelas
                        diagonals.append([dist,a,b,angle])

    diagonals.sort(key=lambda x:x[0]) #Se ordenan con base en la distancia
    l = range(len(distances))
    rectangles = []
    for a in diagonals:
        for b in diagonals:
            if a is not b: #Por todos los pares de diagonal posibles
                amag = a[0] #Magnitud de primera diagonal
                bmag = b[0] #Magnitud de diagonal línea
                ap1 = a[1] #Punto 1 de diagonal 1
                ap2 = a[2] #Punto 2 de diagonal 1
                bp1 = b[1] #Punto 1 de diagonal 2
                bp2 = b[2] #Punto 2 de diagonal 2
                aang = a[3] #Ángulo de diagonal 1
                bang = b[3] #Ángulo de diagonal 2
                if(abs(amag-bmag)<5): #Si las diagonales tienen una longitud similar
                    cxa = int((ap2[0]+ap1[0])/2)
                    cya = int((ap2[1]+ap1[1])/2)    #Se buscan los centros de ambas diagonales
                    cxb = int((bp2[0]+bp1[0])/2)
                    cyb = int((bp2[1]+bp1[1])/2)
                    c_diff = ((cxa-cxb)**2+(cya-cyb)**2)**(1/2)  #Se obtiene la distancia entre los centros
                    angle_diff = abs(aang-bang) #se obtiene el ángulo entre ambas diagonales
                    if(c_diff<5 and angle_diff>10): #Si el centro de ambas diagonales está cercano y tienen un ángulo considerable, hemos encontrado un rectángulo
                        rectangles.append([ap1,ap2,bp1,bp2])

    for rect in rectangles:
        cv2.line(img,(rect[0][0],rect[0][1]),(rect[1][0],rect[1][1]),(0,250,0),2)
        cv2.line(img,(rect[2][0],rect[2][1]),(rect[3][0],rect[3][1]),(250,0,0),2)
        cv2.imshow("frame",img)"""



if __name__ == "__main__":
    capture = cv2.VideoCapture(1,cv2.CAP_DSHOW) #Obtener Webcam
    while True:
        ret, img= capture.read() #Obtener imagen de la webcam

        """Puesto que el feed de la cámara está constantemente cambiando e intentar
        buscar un rectángulo continuo (para encontrar el billete), sería
        extremadamente difícil por factores como sombras, posición, los dedos
        que están sosteniendo el billete, etc, la técnica que se utilizará será
        sacar todos los contornos y de ellos extraer sus extremos, para después
        de esos extremos producidos ver cuáles forman rectángulos aproximados"""
         #Conseguir todas las esquinas presentes para después encontrar rectángulos
        get_corners(img)
        if cv2.waitKey(1) & 0xFF == ord('e'): #Terminar feed si se presiona "e"
            break
