#Proyecto para la materia de Pensamiento Computacional para la Ingeniería
#Esteban Padilla Cerdio
#Última versión - 22/10/2020


import numpy as np
import math
import cv2 #Librería de OpenCV para python
from matplotlib import pyplot as plt
import statistics

global ax

def get_outlines(img): #Función para obtener todos los contornos
    global ax
    img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Transformar imagen a escala de grises
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(img_grey,(kernel_size, kernel_size),0) #Aplicar desenfoque gausiano para suavizar
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold) #Utilizar el algoritmo Canny para resaltar contornos
    ax[0, 1].imshow(cv2.cvtColor(edges, cv2.COLOR_BGR2RGB))
    ax[0, 1].set_title("Contornos") #Publicar la imagen de los contornos
    ax[0, 1].axis('off')
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
        group.sort(key=lambda x: x[0]) #Se ordena el grupo de izquierda a derecha
        dict = {} #Aquí guardaremos los grupos divididos por ángulos

        for i,p in enumerate(group): #Por cada punto en el grupo
            try:
                a = round(math.degrees(math.atan2(group[i+20][1]-p[1],group[i+20][0]-p[0]))/10) #Se obtiene el ángulo entre el punto actual y 20 puntos adelante y se redondea a un dígito para agrupar todos los ángulos similares
                if(abs(a)==9): #Si el ángulo es 90 grados, tiende a cambiar entre positivo y negativo, arruinando el algoritmo, por lo que en ese caso específico se toma su absoluto
                    a = 9
                dict.setdefault(a,[]).append(np.array(p)); #Se agrega el punto al grupo de puntos en el diccionario correspondiente al ángulo que formó

            except IndexError: #Se termina cuando ya no haya puntos para comparar
                break

        for k in dict.keys(): #Se crea una lista de las líneas formadas por puntos en un mismo ángulo
            if(len(dict[k])>50): #Se filtran las líneas menores a 50 puntos
                lines.append((k,dict[k])) #Se agrega una pareja del ángulo y los puntos sobre líneas formadas por dicho ángulo

    return lines #Regresar líneas rectas

def join_lines(img): #Función para unir líneas cercanas que pertenezcan a la misma línea original
    lines = get_lines(img)
    i = 0
    while True: #Se atraviezan todos los pares posibles con un while en lugar de un for porque se estará actualizando constantemente el arreglo de líneas
        j = i
        if(i>=len(lines)):
            break
        while True:
            if(j>=len(lines) or i>=len(lines)): #Detener el ciclo cuando se exceda el índice del arreglo actualizado
                break
            line = lines[i]
            line2=lines[j]

            if i!=j and abs(line[0]-line2[0])<=2:   #Si el ángulo entre ambas líneas es cercano

                p1 = line[1][-1] #El final de la primera línea
                p2 = line[1][0] #El principio de la primera línea
                p3 = line2[1][0] #El principio de la segunda línea
                try:
                    m = (p1[1]-p2[1])/(p1[0]-p2[0]) #Se obtiene la pendiente de las líneas
                except:
                    m = (p1[1]-p2[1])/0.1 #En caso de que exista una división entre zero, se sustituye por un valor pequeño

                b1 = p2[1]-m*p2[0] #Se obtiene la b de la función y = mx+b
                b2 = p3[1]-m*p3[0]

                d = abs(abs(b2 - b1) / ((m * m) - 1)); #Se obtiene la distancia entre ambas líneas

                if(d<5): #Si la distancia es pequeña, significa que pueden ser la misma línea
                    lines[i] = ((line[0]+line2[0])/2,line[1]+line2[1]) #Se le suman los puntos de la segunda línea a la primera
                    lines.pop(j) #Se elimina la segunda línea para que ya no sea considerada por otras líneas
                else:
                    j+=1;
            else:
                j+=1
        i+=1
    return lines


def get_rects(img): #Función para obtener posibles rectángulos
    global ax
    lines = join_lines(img)
    rects = []
    i = j = 0;
    copy = img.copy()
    for i,line in enumerate(lines): #Se atraviezan todas las parejas posibles
        for j in range(i,len(lines)):
            line2 = lines[j]
            if(abs(line[0]-line2[0])<=2): #Si las líneas son paralelas (su ángulo es similar)
                line2 = lines[j]
                p1 = line[1][0] #Inicio de la primera línea
                p2 = line[1][-1] #Final de la primera línea
                p3 = line2[1][-1] #Inicio de la segunda línea
                p4 = line2[1][0] #Final de la segunda línea

                if(np.linalg.norm(p1-p2)>200 and np.linalg.norm(p3-p4)>200): #Si la longitud de ambas líneas es mayor a 200 unidades
                    h1 = np.linalg.norm(p1-p4) #Diagonal 1
                    h2 = np.linalg.norm(p2-p3) #Diagonal 2
                    if(h1>100 and h1<500 and h2>100 and h2<500): #Si las diagonales del rectángulo están entre 100 y 500 unidades
                        rects.append((tuple(p1),tuple(p2),tuple(p3),tuple(p4))) #Se agrega el rectángulo a la lista de posibles
                        cv2.line(copy,tuple(p1),tuple(p2),(0,255,0),3)
                        cv2.line(copy,tuple(p2),tuple(p3),(0,255,0),3)   #Se dibuja el rectángulo
                        cv2.line(copy,tuple(p3),tuple(p4),(0,255,0),3)
                        cv2.line(copy,tuple(p4),tuple(p1),(0,255,0),3)

    ax[1, 0].imshow(cv2.cvtColor(copy, cv2.COLOR_BGR2RGB))
    ax[1, 0].set_title("Rectángulos") #Se publica la imagen con los rectángulos posibles
    ax[1, 0].axis('off')
    return rects

