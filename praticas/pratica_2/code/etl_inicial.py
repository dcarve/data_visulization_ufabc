
import pandas as pd
import re
import numpy as np

superstore_orders = pd.read_excel(r'D:\19_UFABC\dava_viz\data_visulization_ufabc\praticas\pratica_2\VIS_Pr_02_Superstore.xls', sheet_name='Orders')
superstore_people = pd.read_excel(r'D:\19_UFABC\dava_viz\data_visulization_ufabc\praticas\pratica_2\VIS_Pr_02_Superstore.xls', sheet_name='People')
cotacao = pd.read_csv(r'D:\19_UFABC\dava_viz\data_visulization_ufabc\praticas\pratica_2\VIS_Pr_02_euro_cotacao_99_22.csv')

cotacao = cotacao[['Period\\Unit:', '[US dollar ]', '[Chinese yuan renminbi ]']]
cotacao.columns = ['period' , 'dollar' , 'yuan']

pattern = re.compile(r'[+-]?([0-9]*[.])?[0-9]+')

cotacao['dollar'] = cotacao.apply(lambda row: row['dollar'] if pattern.match(str(row['dollar'])) else np.nan, axis=1)
cotacao['yuan'] = cotacao.apply(lambda row: row['yuan'] if pattern.match(str(row['yuan'])) else np.nan, axis=1)

        

cotacao['euro'] = 1
cotacao['dollar'] = cotacao['dollar'].astype(float)
cotacao['yuan'] = cotacao['yuan'].astype(float)

cotacao['euro'] = cotacao['euro']/cotacao['dollar']
cotacao['yuan'] = cotacao['yuan'] * cotacao['euro']
cotacao['dollar'] = 1


cotacao['period'] = pd.to_datetime(cotacao['period'])


cotacao = cotacao.groupby(cotacao['period'].dt.to_period('Q'))['dollar', 'euro','yuan'].mean().reset_index()


superstore_orders['period'] = superstore_orders['Order Date'].dt.to_period('Q')


superstore_orders = superstore_orders.merge(cotacao, on='period', how='left')
superstore_orders = superstore_orders.merge(superstore_people, on='Region', how='left')

superstore_orders = superstore_orders[[
        'Order Date','Country', 'City', 'State', 'Postal Code', 'Region', 'Category', 'Sub-Category',  'Sales', 'Quantity', 'Discount', 'Profit', 'period',
       'dollar', 'euro', 'yuan', 'Person']]

superstore_orders.to_csv(r'D:\19_UFABC\dava_viz\data_visulization_ufabc\praticas\pratica_2\superstore_etl.csv')