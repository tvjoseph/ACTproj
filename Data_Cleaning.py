
import re
from nltk.corpus import stopwords

import ast



def basic_resource_data_cleaning(resource,prop,Delimiter_1,Delimiter_2,Delimiter_4,Res_Grades,Keywords,Regex,Eval_code):
    
    
    column_names = prop.get("Resource_Columns","Column_Names")
    #column_names = column_names.split(prop.get("Cleaning","Delimiter_4"))
    column_names = column_names.split(Delimiter_4)
    for i in column_names:
        resource = resource[~(resource[i].isna())]
       
    #resource["Grade"] = "Grade " + resource[R_Grades].str.replace("|", " Grade ")
    resource["Grade"] = "Grade " + resource[Res_Grades].str.replace(Delimiter_2, " Grade ")
    #resource[Eval_code]=pd.to_numeric(resource[Eval_code])
    
    # Let us now try to clean up the Keywords
    resource['Clean Keywords'] = 0
    for i in range(0,len(resource)):
        
        docsplit = set(resource[Keywords].iloc[i].split(Delimiter_2))
        mylist = []
        for d in docsplit:
            mylist.append(d)
        seclist = ' '.join(mylist)
        newlist = seclist.split(Delimiter_1)
        seclist = ' '.join(newlist)
        #resource['Clean Keywords'].iloc[i] = [re.sub("[^a-zA-Z]", " ", seclist)][0]
        #resource['Clean Keywords'].iloc[i] = [re.sub("[^a-zA-Z]", " ", seclist)][0]
        resource['Clean Keywords'].iloc[i] = [re.sub(Regex," " , seclist)][0]
    
    #resource['Grade_list'] = resource[R_Grades].str.replace('|',',')
    resource['Grade_list'] = resource[Res_Grades].str.replace(Delimiter_2,Delimiter_4)
    
    def remove_Sci(x):
        try:
            return int(ast.literal_eval(x))
        except:
            return x
    resource[Eval_code] = resource[Eval_code].apply(lambda x : remove_Sci(x))            
    return resource
    


def basic_standards_data_cleaning(standards,prop,Delimiter_4,Std_Grades):
    #S_Grades = prop.get("Standard colnames","Std_Grades")
    
    column_names = prop.get("Standard_Columns","Column_Names")
    column_names = column_names.split(Delimiter_4)
    for i in column_names:
        standards = standards[~(standards[i].isna())]
    #standards[S_Grades] = standards[S_Grades].astype(str)
    standards[Std_Grades] = standards[Std_Grades].astype(str)
    return standards

