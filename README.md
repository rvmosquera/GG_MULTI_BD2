# GG_MULTI_BD2




## Face-Recognition

## R-Tree


### Búsqueda KNN
La búsqueda KNN es aplicada en campos que utilizan espacios vectoriales de alta dimensionalidad para codificar información. Esta es principalmente usada en la búsqueda de los **K** elementos más cercanos codificados. En este sentido, utilizamos este tipo de búsqueda para retornar las ímagenes(identifcadores e.g path) que son las **K** más similares(de menor distancia). Generalmente es implementada con una __priorityqueue__ que va asegurando una estructura óptima para mantener estos elementos cercanos en ***O(K.log K)*** pero atravez de una búsqueda secuencial. No obstante, también se puede utilizar otras estructuras multidimensionales para este trabajo, como el __R-Tree__ , estructura que almacena e indexa por Rango de distancias a los vectores característicos de un objeto.

Una parte del proyecto es comparar estas dos estructuras, entre el R-tree armado y con la búsqueda secuencial. 

#### KNN-RTREE

#### KNN-Sequential
 

#### Comparativas
La siguiente tabla muestra los tiempos para realizar las búsquedas por similitud, anteriormente descrita.
*Consideraciones:* 
- Para todas las pruebas se tomaron los tiempos con K = 8. 
- La plataforma y el hardware para la codificación de imágenes han sido dadas por [GoogleCoolab](https://colab.research.google.com/) para facilitar el trabajo grupal y por sus buenas specs de hardware. Es importante mencionar que debido a las limitaciones del GPU, la plataforma indica que la codificación sea dada en el GPU local(NVIDIA GTX 1660ti).  

*Resultados obtenidos*
| Tamaño(N) |    KNN - Rtree     |       KNN-Seq      |
|-----------|:------------------:|:------------------:|
|    100    |         110        |       4814800      |
|    200    | 1.5540294647216797 | 1.6676933765411377 |
|    400    | 1.6249639987945557 | 1.6992597579956055 |
|    800    | 1.5151827335357666 | 1.6198115348815918 |
|    1600   |                    |                    |
|    3200   |                    |                    |
|    6400   |                    |                    |
|   12800   |                    |                    |
