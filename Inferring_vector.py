import numpy as np
from gensim.models.doc2vec import Doc2Vec

def InferVector(log,prop,Doc):
     Vec_df = np.zeros(shape=(len(Doc),50))
     #print(Vec_df)
     fname = (prop.get("Filepaths", "Model_Saving_Path"))
     #print(fname)
     model = Doc2Vec.load(fname)     
     
     for i in range( 0, len(Doc) ):
        #print(i)
        temp = Doc[i]
        temp = str(temp)
        model.random.seed(0)
        Vec_df[i] = model.infer_vector([temp])
     return Vec_df
 
    
