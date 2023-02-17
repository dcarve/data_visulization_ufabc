import pandas as pd
import numpy as np
import matplotlib

# pré convertido para utf-8
df = pd.read_csv('VIS_Pr_01_Vendas.csv')

df = df.groupby('Region').agg(
    {
        'Sales': ['sum'],
        'Profit': ['sum'],
        'Discount': ['mean']
                
    }
).reset_index()


df.columns = ["_".join(t).strip('_') for t in df.columns]

#exportando csv configurações do MS excel
df.to_csv('result_q1.csv', sep=';', index=False, encoding='utf-8-sig')