def get_colors(img): #Función para obtener los colores promedio de cada rectángulo posible

    rects = get_rects(img)
    height, width, _ = np.shape(img)

    l = 0
    colors = []
    for r in rects:
        canvas = img.copy() #Se crea un respaldo de la imagen para no editarla
        r = np.array([[r]], dtype=np.int32 ) #Se trabsfirna ek rectángulo en un arreglo de puntos
        stencil  = np.zeros(img.shape[:-1]).astype(np.uint8) #Se crea una imagen negra del tamaño de la imagen original
        cv2.fillPoly( stencil, r, 255 ) #Se rellena en esa imagen negra de blanco el área entre los cuatro puntos del rectángulo
        sel = stencil != 255 #Se selecciona todo lo que no sea blanco
        canvas[sel] = 0 #Se aplica la máscara para ocultar todo lo que no es el rectángulo
        size = len(canvas[np.any(canvas != [0, 0, 0],axis = -1)]) #Tamaño del interior del rectángulo
        if size>50000: #Si el área del rectángulo es mayor a 50000 unidades
            avg_color_per_row = np.average(canvas[np.any(canvas != [0, 0, 0],axis = -1)], axis=0) #Se obtiene el color promedio de cada línea excluyendo al negro
            avg_colors = np.average(avg_color_per_row, axis=0) #Se obtiene el color promedio de todas las líneas

            if(not math.isnan(avg_colors)):
                colors.append((avg_colors,canvas)) #Se agrega a los colores posibles, junto con su rectángulo original

    return colors

def get_bills(img): #Función para definir la probabilidad del valor del billete según su color

    colors = get_colors(img)
    maxprob  = [0,[],""] #Arreglo donde se guardará la máxima probabilidad, junto con su rectángulo y su valor

    for c in colors:
        color = c[0]
        distances = 1/abs(color-158)**2+1/abs(color-150)**2+1/abs(color-143)**2 #Se obtiene el error total del color actual con los valores aproximados de cada billete
        prob20 = (1/abs(color-158)**2/distances*100,"20") #Probabilidad de que sea de 20 pesos
        prob50 = (1/abs(color-150)**2/distances*100,"50") #Probabilidad de que sea de 50 pesos
        prob200 = (1/abs(color-143)**2/distances*100,"200") #Probabilidad de que sea de 200 pesos

        m = max([prob20,prob50,prob200],key=lambda x:x[0])  #Se obtiene la mayor probabilidad de las tres

        if(m[0]>maxprob[0]): #Se asigna la probabilidad actual al máximo solo si es mayor
            maxprob = [m[0],c[1],m[1]]

    return maxprob

if __name__ == "__main__":
    global ax

    print(" ---------------------------------------------------------------------------------------\n\nBienvenido al Prototipo para el Detector de Billetes. El propósito de este proyecto es fungir como una muestra de una posible aplicación capaz de detectar los valores de billetes por medio de la cámara, y comunicárselos a personas invidentes por medio de otros sentidos como el oído. Por el momento, surgen algunas limitaciones con calidades de fotografías distintas, por lo que se han preparado diferentes imágenes cuya efectividad no ha sido disminuida por factores como luz o resolución.\n\nAntes de comenzar, asegúrate de haber incluído las imágenes precargadas en la misma carpeta que este código \n\n --------------------------------------------------------------------------------------- \n")
    imagenes = ["50.png","502.png","20.png","202.png","200.png","2002.png","203.png"]
    while True:
        print("\nSeleccione un número del 1 al 7 para analizar una de las fotografías precargadas. Seleccione -1 para terminar: \n")
        i = int(input())
        if i==-1:
            break
        elif(i>=1 and i<=len(imagenes)):
            src = imagenes[i-1]
        else:
            print("Por favor seleccione un número válido\n")
            continue

        img = cv2.imread(src,1) #se obtiene la imagen
        fig, ax = plt.subplots(2, 2,figsize=(12,8)) #se preparan las gráficas para las imágenes
        prob = get_bills(img) #Se obtiene la probabilidad más alta
        ax[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) #Se publica la imagen original
        ax[0, 0].set_title("Original")
        ax[0, 0].axis('off')
        ax[1, 1].imshow(cv2.cvtColor(prob[1], cv2.COLOR_BGR2RGB)) #Se publica la imagen con máscara
        ax[1, 1].set_title("Masked")
        ax[1, 1].axis('off')

        ax[1, 1].text(0.5,-0.1, "Valor: $"+str(prob[2])+" - Probabilidad "+str(round(prob[0]))+"%", size=20, ha="center",
                 transform=ax[1, 1].transAxes) #Se publica el resultado
        fig.tight_layout()

        plt.show()
    print("Muchas gracias por probar este prototipo. Vuelva pronto.")
