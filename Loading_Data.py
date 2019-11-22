

"""
Data Cleaning:
    
    This script will allow users to load data from the server to create pandas dataframes out of it. The created dataframes will be sent back to the 
    driver program for further processes.
    
    Used Libraries:
        Pandas
"""
#adding comment

#importing libraries
import pandas as pd


def data_loading(prop,log):
    resources = pd.read_csv(prop.get("Filepaths", "Resource_File_Path"),encoding = "ISO-8859-1")    
    standards = pd.read_csv(prop.get("Filepaths", "Standards_File_Path"),encoding = "ISO-8859-1")
    return resources,standards