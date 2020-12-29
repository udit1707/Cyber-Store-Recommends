import numpy as np
import pandas as pd
import pymysql
import datetime
from sqlalchemy import create_engine

cnx = create_engine('mysql+pymysql://{Username}:{Password}@{Hostname}/{Database}')    
products = pd.read_sql_query("SELECT id,name,image,mongoId,mean_rating,count_ratings,updatedAt FROM products WHERE count_ratings>=1", cnx) #read the entire table

products['updatedAt']=products['updatedAt'].dt.strftime('%Y-%m-%d')
# print(products.info())
C = products['mean_rating'].mean()
    #print(C)
m = products['count_ratings'].quantile(0.60)
    #print(m)
q_prod = products.copy().loc[products['count_ratings'] >= m]

def weighted_rating(x, m=m, C=C):
    v = x['count_ratings']
    R = x['count_ratings']
    return (v/(v+m) * R) + (m/(m+v) * C)
    
    
q_prod['score'] = q_prod.apply(weighted_rating, axis=1)
q_prod = q_prod.sort_values('score', ascending=False)

def recommenFetch():
    dic={'image':q_prod.head(8)['image'].tolist(),'id':q_prod.head(8)['mongoId'].tolist(),'name':q_prod.head(8)['name'].tolist(),'mean':q_prod.head(8)['mean_rating'].tolist(),'count':q_prod.head(8)['count_ratings'].tolist(),'update':q_prod.head(8)['updatedAt'].tolist()}
    print(dic)
    return dic

