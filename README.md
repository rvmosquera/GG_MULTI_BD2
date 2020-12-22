# GG_MULTI_BD2 Reconociento de Rostro

# Integrant
|  **#** | **Código** | **Apellidos, Nombre** | **% Trabajo** |
| :---: | :---: | :---: | :---: |
|  1 | 201800000 | Vilchez Aguirre Osman Rafael | 33.3% |
|  2 | 201810711 | Mosquera Pumaricra, Raúl Vides | 33.3% |
|  1 | 201810010 | Lazo Pampa, David Alejandro | 33.3% |



## Face-Recognition

Es una librería que está disponible en python, la cuál permite el manejo e identificación de rostros en imágenes. Según la [documentación](https://pypi.org/project/face-recognition/), los vectores característicos que codifican cada carácterítica de la imágen(128 dimensiones) son obtenidos a travéz de IA que ya ha setteado los pesos de las neuronas asociadas por lo que la librería nos entrega una capa alta de abstracción y permite el llamado de funciones de forma directa para obtener y manejar estos vectores.

Esta librería será usada para la obtención de los vectores característicos así como para la función de distancia que permite obtener esta a travéz de la [EUCLIDEAN DIST](https://es.wikipedia.org/wiki/Distancia_euclidiana).

**OBS:** Lamentablemente en el proyecto no consideramos una de las funcionalidades más potentes de Face-Recognition en su totalidad para el análisis, *face_encodings()*, que retorna una lista de vectores característicos asociados a todos los rostros en una imágen.  
Es por ello que en términos prácticos y para la implementación, puesto que por lo general el dataset contiene todos los rostros pero, la imagen original solo contiene el vector del primer rostro. 


## R-Tree
Estructura de datos multidimensional que permite el indexionamiento espacial de vectores característicos. En este caso, python a travéz de la librería [rtree](https://pypi.org/project/Rtree/) provee los métodos necesarios para que indexemos nuestros vectores característicos en el R-Tree.

### Búsqueda KNN e implementación
La búsqueda KNN es aplicada en campos que utilizan espacios vectoriales de alta dimensionalidad para codificar información. Esta es principalmente usada en la búsqueda de los **K** elementos más cercanos codificados. En este sentido, utilizamos este tipo de búsqueda para retornar las ímagenes(identifcadores e.g path) que son las **K** más similares(de menor distancia). Generalmente es implementada con una __priorityqueue__ que va asegurando una estructura óptima para mantener estos elementos cercanos en ***O(K.log K)*** pero atravez de una búsqueda secuencial. No obstante, también se puede utilizar otras estructuras multidimensionales para este trabajo, como el __R-Tree__ , estructura que almacena e indexa por Rango de distancias a los vectores característicos de un objeto.

Una parte del proyecto es comparar estas dos estructuras a nivel temporal, entre el R-tree armado y con la búsqueda secuencial. 

#### KNN-RTREE
El costo del algoritmo es de:
***O(logM(N) + k.d)***, donde N es la cantidad de elementos en el Rtree (en este caso tuplas de las características de las imágenes) y un d, el cual corresponde el tiempo el vecino más cerano y K la cantidad de vecinos.
```
# Part of the code of KNN-Rtree
# Extract vector characteristic from image
  query = encode_for_r(to_search)

  p = index.Property()
  p.dimension = 128 #D
  p.buffering_capacity = 10 #M
  #idx = index.Index(rtree_name, properties=p)
  rtreeidx = index.Rtree(rtree_name, properties=p)  
  
  query_list = list(query)
  for query_i in query:
    query_list.append(query_i)

  start = timer() 
  return rtreeidx.nearest(coordinates=query_list, num_results=k, objects='raw')
```

#### KNN-Sequential
En esta implementación se hace uso de un heap para mantener ordenada crecientemente las distancias, las distancias se proveen por face_recognition con face_distance, el cual devuelve un arreglo con las distancias a cada imagen del dataset.
```
def encode(name):
  img = fr.load_image_file(path + '/' + name)
  return fr.face_encodings(img)[0]

def KNN_Seq(k,to_search,n):      
  query = encode(to_search)
  cantidad = 0
  conocidas = []
  names_in_order = []
  c = 0
  for file_name in pics_list:
    cantidad = cantidad +1
    print("Processing: ", file_name)
    img_fname = path + '/' + file_name
    img = fr.load_image_file(img_fname)
    aux_c = fr.face_encodings(img)
    for aux in aux_c:
      names_in_order.append(file_name)
      conocidas.append(aux)
    c = c+1
    if c==n:
      break


  distances = fr.face_distance(conocidas,query)
  res = [] 
  for i in range(cantidad):
    res.append((distances[i],names_in_order[i]))
  
  heapq.heapify(res) 

  return heapq.nsmallest(k, res)
 

print(KNN_Seq(8,"foto1.jpg",100))
```


El costo del algoritmo es de:

***O(t.n.l+ d.n.l + n.k.log(k))***, t = tiempo de la codificación d = tiempo de la obtención de las distancias k = cantidad de imágenes a retornar l = cantidad de caras en la imagen.

#### Comparativas
La siguiente tabla muestra los tiempos para realizar las búsquedas por similitud, anteriormente descrita.
*Consideraciones:* 
- Para todas las pruebas se tomaron los tiempos con K = 8. 
- La plataforma y el hardware para la codificación de imágenes han sido dadas por [GoogleCoolab](https://colab.research.google.com/) para facilitar el trabajo grupal y por sus buenas specs de hardware. Es importante mencionar que debido a las limitaciones del GPU, la plataforma indica que la codificación sea dada en el GPU local(NVIDIA GTX 1660ti).  
- Los tiempos fueron tomados después de hacer la indexación(en el R-tree) y después de realizar y calcular las distancias en la búsqueda secuencial.


*Resultados obtenidos*
| Tamaño(N) | KNN - Rtree  |   KNN-Seq   |
|-----------|:------------:|:-----------:|
|    100    |  0.009794711 | 0.000825741 |
|    200    |  0.011172232 | 0.001032722 |
|    400    |  0.013048095 | 0.001414824 |
|    800    |  0.015653412 | 0.001876513 |
|    1600   |  0.017586873 | 0.003131072 |
|    3200   |  0.024952998 | 0.005130535 |
|    6400   |  0.033386171 | 0.009742670 |
|   12800   |  0.056623063 | 0.019123669 |

 ![Comparativa](https://github.com/rvmosquera/GG_MULTI_BD2/blob/main/img.png) 

##### Análisis de los resultados
Teóricamente, estimamos que las búsquedas en una estructura de árbol especializada en la indexación de acuerdo a las distancias debe ser más rápida que las realizas en una de búsqueda secuencial. Sin embargo, bajo el criterio de la [maldición de la alta dimensionalidad](https://bib.dbvis.de/uploadedFiles/190.pdf) que se basa en la naturaleza de la estructura del R-tree, la superposición de los cuadros delimitadores en el directorio, que aumenta con la dimensión creciente. 
Es por ello que ya teníamos expectativas de la poca eficiencia al indexar vectores característico de alta dimensionalidad. Pese a ello, esto es notable solo en el valor base de la búsqueda de los 100 primeros, en la cuál supera en orden al de la búsqueda secuencial, no obstante, a medida que n va creciendo, se nota la diferencia entre el **crecimiento lineal** del secuencial y el **crecimiento logarítmico** del *R-tree* que en la entrada de 12800 ya no hay una diferencia de orden.


***Mitigación:*** 
- La mitigación no fue mapeada en la implementación, pero una solución a esta puede ser reducir la dimensionalidad buscando características menos predominantes en la diferenciación de las imágenes y eliminarlas.
- Otra solución, puede ser la indexación en un árbol [X-tree](https://bib.dbvis.de/uploadedFiles/190.pdf) que usa la superposición-minimización de división y supernodos para mantener la estructura lo más jerárquico posible y, al mismo tiempo, evitar divisiones en el nodo que darían como resultado una gran superposición.


### Búsqueda por radio e implementación 
De forma análoga a la implementación kNN pero con menor complejidad, codificamos, hallamos las distancias, y si estas son menores al valor de r, serán retornadas.
```
import face_recognition as fr
import numpy as np
import os

path = '/content/drive/My Drive/DB2/Project3/Data/Test_1'
pics_list = os.listdir(path)

def encode(name):
  img = fr.load_image_file(path + '/' + name)
  return fr.face_encodings(img)[0]



def search_r(r,to_search):  
  query = encode(to_search)
  cantidad = 0
  conocidas = []
  names_in_order = []
  for file_name in pics_list:
    cantidad = cantidad +1
    print("Processing: ", file_name)
    img_fname = path + '/' + file_name
    img = fr.load_image_file(img_fname)
    aux = fr.face_encodings(img)[0]
    names_in_order.append(file_name)
    conocidas.append(aux)

  distances = fr.face_distance(conocidas,query)
  
  res = []
  for i in range(cantidad):
    if distances[i]<=r:
      res.append((distances[i],names_in_order[i]))

  return res

name_img = "foto1.jpg"
print(search_r(1,name_img))

```
***O(t.l.n + d.l.n + n)***, t = tiempo de la codificación d = tiempo de la obtención de las distancias l = cantidad de caras en la imagen.







