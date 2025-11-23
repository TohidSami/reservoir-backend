import numpy as np
import pandas as pd

days=60000
time_vector=np.arange(days)

well_params = {
    'Well-A1': {
        'oil_initial': 2000, 'oil_decline': 0.0001,
        'gor_initial': 800, 'gor_increase': 0.05,
        'wc_initial': 0.02, 'wc_increase': 0.00002
    },
    'Well-B2': {
        'oil_initial': 3000, 'oil_decline': 0.00015,
        'gor_initial': 600, 'gor_increase': 0.03,
        'wc_initial': 0.05, 'wc_increase': 0.00003
    },
    'Well-C13': {
        'oil_initial': 1500, 'oil_decline': 0.00005,
        'gor_initial': 1200, 'gor_increase': 0.08,
        'wc_initial': 0.01, 'wc_increase': 0.00001
    }
}
d1=[]
for well_name , params in well_params.items():
    
    noise_oil=np.random.normal(loc=1 , scale=0.03 , size=days)
    oil_rate=params['oil_initial']*np.exp(-params['oil_decline'])*time_vector
    oil=(oil_rate*noise_oil).clip(min=0)

    noise_g=np.random.normal(loc=1 , scale=0.05 , size=days)
    gor_trend=params['gor_initial']+params['gor_increase']*time_vector
    gor_rate=gor_trend*noise_g
    gas=(oil*gor_rate/  1000).clip(min=0)

    noise_w=np.random.normal(loc=1 , scale=0.05 , size=days)
    wc_trend=params['wc_initial']+params['wc_increase']*time_vector
    wc_rate=(wc_trend*noise_w).clip(min=0.01, max=0.95)
    water=(oil*(wc_rate/(1-wc_rate))).clip(min=0)

    dates=pd.date_range(start='1950-01-01' ,periods=days,freq='D')
    df=pd.DataFrame({
        'WellName':well_name,
        'ReportDate': dates,
        'OilProduction': oil,
        'GasProduction': gas,
        'WaterProduction': water
    })
    
    df['OilProduction'] = df['OilProduction'].astype('float32')
    df['GasProduction'] = df['GasProduction'].astype('float32')
    df['WaterProduction'] = df['WaterProduction'].astype('float32')


    d1.append(df)
    



    print("hi")
final=pd.concat(d1,ignore_index=True)
file_name = 'production_data_big.xlsx'
print("hello")
final.to_excel(file_name,index=False,engine='openpyxl')














print("hello")