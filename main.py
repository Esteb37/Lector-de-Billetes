#Proyecto para la materia de Pensamiento Computacional para la Ingeniería
#Esteban Padilla Cerdio
#Última versión - 9/10/2020


import numpy as np
import math
import cv2 #Librería de OpenCV para python
from matplotlib import pyplot as plt
import statistics


def get_outlines(img): #Función para obtener todos los contornos

    img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Transformar imagen a escala de grises
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(img_grey,(kernel_size, kernel_size),0) #Aplicar desenfoque gausiano para suavizar
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold) #Utilizar el algoritmo Canny para resaltar contornos
    #cv2.imshow("edges",edges)
    return edges #Regresar una matriz con los contornos en blanco y lo demás en negro

def get_cont(img): #Función para obtener grupos de líneas continuas

    edges = [*zip(*get_outlines(img))] #Obtener contornos e invertir la matriz para poder analizarla de derecha a izquierda

    pixels = [(ix,iy) for ix, row in enumerate(edges) for iy, i in enumerate(row) if i == 255] #Hacer un grupo con todos los puntos pertenecientes a un contorno

    lines = {} #Tabla HASH que permitirá asociar puntos cercanos a un punto de origen
    groups = [] #Lista de líneas agrupadas

    radius = 3 #Distancia máxima para considerar dos puntos como aledaños
    r = range(-radius,radius+1)

    for pixel in pixels: #Por cada pixel perteneciente a un contorno

        try: #Si ese pixel ya fue asociado a un punto de origen
            origin = lines[str(pixel)] #Obtener el punto de origen
            for i in r:
                for j in r: #Atravesar todos los pixeles pertenecientes a su radio
                    try:
                        if (i!=0 or j!=0) and edges[pixel[0]+i][pixel[1]+j]==255: #Si es un pixel diferente y es parte de un contorno
                            p = (pixel[0]+i,pixel[1]+j)
                            try:
                                bin = lines[str(p)] #Probar si ya ha sido asociado
                            except KeyError:
                                index = lines[origin]
                                groups[index].add(p) #Agregar a un grupo de puntos asociados
                                lines[str(p)] = origin #Asociar al punto de origen
                    except IndexError:
                        pass

        except KeyError: #Si el punto no ha sido asociado a nada, o sea que es el primero de su grupo
            groups.append(set([pixel])) #Crear un nuevo grupo con ese punto

            index = len(groups)-1
            lines[str(pixel)] = index #Asociar este punto de origen con el índice de la matriz de grupos

            for i in r:
                for j in r: #Atravesar todos los puntos de su comunidad aledaña
                    try:
                        if (i!=0 or j!=0) and edges[pixel[0]+i][pixel[1]+j]==255: #Si es un pixel diferente y es parte de un contorno
                            p = (pixel[0]+i,pixel[1]+j)
                            groups[index].add(p)  #Agregar al grupo
                            lines[str(p)] = str(pixel) #Asociar con el origen
                    except IndexError:
                        pass
    return groups #Regresar grupos de líneas continuas

def get_lines(img): #Función para obtener líneas rectas
    groups = get_cont(img) #Obtener grupos

    lines = [] #Lista de grupos que sean considerados líneas rectas aproximadas

    for group in groups: #Por cada grupo de puntos
        group = list(group)
        origin = group[0] #Asignar el primer punto como el origen
        slopes = [] #lista de pendientes
        for i,point in enumerate(group):
            if i>0 and (point[0]-origin[0])!=0:
                slope = (point[1]-origin[1])/(point[0]-origin[0]) #Agregar pendiente de punto n con origen
                slopes.append(slope)
        try:
            if statistics.stdev(slopes)<0.5: #si la variación estandar de las pendientes es baja, significa que la pendiente no varía, por lo que es una línea recta
                lines.append(group) #Agregar solo si es línea recta
        except:
            pass
    return lines #Regresar líneas rectas




if __name__ == "__main__":
    capture = cv2.VideoCapture(0,cv2.CAP_DSHOW) #Obtener Webcam


    while True:

        ret, img= capture.read() #Obtener imagen de la webcam

        get_lines(img)
        """Puesto que el feed de la cámara está constantemente cambiando e intentar
        buscar un rectángulo continuo (para encontrar el billete), sería
        extremadamente difícil por factores como sombras, posición, los dedos
        que están sosteniendo el billete, etc, la técnica que se utilizará será
        obtener todos los contornos y de ahí extraer los grupos de puntos que pertenezcan
        a líneas continuas, de las cuales se filtrarán solo las líneas rectas y de ahí
        podremos buscar rectángulos."""
         #Conseguir todas las esquinas presentes para después encontrar rectángulos
        if cv2.waitKey(1) & 0xFF == ord('e'): #Terminar feed si se presiona "e"
            g+=1
