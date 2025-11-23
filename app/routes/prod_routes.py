from app.database import engine
from sqlalchemy import text
from flask import Blueprint, jsonify,request
import pandas as pd

prod_bp=Blueprint('production',__name__)
# prod_bp=Blueprint(name='production', import_name= __name__
#                   , url_prefix="/api/wells",template_folder='template',static_folder='static')

@prod_bp.route("/api/wells/<int:well_id>/production")
# def get_prod(well_id):
    # try:
        # # with engine.connect() as conn:
def get_production(well_id):
    with engine.connect() as conn:
        txt_well=text("SELECT well_id, report_date, oil_rate, gas_rate, water_rate"
        " FROM production_data  WHERE well_id=:id ORDER BY report_date ASC")
        production_history=[]
        result=conn.execute(txt_well,{"id":well_id})
        rows=result.fetchall()
        if not rows:
            return jsonify({
                    "well_id": well_id,
                    "message": "No production data found for this well.",
                    "data": []
                }), 404
        for row in rows:
            prod={
                "well_id":row.well_id,
                "date":str(row.report_date),
                "oil":round(row.oil_rate),
                "gas":round(row.gas_rate),
                "water":round(row.water_rate)
            }
            production_history.append(prod)
        return jsonify({
            "well_id": well_id,
            "count": len(production_history),
            "data": production_history
        })
    


@prod_bp.route("/api/wells/<int:well_id>/summery")
def get_summery(well_id):
    try: 
        with engine.connect() as conn:
            tx_smu=text("SELECT report_date, oil_rate, gas_rate, water_rate"
            " FROM production_data WHERE well_id=:id ORDER BY report_date ASC")
            result=conn.execute(tx_smu,{"id":well_id})
            rows=result.fetchall()
            if not rows:
                    return jsonify({
                    "well_id": well_id,
                    "message": "No production data found for this well.",
                    "data": []
                    }), 404
            
            df=pd.DataFrame(rows,columns=['report_date', 'oil_rate','gas_rate','water_rate'])
            cum_oil=df['oil_rate'].sum()
            cum_gas=df['gas_rate'].sum()
            cum_water=df['water_rate'].sum()

            cum_GOR=(cum_gas*1000)/cum_oil if cum_oil>0 else 0
            cum_WC=(cum_water)/(cum_water+cum_oil)*100 if cum_water+cum_oil>0 else 0
            First_date=str(df['report_date'].min())
            last_date=str(df['report_date'].max())
            day_prod=len(df)
            summary={
            "well_id":well_id,
            "dates":{
                "start":First_date,
                "last":last_date,
                "days on Production":day_prod
                     },
            "cumulative Production":{
                "cumulative OIL":round(cum_oil,2),
                "cumulative GAS":round(cum_gas,2),
                "cumulative WATER":round(cum_water,2)
            },
            "cumulative GOR":round(cum_GOR,2),
            "cumulative WC":round(cum_WC,2)
        }
        return jsonify(summary)
    
    except Exception as e:
        print(f"Error during summary calculation: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}),500





