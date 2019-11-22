# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 18:17:07 2019

@author: jennifer.john
"""


import datetime
import logging as log
from configparser import ConfigParser
from .driver_Inc import processResourceAlignment
#import sys
def main(method):
    # ------------------------------------------------------------------------------------------------------------------
    # Start the program
     if method=='train':
        start_exec_time = datetime.datetime.now()
        # ------------------------------------------------------------------------------------------------------------------
        # Fetch the properties and configurations
        prop = ConfigParser()
        prop.read(r"D:/Data_Science/Knovation_data/Incremental_Demo/Subjects/English/properties.ini")
        # ------------------------------------------------------------------------------------------------------------------
        #  Setup Logging mechanism
        for handler in log.root.handlers[:]:
            log.root.removeHandler(handler)
        log.basicConfig(filename=prop.get("Logging", "log_filepath")+"Knovation" + str(start_exec_time).split()[0] +".log",filemode = 'w',level=prop.get("Logging", "log_level"))
        #log.basicConfig(filename=prop.get("Logging", "log_filepath")+'knovation',level="INFO")
    
        log.info("-------------------------------------" + str(start_exec_time) + "-----------------------------------------")
            
        log.info("Initializing the process...")
        # -----------------------------------------------------------------------------------------------------------------
        # Fetch the properties and configurations
        log.info("Checking for configurations...")
        subject = (prop.get("Default", 'subject')).encode('UTF8')
        log.info(subject)
        log.info("Configurations loaded successfully...")
        # -----------------------------------------------------------------------------------------------------------------------
        
        processResourceAlignment(prop,log,method)
        end_exec_time = datetime.datetime.now()
    
        execution_response_time = end_exec_time - start_exec_time
        log.info("Execution time of the entire program is " + str(execution_response_time.total_seconds()))
        log.shutdown()
     elif method=='IncRes':
        start_exec_time = datetime.datetime.now()
        # ------------------------------------------------------------------------------------------------------------------
        # Fetch the properties and configurations
        prop = ConfigParser()
        prop.read(r"D:/Data_Science/Knovation_data/Incremental_Demo/Subjects/English/properties.ini")
        # ------------------------------------------------------------------------------------------------------------------
        #  Setup Logging mechanism
        for handler in log.root.handlers[:]:
            log.root.removeHandler(handler)
        log.basicConfig(filename=prop.get("Logging", "log_filepath")+"Knovation_test" + str(start_exec_time).split()[0] +".log",filemode = 'w',level=prop.get("Logging", "log_level"))
    #    log.basicConfig(filename=prop.get("Logging", "log_filepath")+'knovation',level="INFO")
    
        log.info(
            "-------------------------------------" + str(start_exec_time) + "-----------------------------------------")
        log.info("Initializing the process...")
        # -----------------------------------------------------------------------------------------------------------------
        # Fetch the properties and configurations
        log.info("Checking for configurations...")
        subject = (prop.get("Default", 'subject')).encode('UTF8')
        log.info(subject)
        log.info("Configurations loaded successfully...")
        # -----------------------------------------------------------------------------------------------------------------------
        
        processResourceAlignment(prop,log,method)
        end_exec_time = datetime.datetime.now()
    
        execution_response_time = end_exec_time - start_exec_time
        log.info("Execution time of the entire program is " + str(execution_response_time.total_seconds()))
        log.shutdown()      
     elif method=='IncStd':
        start_exec_time = datetime.datetime.now()
        # ------------------------------------------------------------------------------------------------------------------
        # Fetch the properties and configurations
        prop = ConfigParser()
        prop.read(r"D:/Data_Science/Knovation_data/Incremental_Demo/Subjects/English/properties.ini")
        # ------------------------------------------------------------------------------------------------------------------
        #  Setup Logging mechanism
        for handler in log.root.handlers[:]:
            log.root.removeHandler(handler)
        log.basicConfig(filename=prop.get("Logging", "log_filepath")+"Knovation_test" + str(start_exec_time).split()[0] +".log",filemode = 'w',level=prop.get("Logging", "log_level"))
    #    log.basicConfig(filename=prop.get("Logging", "log_filepath")+'knovation',level="INFO")
    
        log.info(
            "-------------------------------------" + str(start_exec_time) + "-----------------------------------------")
        log.info("Initializing the process...")
        # -----------------------------------------------------------------------------------------------------------------
        # Fetch the properties and configurations
        log.info("Checking for configurations...")
        subject = (prop.get("Default", 'subject')).encode('UTF8')
        log.info(subject)
        log.info("Configurations loaded successfully...")
        # -----------------------------------------------------------------------------------------------------------------------
        
        processResourceAlignment(prop,log,method)
        end_exec_time = datetime.datetime.now()
    
        execution_response_time = end_exec_time - start_exec_time
        log.info("Execution time of the entire program is " + str(execution_response_time.total_seconds()))
        log.shutdown()        
     
     
