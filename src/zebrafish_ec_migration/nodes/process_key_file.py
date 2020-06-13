import pandas as pd
import numpy as np
from typing import Dict, List


def preprocess_key_file(parameters: Dict) -> pd.DataFrame:

    default_load_args = {"engine": "xlrd", "skiprows" : 1}
    df_key =  pd.read_excel(parameters["key_file"], **default_load_args)

    preprocessed_key_file = _specify_analysis_groups(df_key)

    return preprocessed_key_file
    


def _specify_analysis_groups(df_key):

    
    #TODO: remove some code chunks here since many columns are not needed anymore
    
    df_key = df_key.rename(columns={'File name': 'filename'})
    
    df_key = df_key[~df_key['filename'].isnull()]

    df_key['imaging start [dpf]'] = df_key.loc[:, 'dpf']

    df_key.rename(index=str, columns={'vessel type': 'vessel_type'}, inplace=True)

    df_key['vessel_type'] = ['aorta' if d_['Aorta'] else ('dlav' if d_['DLAV'] else 'isv') for _, d_ in
                            df_key.iterrows()]  # vessel type

    df_key['isv_type']  =  ['aISV' if d_['aISV'] else ('vISV' if d_['vISV'] else ('either' if d_['ISV'] else 'none')) for _, d_ in
                                                            df_key.iterrows()]  # vessel type`
    # df_key.loc[df_key['vessel_type']!='isv', 'isv_type']  =  ['aISV' if d_['aISV'] else ('vISV' if d_['vISV'] else ('either' if d_['ISV'] else 'none')) for _, d_ in

    df_key['filename_short'] = [fn_['filename'][fn_['filename'].find('Statistics on cell migration'):] for _, fn_ in
                                df_key.iterrows()]
    df_key['filename_short'] = [fns.replace('.csv', '') for fns in df_key['filename_short']]

    df_key['is_control'] = np.array(df_key['tnnt2'] == 0) * \
                            np.array(df_key['CK-666'] == 0) * \
                            np.array(df_key['CK689'] == 0) * \
                            np.array(df_key['Tricaine'] == 0) * \
                            np.array(df_key['Epinephrine'] == 0) * \
                            np.array(df_key['Glycerin'] == 0) * \
                            np.array(df_key['DMSO'] == 0) * \
                            np.array(df_key['WaspI [um]'] == 0) * \
                            np.array(df_key['WaspII [um]'] == 0) * \
                            np.array(df_key['Wiskostatin'] == 0) * \
                            np.array(df_key['ctr morpholino [um]'] == 0) * \
                            np.array(df_key['Rac1 or Cdc42'] == 'None') * \
                            np.array(df_key['Gata1 400uM'] == 'None')


    df_key['is_Tricaine'] = (df_key['Tricaine'] > 0)
    df_key['is_Epinephrine'] = (df_key['Epinephrine'] > 0)
    df_key['is_Glycerin'] = (df_key['Glycerin'] > 0)
    df_key['is_DMSO'] = (df_key['DMSO'] > 0)
    df_key['is_WaspI'] = (df_key['WaspI [um]'] > 0)
    df_key['is_WaspII'] = (df_key['WaspII [um]'] > 0)
    df_key['is_CK666'] = (df_key['CK-666'] > 0)
    df_key['is_CK689'] = (df_key['CK689'] > 0)
    df_key['is_tnnt2'] = (df_key['tnnt2'] > 0)
    df_key['is_Wiskostatin'] = (df_key['Wiskostatin'] > 0)
    df_key['is_ctrMorpholino'] = (df_key['ctr morpholino [um]'] > 0)
    df_key['is_Gata1'] = df_key['Gata1']==True
    df_key['is_Rac1'] = df_key['Rac1 or Cdc42'] == 'Rac1'
    df_key['is_cdc42'] = df_key['Rac1 or Cdc42'] == 'Cdc42T17N'
    df_key['is_Rac1'] = df_key['Rac1 or Cdc42'] == 'Rac1'


    df_key['exp_type'] = ['ctr_'*f_['is_control'] + \
                            'tric_'*f_['is_Tricaine'] + \
                            'epi_' * f_['is_Epinephrine'] + \
                            'glyc_' * f_['is_Glycerin'] + \
                            'dmso_' * f_['is_DMSO'] + \
                            'waspI_' * f_['is_WaspI'] + \
                            'waspII_' * f_['is_WaspII'] + \
                            'ck666_' * f_['is_CK666'] + \
                            'ck689_' * f_['is_CK689'] + \
                            'tnnt2_' * f_['is_tnnt2'] + \
                            'wisk_' * f_['is_Wiskostatin'] + \
                            'Rac1_' * f_['is_Rac1'] + \
                            'Gata1_' * f_['is_Gata1'] + \
                            'cdc42_' * f_['is_cdc42'] + \
                            'ctrMorph_' * f_['is_ctrMorpholino'] + \
                            'fish' for _, f_ in df_key.iterrows()]
       
        
    result_df = df_key.copy()
    
    
    for index, row in result_df.iterrows():

        if pd.isna(row['WaspI [100uM]']) and pd.isna(row['WaspI [100uM].1']):
            result_df.at[index,'WaspI [100uM] (merged)'] = 0
        elif (not pd.isna(row['WaspI [100uM]'])):
            result_df.at[index,'WaspI [100uM] (merged)'] = row['WaspI [100uM]']
        else:
            result_df.at[index,'WaspI [100uM] (merged)'] = row['WaspI [100uM].1']
            
    
    analysis_group = "none"
    
    control_false = ['WaspI [50uM]', 'WaspI [100uM] (merged)',  'WaspI [200uM]', 'WaspII [50uM]', 'WaspII [100uM]', 'WaspII [200uM]',
                    'tnnt2', 'Gata1', 'Rac1T17N', 'Cdc42G12V', 'Cdc42T17N', 'CK-666', 'CK689', 'Tricaine', 'Epinephrine', 'Glycerin', 'Wiskostatin', 'DMSO']
    
    wasp_50_false = ['WaspI [100uM] (merged)', 'WaspI [200uM]', 'WaspII [50uM]', 'WaspII [100uM]', 'WaspII [200uM]', 'tnnt2', 'Gata1',
                    'Rac1T17N', 'Cdc42G12V', 'Cdc42T17N', 'CK-666', 'CK689', 'Tricaine', 'Epinephrine', 'Glycerin', 'Wiskostatin', 'DMSO']
    
    
    wasp_100_false = ['WaspI [50uM]', 'WaspI [200uM]','WaspII [50uM]', 'WaspII [100uM]', 'WaspII [200uM]','tnnt2', 'Gata1',
                    'Rac1T17N', 'Cdc42G12V', 'Cdc42T17N', 'CK-666', 'CK689', 'Tricaine', 'Epinephrine', 'Glycerin', 'Wiskostatin', 'DMSO']
    
    gata1_false = ['WaspI [50uM]', 'WaspI [100uM] (merged)', 'WaspI [200uM]', 'WaspII [50uM]', 'WaspII [100uM]', 'WaspII [200uM]','tnnt2',
                'Rac1T17N', 'Cdc42G12V', 'Cdc42T17N', 'CK-666', 'CK689', 'Tricaine', 'Epinephrine', 'Glycerin', 'Wiskostatin', 'DMSO'] 
    
    
    gata1_wasp1_false = ['Control', 'WaspII [50uM]', 'WaspII [100uM]', 'WaspII [200uM]', 'tnnt2', 
                        'Rac1T17N', 'Cdc42G12V', 'Cdc42T17N', 'CK-666', 'CK689', 'Tricaine', 'Epinephrine', 'Glycerin', 'Wiskostatin', 'DMSO']
    
    
    df_control =  result_df[result_df['Control']==1]
    
    for cond in control_false:
        df_control =  df_control[df_control[cond]!=1]
        
    df_control["analysis_group"] = pd.Series(["control" for i in range(len(df_control))], index=df_control.index)    
    
    
    
    df_wasp_50 =  result_df[result_df['WaspI [50uM]']==1]
    
    for cond in wasp_50_false:
        df_wasp_50 =  df_wasp_50[df_wasp_50[cond]!=1]
        
    df_wasp_50["analysis_group"] = pd.Series(['WaspI [50uM]' for i in range(len(df_wasp_50))], index=df_wasp_50.index)  
    
    
    
    df_wasp_100 =  result_df[result_df['WaspI [100uM] (merged)']==1]
            
    for cond in wasp_100_false:
        df_wasp_100 =  df_wasp_100[df_wasp_100[cond]!=1]
        
    df_wasp_100["analysis_group"] = pd.Series(['WaspI [100uM]' for i in range(len(df_wasp_100))], index=df_wasp_100.index)  
    
    
    
    df_gata1 =  result_df[result_df['Gata1']==1]
            
    for cond in gata1_false:
        df_gata1 =  df_gata1[df_gata1[cond]!=1]
        
    df_gata1["analysis_group"] = pd.Series(['Gata1' for i in range(len(df_gata1))], index=df_gata1.index)  
    
    
    
    df_wasp_gata1 =  result_df[result_df['Gata1']==1]
                    
    df_wasp_gata1 = df_wasp_gata1[df_wasp_gata1['WaspI [100uM] (merged)'] == 1]
                    
    for cond in gata1_wasp1_false:
        df_wasp_gata1 =  df_wasp_gata1[df_wasp_gata1[cond]!=1]
        
    df_wasp_gata1["analysis_group"] = pd.Series(['Gata1_Wasp1' for i in range(len(df_wasp_gata1))], index=df_wasp_gata1.index)  
    
    
    
    return pd.concat([df_control,df_wasp_100,df_gata1,df_wasp_gata1],ignore_index=True) 

