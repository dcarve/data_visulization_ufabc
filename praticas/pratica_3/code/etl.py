# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import re


def read_data_and_clean_up():
    
    df = pd.read_csv('VIS_Pr_03_hungry_in_the_world.csv')
    
    cols  = list(df.columns)
    cols.remove("Country")
    
    
    
    def clean_up_countrie_names(row):
        if "d'Ivoire" in row['Country']:
            return "Côte d'Ivoire"
        elif "rkiye" in row['Country']:
            return "Turkiye"
        else:
            return row['Country']
    
    df['Country'] = df.apply(lambda row : clean_up_countrie_names(row), axis=1)
    
    
    
    def clean_up_numbers(row):
        if isinstance(row[col],str):
            res = re.findall(r"[-+]?(?:\d*\.*\d+)", row[col])[0]
        
            res_list = res.split('.')
            
            res_list = [i for i in res_list if i]
            
            res = '.'.join(res_list)
            
            return float(res)
        else:
            return row[col]
        
    
    
    for col in cols:
        df[col] = df.apply(lambda row : clean_up_numbers(row), axis=1)
        
    return df



def melt(df):
        
        
    cols  = list(df.columns)
    cols.remove("Country")
    cols.remove("Absolute change since 2014")
    cols.remove('Percent change sice 2014')
        
        
    df = df.melt(
            id_vars=['Country'],
            value_vars=cols,
            var_name='year',
            value_name='ghi'
    )
    

    return df
    
def percent(df):
            
    cols  = list(df.columns)
    cols.remove("Country")
    cols.remove("Absolute change since 2014")
    cols.remove('Percent change sice 2014')
    
    cols.sort()
    
    
    cols_percent = [[cols[i],cols[1+i]] for i in range(len(cols)) if i < len(cols)-1]
    cols_names = list()
    
    for n in cols_percent:
        cols_names.append((n[0],n[1]))
        df[(n[0],n[1])] = (df[n[1]]/df[n[0]]-1)
        
        df = df.replace([np.inf, -np.inf], np.nan)
        #df = df.replace([np.nan], 0)
        
    df = df.melt(
            id_vars=['Country'],
            value_vars=cols_names,
            var_name='year',
            value_name='percent_change'
    )
    
    df = df.dropna()
    
    df['period'] = df.apply(lambda row: '-'.join(row['year']), axis=1)
    df['year'] =  df.apply(lambda row: row['year'][1], axis=1)

    return df
    
    
    
    
df = read_data_and_clean_up()
df1 = melt(df)
df2 = percent(df)


df = df1.merge(df2, on=['Country','year'], how='outer')
df = df.sort_values(['Country','year'])



df.to_csv('clean_up_dataset.csv', index=False, sep='\t', decimal=',')