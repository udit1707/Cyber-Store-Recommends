import numpy as np
import pandas as pd
# Using the scikit surprise package establish recommender model

from surprise import Reader, Dataset, SVD
from surprise.model_selection.validation import cross_validate

#read file
def runCollab(userPredict,url):
    data=pd.read_csv(url)
    # print(data.head())
    data['rating']=data['rating'].astype(float)
    df=data.copy()
    df.drop(columns=['id','mongoProd'],inplace=True)
    #df.head()
    df.index=np.arange(0,len(df))
    #print(df.shape)
    #print(df.head())
    
    reader=Reader()
    dataFin=Dataset.load_from_df(df[['userId','productId','rating']],reader)
    #creating an instance of our Model SVD
    svd=SVD()
    # cross_validate(svd,dataFin,measures=['RMSE', 'MAE'], cv=5, verbose=True)
    
    #loading entire dataset
    trainD=dataFin.build_full_trainset()
    svd.fit(trainD) #training our dataset
    # print(data['productId'].unique())
    idss={'productId':data['productId'].unique()}
    titles=pd.DataFrame(idss)
    #drop duplicates

    # titles.drop_duplicates(subset ="productId",keep = 'first', inplace = True) 
    #running our estimation
    titles['estimation']=titles['productId'].apply(lambda x: svd.predict(userPredict, x).est)
    # print(data.head(20))
    titles = titles.sort_values('estimation', ascending=False)
    print(titles.head())
    dic={'id':titles.head(8)['productId'].tolist()}
    print(dic)
    return dic


  

    



    

