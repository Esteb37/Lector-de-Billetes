#Proyecto para la materia de Pensamiento Computacional para la Ingeniería
#Esteban Padilla Cerdio
#Última versión - 10/09/2020


import numpy as np
import cv2 #Librería de OpenCV para python



def get_outlines(img): #Función para obtener todos los contornos

    img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Transformar imagen a escala de grises
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(img_grey,(kernel_size, kernel_size),0) #Aplicar desenfoque gausiano para suavizar
    cv2.imshow("frame3",blur_gray)
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold) #Utilizar el algoritmo Canny para resaltar contornos
    cv2.imshow("frame2",edges)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #Extraer todos los contornos continuos
    return contours


def get_corners(img): #Función para extraer esquinas de los contornos
    contours = get_outlines(img) #Sacar contornos
    corners = []
    #El algoritmo buscará los extremos derecho, izquierdo, superior e inferior
    #de cada contorno
    for cnt in contours:
        max_x = 0  #Coordenada en x más a la derecha
        min_x = 10000 #Coordenada en x más a la izquierda
        max_cx = [] #Punto extremo derecho
        min_cx = [] #punto extremo izquierdo
        max_y = 0 #Coordenada en y más a la derecha
        min_y = 10000 #Coordenada en y más a la izquierda
        max_cy = [] #Punto extremo inferior
        min_cy = [] #Punto extremo superior

        for point in cnt:
            x = point[0][0] #Coordenadas
            y = point[0][1]
            if x>max_x: #Si es el más lejano a la derecha
                max_c = [x,y] #Es el nuevo punto extremo derecho
                max_x = x #Su posición en x es la más lejana a la derecha

            #Se repite lo mismo con las otras tres coordenadas
            elif x<min_x:
                min_c = [x,y]
                min_x = x;
            if y>max_y:
                max_cy = [x,y]
                max_y = y
            elif y<min_y:
                min_cy = [x,y]
                min_y = y;

        corners+=[max_cx,min_cx,max_cy,min_cy] #Se agrega a la lista de esquinas

    for point in corners:
        try:
            cv2.circle(img,(point[0],point[1]),3,(0,250,0),2) #Se dibujan las esquinas
        except:
            pass
    cv2.imshow("frame",img)
    return corners



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
        get_corners(img) #Conseguir todas las esquinas presentes para después encontrar rectángulos

        if cv2.waitKey(1) & 0xFF == ord('e'): #Terminar feed si se presiona "e"
            break
