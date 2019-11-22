#Importing modules
from .Loading_Data import data_loading
from .Data_Cleaning import basic_resource_data_cleaning,basic_standards_data_cleaning,making_nested_list_resource,making_nested_list_standards
from .Recommendation_Final import Recommendation
from gensim.models.doc2vec import Doc2Vec
from pymongo import MongoClient
from .Inferring_vector import InferVector



def processResourceAlignment(prop,log, method):
     #------------------------------------------------------------------------------------------------------------------
    if method=='train':
        log.info("---------Into the driver program---------------")
                
        Delimiter_1 = prop.get("Cleaning","Delimiter_1")
        Delimiter_2 = prop.get("Cleaning","Delimiter_2")
        Delimiter_3 = prop.get("Cleaning","Delimiter_3")
        Delimiter_4 = prop.get("Cleaning","Delimiter_4")
        Res_Grades = prop.get("Resource colnames","Res_Grades")        
        Keywords = prop.get("Resource colnames","Keywords")
        Regex = prop.get("Regex","Rgex_1")
        Std_Grades = prop.get("Standard colnames","Std_Grades")
        Eval_desc = prop.get("Resource colnames","Eval_desc")
        Subject_Node= prop.get("Resource colnames","Subject_Node")        
        Subject_Node_Lineage = prop.get("Resource colnames","Subject_Node_Lineage")        
        Std_desc = prop.get("Standard colnames","Std_desc")
        Std_Lineage = prop.get("Standard colnames","Std_Lineage")
        Eval_code = prop.get("Resource colnames","Eval_Code")
        GUID = prop.get("Standard colnames","GUID")
                
        client = MongoClient(port=27017)
        db=client.Demo

        resources,standards = data_loading(prop,log)
        resources = resources.iloc[0:10]
        resources = basic_resource_data_cleaning(resources,prop,Delimiter_1,Delimiter_2,Delimiter_4,Res_Grades,Keywords,Regex,Eval_code)                
        resources = resources.reset_index(drop=True)
        
        standards = basic_standards_data_cleaning(standards,prop,Delimiter_4,Std_Grades)
       
        combinedResource = making_nested_list_resource(resources,prop,Eval_desc,Subject_Node,Subject_Node_Lineage,Regex,Delimiter_1,Delimiter_2,Delimiter_3)        
        #print(combinedResource[0])
        combinedStandards = making_nested_list_standards(standards,prop,Regex,Delimiter_1,Std_desc,Std_Lineage,Delimiter_3)
        #print(combinedStandards[0])
        
        resourceDf = InferVector(log,prop,combinedResource)
        print("Resource vectors")
        print(resourceDf[0:2])
        standDf = InferVector(log,prop,combinedStandards)
        print("Standard vectors")
        print(standDf[0:2])
        
        for i in range(len(standards)):
            print(i)
            Standard_list = standards.iloc[i][Std_Grades]
            Standard_list = list(Standard_list.split(" "))
            Standard_list = Standard_list[0].split(Delimiter_4)
            Filtered_Res = resources[resources["Grade_list"].str.split(Delimiter_4,expand=True).isin(Standard_list).any(1)]   
            std1 = Filtered_Res.index                    
            contents_F = resources.iloc[std1][Eval_code]
            guid = str(standards.loc[i][GUID])
            
            Recommendation(i,log,prop,resourceDf,standDf,std1,contents_F,guid,db)   
                
        """
        
        log.info("Printing combined res and std infor")
        log.info(str(len(combinedResource)))
        log.info(str(len(combinedStandards)))
        log.info(combinedResource[0])
        log.info(combinedStandards[0])
                    
        #Creating Corpus
        corpus = combinedResource+combinedStandards
        #end_model_cleaning = datetime.datetime.now()
        #Time_for_model = end_model_cleaning - start_model_cleaning
        #log.info("Time taken for cleaning data for model: " + str(Time_for_model.total_seconds()))
        
#        print("Printing the type of corpus")
#        print(type(corpus))
        #print(getsizeof(corpus))
        #start_tags=datetime.datetime.now()
        tags = creatingTags(corpus)
        #end_tags=datetime.datetime.now()
        #tag_time = end_tags - start_tags
        #log.info("Time taken for creating tags: " + str(tag_time.total_seconds()))
        start_time_model = datetime.datetime.now()
        
        
        createGensimModels(tags,prop)
        End_time_model = datetime.datetime.now()
       
        execution_response_time_model = End_time_model - start_time_model
        log.info("Execution time for model building is" + str(execution_response_time_model.total_seconds()))
        
        #start_vector =datetime.datetime.now()
#        fname = (prop.get("Filepaths", "Model_Saving_Path"))
#        model = Doc2Vec.load(fname)       
                             
        """
    elif method=='IncRes':
        
        log.info("---------Into the driver program---------------")
        resources,standards = data_loading(prop,log)
        
                
        log.info("Before Cleaning Resources------"+str(len(resources)))
        log.info("Before Cleaning Standards------"+str(len(standards)))
        
        
        #Saving the arguments as objectsS
        Delimiter_1 = prop.get("Cleaning","Delimiter_1")
        Delimiter_2 = prop.get("Cleaning","Delimiter_2")
        Delimiter_3 = prop.get("Cleaning","Delimiter_3")
        Delimiter_4 = prop.get("Cleaning","Delimiter_4")
        Res_Grades = prop.get("Resource colnames","Res_Grades")
        #Res_Grade_list = prop.get("Resource colnames","Res_Grade_list")
        Keywords = prop.get("Resource colnames","Keywords")
        Regex = prop.get("Regex","Rgex_1")
        Std_Grades = prop.get("Standard colnames","Std_Grades")
        Eval_desc = prop.get("Resource colnames","Eval_desc")
        Subject_Node= prop.get("Resource colnames","Subject_Node")
        #Clean_Keywords = prop.get("Resource colnames","Clean_Keywords")
        Subject_Node_Lineage = prop.get("Resource colnames","Subject_Node_Lineage")
        #ResGrade_M = prop.get("Resource colnames","ResGrade_M")
        Std_desc = prop.get("Standard colnames","Std_desc")
        Std_Lineage = prop.get("Standard colnames","Std_Lineage")
        Eval_code = prop.get("Resource colnames","Eval_Code")
        GUID = prop.get("Standard colnames","GUID")
        
        username = prop.get("MongoDB Credentials", "username")
        password = prop.get("MongoDB Credentials", "password")
        ip = prop.get("MongoDB Credentials", "ip")
        port = prop.get("MongoDB Credentials", "port")
        database_name = prop.get("MongoDB Credentials", "database_name")
        collection_name = prop.get("MongoDB Credentials", "collection")
        url = "mongodb://"+username+":"+password+"@"+ip+":"+port+"/"+database_name 
        print(url)
        client = MongoClient(url)
        db = client[database_name]
        collection = db[collection_name]
        
        file=prop.get("Filepaths","TextFile_Path") 
       
        resources = basic_resource_data_cleaning(resources,prop,Delimiter_1,Delimiter_2,Delimiter_4,Res_Grades,Keywords,Regex)
        standards = basic_standards_data_cleaning(standards,prop,Delimiter_4,Std_Grades)
        combinedStandards = making_nested_list_standards(standards,prop,Regex,Delimiter_1,Std_desc,Std_Lineage,Delimiter_3)
                       
        log.info("After Cleaning Standards-------"+str(len(standards)))
        
