import pandas as pd

# pré convertido para utf-8
df = pd.read_csv('VIS_Pr_01_Vendas.csv')

df = df.copy()

df['perform']  = df['Profit']/(df['Sales']-df['Discount'])

df = df.groupby(['Customer Name', 'Segment']).agg(
    {
        'perform': ['mean']
    }
).reset_index()

df.columns = [t[0] for t in df.columns]


def f(x):
    
    if x<0.1:
        return "E"
    elif (x>-0.1) and (x<0.15):
        return "D"
    elif (x>-0.15) and (x<0.2):
        return "C"
    elif (x>-0.2) and (x<0.25):
        return "B"
    elif (x>-0.25):
        return "A"


df['perform'] = df.apply(lambda row: f(row['perform']), axis=1)


#exportando csv configurações do MS excel
df.to_csv('result_q3.csv', sep=';', index=False, encoding='utf-8-sig')
