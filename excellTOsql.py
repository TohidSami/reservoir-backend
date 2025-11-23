from sqlalchemy import create_engine, text
import pandas as pd
import os 

# db_url="postgresql://postgres:123salam@localhost:5432/test1"
db_url=os.environ.get(
    "DATABASE_URL", 
    # "postgresql://postgres:123salam@localhost:5432/test1"
    "postgresql://postgres:123456@localhost:5433/res_db"
)


try:
    engine=create_engine(db_url)
    with engine.connect() as conn:
        result=conn.execute(text("SELECT well_id, well_name FROM well_header"))
        print("con to db")
        well_map = {row.well_name: row.well_id for row in result}
        filename="production_data_big.xlsx"
        df=pd.read_excel(filename)
        df['well_id'] = df['WellName'].map(well_map)
        df.rename(columns={
        'ReportDate': 'report_date',
        'OilProduction': 'oil_rate',
        'GasProduction': 'gas_rate',
        'WaterProduction': 'water_rate'
        }, inplace=True)
        final_columns = ['well_id', 'report_date', 'oil_rate', 'gas_rate', 'water_rate']
        df_final = df[final_columns]
        
        print("hi")
        df_final.to_sql(
        "production_data", 
        con=engine, 
        if_exists='append', 
        index=False,
        chunksize=10000 
    )
        # df_final.to_sql("production_data",con=engine,if_exists='append',index=False)
        


except Exception as e:
    print ("not")