#        print("Standard's type")
#        print(type(standards))
        resources_length = len(resources) #To get resource length from model
        standards_length = len(standards)
        print(resources_length)
        print(standards_length)
        
        fname = (prop.get("Filepaths", "Model_Saving_Path"))
        model = Doc2Vec.load(fname)
        
        # Making the vectors of the documents    
        vec_df = model.docvecs.vectors_docs
        print(vec_df.shape)
        #For New Resources
        New_resources_data = Load_newData_Res(prop,log)
        print("New_res_info")
        print(len(New_resources_data))
        print(New_resources_data.columns)
        
        New_resources_data = basic_resource_data_cleaning(New_resources_data,prop,Delimiter_1,Delimiter_2,Delimiter_4,Res_Grades,Keywords,Regex)
        New_resources_data = New_resources_data.reset_index(drop=True)
        
       
        New_res_nested_list = making_nested_list_resource(New_resources_data,prop,Eval_desc,Subject_Node,Subject_Node_Lineage,Regex,Delimiter_1,Delimiter_2,Delimiter_3)
        print("New resources imported and cleaned")
        print(len(New_res_nested_list))
        
        with open(file, 'w') as filetowrite:
            filetowrite.write('Data cleaning is completed')
            
        New_Res_vector = InferVector_Res(prop,log,New_res_nested_list)
        resourceDf = New_Res_vector
        
        #standDf = vec_df[resources_length:,:]
        standDf = InferVector_Res(prop,log,combinedStandards)
        
        
        with open(file, 'w') as filetowrite:
            filetowrite.write('Vectors are inferred from the model for incremental resources')

        
        print("Printing the type of Res vec")
        print(type(New_Res_vector))
        for i in range(len(standards)):
            print(i)
            Standard_list = standards.iloc[i][Std_Grades]
            Standard_list = list(Standard_list.split(" "))
            Standard_list = Standard_list[0].split(Delimiter_4)
            Filtered_Res = New_resources_data[New_resources_data["Grade_list"].str.split(Delimiter_4,expand=True).isin(Standard_list).any(1)]   
            std1 = Filtered_Res.index                    
            contents_F = New_resources_data.iloc[std1][Eval_code]
            guid = str(standards.loc[i][GUID])
            
            Incremental_Resource_Recommenndation(i,log,prop,resourceDf,standDf,std1,contents_F,guid,db,collection)
        with open(file, 'w') as filetowrite:
             filetowrite.write('Recommendations for standards are updated')
             
        
    elif method=='IncStd':        
         
        log.info("---------Into the driver program---------------")
        resources,standards = data_loading(prop,log)
        print(resources.columns)
        
        
        log.info("Before Cleaning Resources------"+str(len(resources)))
        log.info("Before Cleaning Standards------"+str(len(standards)))
        Delimiter_1 = prop.get("Cleaning","Delimiter_1")
        Delimiter_2 = prop.get("Cleaning","Delimiter_2")
        Delimiter_3 = prop.get("Cleaning","Delimiter_3")
        Delimiter_4 = prop.get("Cleaning","Delimiter_4")
        Res_Grades = prop.get("Resource colnames","Res_Grades")
        #Res_Grade_list = prop.get("Resource colnames","Res_Grade_list")
        Keywords = prop.get("Resource colnames","Keywords")
        Regex = prop.get("Regex","Rgex_1")
        Std_Grades = prop.get("Standard colnames","Std_Grades")
        Eval_desc = prop.get("Resource colnames","Eval_desc")
        Subject_Node= prop.get("Resource colnames","Subject_Node")
        #Clean_Keywords = prop.get("Resource colnames","Clean_Keywords")
        Subject_Node_Lineage = prop.get("Resource colnames","Subject_Node_Lineage")
        #ResGrade_M = prop.get("Resource colnames","ResGrade_M")
        Std_desc = prop.get("Standard colnames","Std_desc")
        Std_Lineage = prop.get("Standard colnames","Std_Lineage")
        Eval_code = prop.get("Resource colnames","Eval_Code")
        GUID = prop.get("Standard colnames","GUID")
        
