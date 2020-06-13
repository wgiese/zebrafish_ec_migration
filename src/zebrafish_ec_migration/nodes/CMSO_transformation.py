import pandas as pd
import numpy as np
from typing import Dict, List



def _read_IMARIS_cell_migration_data(filename):
    '''
    Function that extracts detailed time resolved data on cell migration for a given experimentonly vessel diameters for each experiment/fish over time.
    Input:
        filename of the
    
    
    Return:
        - df_stat: pandas DataFrame with information on vessel diameters over time
    '''
    
    if (not os.path.isfile(filename)):
        return pd.DataFrame()
    
    print("Open file: %s" % filename)
    
    
    sep = self.count_delimiters(open(filename, "r", encoding = "ISO-8859-1").read())
                    
    num_lines = sum(1 for line in open(filename, encoding = "ISO-8859-1"))
    
    if num_lines < 10:
        return pd.DataFrame()
    
    f = open(filename, "r", encoding = "ISO-8859-1")
    skip_row = 0
    
    for line in f.readlines():
        row = line.split(sep)
        if len(row) > 0:
            if row[0] == "Variable":
                break
            if row[0] == "Position X":
                break
        skip_row += 1
    
    f.close()
    
    if skip_row > 10:
        return pd.DataFrame()            
    
    df_stat = pd.read_csv(filename, skiprows=skip_row, sep=sep, encoding = "ISO-8859-1")
            
    return df_stat


def CMSO_movement_data(processed_key_file: pd.DataFrame, parameters: Dict, start_time, end_time) -> pd.DataFrame:
    
    imaris_data = dict()
    
    object_data = dict()
    

    
    
    for fish_number in processed_key_file["fish number"].unique():
        
        
        

        
        if (np.isnan(fish_number)):
            continue
               
        df_single_fish_all_groups = processed_key_file[processed_key_file['fish number'] == fish_number]
        
        for analysis_group in  df_single_fish_all_groups["analysis_group"].unique():
            
            
            
            df_single_fish = df_single_fish_all_groups[df_single_fish_all_groups["analysis_group"] == analysis_group]
            
            
            print("=================================================")
            print("fish number: %s" % int(fish_number))
            print("=================================================")
            
            print(df_single_fish)
            
            objects_df = pd.DataFrame({"X":[1,2],"Y":[3,4]}) 
        
            object_data['objects_fish_%s.csv' % int(fish_number)] = objects_df 
            
            #_read_IMARIS_cell_migration_data()
        
        
    return object_data
    
        
    #print("The following parameters are used: ")
    #print(parameters)
    
    #time_points = np.arange(start_time,end_time,parameters["time_resolution"])
    
    ##feature_dir = "./data/02_intermediate/" + "/feature_files_%s_%s_%s/" % (start_time,end_time,parameters["dt"])
    #movement_data_dir = "./data/02_intermediate/" + "/movement_data_%s_%s/" % (start_time,end_time)
    ##trajectory_dir = "./data/02_intermediate/" + "/plot_trajectories_%s_%s_%s/" % (start_time,end_time,parameters["dt"])



    #try:
        ## Create target Directory
        #os.mkdir(feature_dir)
        #print("Directory " , feature_dir ,  " Created ") 
    #except FileExistsError:
        #print("Directory " , feature_dir ,  " already exists")

    #try:
        ## Create target Directory
        #os.mkdir(movement_data_dir)
        #print("Directory " , movement_data_dir ,  " Created ") 
    #except FileExistsError:
        #print("Directory " , movement_data_dir ,  " already exists")
        
    #try:
        ## Create target Directory
        #os.mkdir(trajectory_dir)
        #print("Directory " , trajectory_dir ,  " Created ") 
    #except FileExistsError:
        #print("Directory " , trajectory_dir ,  " already exists")

    #features_df = pd.DataFrame()

    ##file_statistics_df = pd.DataFrame(data=[], index=[], columns=['#tracks','mean_track_length','max_step'])
    #file_statistics_df = pd.DataFrame()
    
    #df_key = preprocessed_key_file.copy()
    
    #ex = extract.ExtractData(parameters["data_dir"], key_filename = 'Key.xlsx')
    #f = extract_features.ExtractFeatures()
    #geo = extract_geometry.ExtractGeometry()
    
    #counter_statistics = 0
    
    #for fish_number in df_key["fish number"].unique():
       
    
        #if (np.isnan(fish_number)):
            #continue
               
        #df_single_fish_all_groups = df_key[df_key['fish number'] == fish_number]
        
        #for analysis_group in  df_single_fish_all_groups["analysis_group"].unique():
            

            
            #df_single_fish = df_single_fish_all_groups[df_single_fish_all_groups["analysis_group"] == analysis_group]
            
            
            #print("=================================================")
            #print("fish number: %s" % int(fish_number))
            #print("=================================================")
            
            #movement_data, key_row = ex.get_movement_data(fish_number, df_key, parameters["data_dir"], start_time, end_time, analysis_group)