def making_nested_list_resource(resource,prop,Eval_desc,Subject_Node,Subject_Node_Lineage,Regex,Delimiter_1,Delimiter_2,Delimiter_3):

    
    def doc_to_words( raw_data ):
    
        words = raw_data.lower().split()                             
        stops = set(stopwords.words("english"))                  
        meaningful_words = [w for w in words if not w in stops]   
        return( " ".join(meaningful_words ))
        #return( prop.get("Cleaning","Delimiter_1").join(meaningful_words ))

    def doc_to_words2( raw_data,Regex,Delimiter_1 ):
        #letters_only = re.sub("[^a-zA-Z]", " ", raw_data) 
        letters_only = re.sub(Regex," ", raw_data)
        words = letters_only.lower().split(Delimiter_1)                             
        stops = set(stopwords.words("english"))                  
        meaningful_words = [w for w in words if not w in stops]   
        return( " ".join(meaningful_words ))
        #return( prop.get("Cleaning","Delimiter_1").join(meaningful_words ))
        
    def doc_to_words3( raw_data,Regex,Delimiter_2 ):
        #letters_only = re.sub("[^a-zA-Z]", " ", raw_data) 
        letters_only = letters_only = re.sub(Regex," ", raw_data)
        #words = letters_only.lower().split('|')                             
        words = letters_only.lower().split(Delimiter_2)                            
        stops = set(stopwords.words("english"))                  
        meaningful_words = [w for w in words if not w in stops]   
        return( " ".join(meaningful_words ))
        #return( prop.get("Cleaning","Delimiter_1").join(meaningful_words ))
        
    def doc_to_words4( raw_data,Regex,Delimiter_3 ):
        #letters_only = re.sub("[^a-zA-Z]", " ", raw_data) 
        letters_only = letters_only = re.sub(Regex," ", raw_data)
        
        #words = letters_only.lower().split('>')                             
        words = letters_only.lower().split(Delimiter_3)                             
        stops = set(stopwords.words("english"))                  
        meaningful_words = [w for w in words if not w in stops]   
        return( " ".join(meaningful_words ))
        #return( prop.get("Cleaning","Delimiter_1").join(meaningful_words ))
        
        
    def doc_to_words5( raw_data,Delimiter_3 ):
         
        words = raw_data.lower().split(Delimiter_3)                             
        stops = set(stopwords.words("english"))                  
        meaningful_words = [w for w in words if not w in stops]   
        return( " ".join(meaningful_words ))
        #return( prop.get("Cleaning","Delimiter_1").join(meaningful_words ))
        

        
    resdata1 = resource[Eval_desc]
    resdata2 = resource[Subject_Node]
    resdata3 = resource['Clean Keywords']
    resdata4 = resource[Subject_Node_Lineage]
    resdata5 = resource["Grade"]   
   
    clean_train_resdata1 = []
    clean_train_resdata2 = []
    clean_train_resdata3 = []
    clean_train_resdata4 = []
    clean_train_resdata5 = []
    
    for i in range( 0, len(resdata1) ):
        clean_train_resdata1.append( doc_to_words2( resdata1.iloc[i],Regex,Delimiter_1 ) )
        clean_train_resdata2.append( doc_to_words3( resdata2.iloc[i],Regex,Delimiter_2 ) )
        clean_train_resdata3.append( doc_to_words( resdata3.iloc[i] ) )
        clean_train_resdata4.append( doc_to_words4( resdata4.iloc[i],Regex,Delimiter_3 ) )
        clean_train_resdata5.append( doc_to_words( resdata5.iloc[i] ) )
        
    
    combResdata = list(zip(clean_train_resdata1,clean_train_resdata3,clean_train_resdata4, clean_train_resdata5)) # ,clean_train_resdata3, clean_train_resdata2
    print(len(combResdata))

    # Combinig both the strings for resources
    Resdata = []
    for i, _d in enumerate(combResdata):
        Resdata.append(_d[0] +' ' + _d[1]+' ' + _d[2]+' ' + _d[3]) 
    
    return Resdata



def making_nested_list_standards(standards,prop,Regex,Delimiter_1,Std_desc,Std_Lineage,Delimiter_3):
    
    def doc_to_words2( raw_data ):
        letters_only = re.sub(Regex," ", raw_data) 
        words = letters_only.lower().split(Delimiter_1)                             
        stops = set(stopwords.words("english"))                  
        meaningful_words = [w for w in words if not w in stops]   
        return( " ".join(meaningful_words ))
    def doc_to_words5( raw_data,Delimiter_3):
        
        words = raw_data.lower().split(Delimiter_3)                             
        stops = set(stopwords.words("english"))                  
        meaningful_words = [w for w in words if not w in stops]   
        return( " ".join(meaningful_words ))
    stddata1 = standards[Std_desc]
    stddata2 = standards[Std_Lineage]
    clean_train_stddata1 = []
    clean_train_stddata2 = []

    for i in range( 0, len(stddata1) ):
        clean_train_stddata1.append( doc_to_words2( stddata1.iloc[i] ) )
        clean_train_stddata2.append( doc_to_words5( stddata2.iloc[i],Delimiter_3 ) )
    combStddata = list(zip(clean_train_stddata1, clean_train_stddata2))

    # Combinig both the strings for resources
    Stddata = []
    for i, _d in enumerate(combStddata):
        Stddata.append(_d[0] +' ' + _d[1]) 
    return Stddata



 


    















