
import numpy as np
import operator
import itertools

def normalise(A):
    lengths = (A**2).sum(axis=1, keepdims=True)**.5
    return A/lengths


def Recommendation(i,log,prop,resourceDf,standDf,std1,contents_F,guid,db):
    	
    
        d1 = resourceDf[std1]        
        d2 = standDf[[i]] 
        
        d2 = normalise(d2)  
        d1 = normalise(d1)
        
        
        final = np.dot(d2,d1.T)        
        
        Filter_score_list = final[0].tolist()
        result_filtered = {}
        result_filtered["GUID"] = guid

        Evaluation = {}
        for k in range(0,len(contents_F)):
            Evaluation[str(contents_F.iloc[k])] = Filter_score_list[k]
        sorted_Evaluation = dict( sorted(Evaluation.items(), key=operator.itemgetter(1),reverse=True))
        sorted_Evaluation = dict(itertools.islice(sorted_Evaluation.items(), 100))
        result_filtered.update(sorted_Evaluation)
        db.Trial1.insert_one(result_filtered)