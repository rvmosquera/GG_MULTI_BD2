import os
import face_recognition as fr
import numpy as np
import heapq 
from rtree import index

def KNN_Seq(k,query,n,path):  

  dir_list = os.listdir(path)

  conocidas = []
  names_in_order = []
  break_fg = False
  c = 0  
  for file_path in dir_list:
    path_tmp = path + "/" + file_path

    img_list = os.listdir(path_tmp)
    
    for file_name in img_list: 
      
      path_tmp2 = path_tmp + "/" + file_name

      img = fr.load_image_file(path_tmp2)

      unknown_face_encodings = fr.face_encodings(img)
      
      for elem in unknown_face_encodings:

        if c == n: #Process n_images 
          break_fg = True
          break

        names_in_order.append(path_tmp2)
        conocidas.append(elem)        
        c = c + 1
        
      if break_fg:
        break

    if break_fg:
      break    
  


  distances = fr.face_distance(conocidas,query)
  res = [] 

  for i in range(c):
    res.append((distances[i],names_in_order[i]))
  heapq.heapify(res)
  final=heapq.nsmallest(k, res)
    
  return final



################################3
################################3ç
################################3
def knnRtree(k, query, n,datapath):
  
# R-Tree generation
  print('inicio')
  rtree_idx = datapath + 'rtree_' + str(n)
  
  
# From image

  query_list = list(query)
  for query_i in query:
    query_list.append(query_i)
  print('final-------------------------------------------------')
  lista=rtree_idx.nearest(coordinates=query_list, num_results=k)
  print(lista)
  return lista
  