#        username = prop.get("MongoDB Credentials", "username")
#        password = prop.get("MongoDB Credentials", "password")
#        ip = prop.get("MongoDB Credentials", "ip")
#        port = prop.get("MongoDB Credentials", "port")
#        database_name = prop.get("MongoDB Credentials", "database_name")
#        collection_name = prop.get("MongoDB Credentials", "collection")
#        url = "mongodb://"+username+":"+password+"@"+ip+":"+port+"/"+database_name 
#        print(url)
#        client = MongoClient(url)
#        db = client[database_name]
#        collection = db[collection_name]
        client = MongoClient(port=27017)
        db=client.knovation

        #file=prop.get("Filepaths","TextFile_Path") 
        
        resources = basic_resource_data_cleaning(resources,prop,Delimiter_1,Delimiter_2,Delimiter_4,Res_Grades,Keywords,Regex,Eval_code)
        resources = resources.reset_index(drop=True)
        log.info("After Cleaning Resources-------"+str(len(resources)))
        
        combinedResource = making_nested_list_resource(resources,prop,Eval_desc,Subject_Node,Subject_Node_Lineage,Regex,Delimiter_1,Delimiter_2,Delimiter_3)
        resourceDf = InferVector_Res(prop,log,combinedResource)
    
        #print(resources.info())
        #print(len(resources))
        
        
        
#        resources_length = len(resources)
        
#        print(len(resources))
        
#        fname = (prop.get("Filepaths", "Model_Saving_Path"))
#        model = Doc2Vec.load(fname)
#        
#        # Making the vectors of the documents    
#        vec_df = model.docvecs.vectors_docs
#        
#        # Let us now seperate the resources matrix and also the standards matrix
#        resourceDf = vec_df[:resources_length,:]
#        print("Printing the shape of resDf")
#        print(resourceDf.shape)
        
        #New_standard_data = Load_newData_Std(prop,log)
        New_standard_data = basic_standards_data_cleaning(standards,prop,Delimiter_4,Std_Grades)
        New_std_nested_list = making_nested_list_standards(New_standard_data,prop,Regex,Delimiter_1,Std_desc,Std_Lineage,Delimiter_3)
        print(len(New_std_nested_list))
        
        
#        with open(file, 'w') as filetowrite:
#            filetowrite.write('Data cleaning is completed')
#        
        standDf = InferVector_Std(prop,log,New_std_nested_list)
        print(standDf)
        
        print(standDf.shape)
#        with open(file, 'w') as filetowrite:
#            filetowrite.write('Vectors are inferred from the model for incremental standards')
        for i in range(len(New_standard_data)):
            print(i)
            Standard_list = New_standard_data.iloc[i][Std_Grades]
            Standard_list = list(Standard_list.split(" "))
            Standard_list = Standard_list[0].split(Delimiter_4)
            Filtered_Res = resources[resources["Grade_list"].str.split(Delimiter_4,expand=True).isin(Standard_list).any(1)]   
            std1 = Filtered_Res.index                    
            contents_F = resources.iloc[std1][Eval_code]
            guid = str(standards.loc[i][GUID])
            
            Incremental_Standards_Recommendation(i,log,prop,resourceDf,standDf,std1,contents_F,guid,db)
        
#        with open(file, 'w') as filetowrite:
#            filetowrite.write('Recommendations for new standards are obtained')
#        
           
        
        
       
        