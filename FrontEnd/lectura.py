import os
import face_recognition as fr
import numpy as np
import heapq 
from rtree import index
from timeit import default_timer as timer
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
################################3
################################3
from rtree import index
import face_recognition as fr
from timeit import default_timer as timer
#Version for Web
def encode_for_r(name):
  path = '/content/drive/My Drive/DB2/Project3/Data/Test_1'

  img = fr.load_image_file(path + '/' + name)
  return fr.face_encodings(img)[0]

 
def KNN_rtree(k, to_search, n):
# global start
# R-Tree Lecture from secondary memory
  
  path = "/home/raiko/GG_MULTI_BD2/BackEnd/Project3/Data/"
  rtree_name = path + 'rtreeFile'

  #rtree_name = path + 'rtree_' + str(n)
  #rtree_idx = process_collection(rtree_name, n)
  #print("R-tree generated")
# From image
  #query = encode_for_r(to_search)
  query=to_search
  p = index.Property()
  p.dimension = 128 #D
  p.buffering_capacity = 10 #M
  #p.dat_extension = 'data'
  #p.idx_extension = 'index'
  #idx = index.Index(rtree_name, properties=p)
  #rtreeidx = index.Rtree(rtree_name, properties=p)
  rtreeidx = index.Rtree(rtree_name, properties=p)  
  query_list = list(query)
  for query_i in query:
    query_list.append(query_i)

#  start = timer() 
  
  return rtreeidx.nearest(coordinates=query_list, num_results=k, objects='raw')
