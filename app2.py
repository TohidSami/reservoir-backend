from flask import Flask, jsonify, request,send_file
import pandas as pd
from sqlalchemy import create_engine, text
import sys
import matplotlib.pyplot as plt
import io  
import numpy as np


app = Flask(__name__)

DataBase1='postgresql://postgres:123salam@localhost:5432/test1'

try:
    engine=create_engine(DataBase1)
    
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print(f'/n')
    print("connected to DB") 

except Exception as e:
    print("cant connect")

@app.route("/api/wells/<int:well_id>")
def get_well_API(well_id):
    print(f"API req was for well {well_id} sent to /api/wells")
    #wells_list=[]
    try:
        with engine.connect() as conn:
            txt_well_api=text("SELECT well_id, well_name, uwi,latitude,longitude, kb_elevation, field_name FROM WellHeader WHERE well_id=:id" )
            in_well={"id":well_id}
            ResWellAPI=conn.execute(txt_well_api,in_well)
            row=ResWellAPI.fetchone()            
            if row:
                well_data={
                         "well_id":row.well_id,
                         "well_name":row.well_name,
                         "uwi":row.uwi,
                         "field":row.field_name,
                         "location":{
                              "lat":row.latitude,
                              "lon":row.longitude
                         }
                    }
                #wells_list.append(well_data)
            else:
                return jsonify({"error": "Not Found", "message": f"this well id : {well_id} was not founded"}), 404
        return jsonify(well_data)
    except Exception as e:
        print(f"خطا در : {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)})
    

@app.route("/api/wells/<int:well_id>/production")
def get_production(well_id):
    with engine.connect() as conn:
        txt_well=text("SELECT well_id, report_date, oil_rate, gas_rate, water_rate"
        " FROM production  WHERE well_id=:id ORDER BY report_date ASC")
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
    
@app.route("/api/wells/<int:well_id>/summery")
def get_summery(well_id):
    try: 
        with engine.connect() as conn:
            tx_smu=text("SELECT report_date, oil_rate, gas_rate, water_rate"
            " FROM production  WHERE well_id=:id ORDER BY report_date ASC")
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




@app.route("/api/wells", methods=['POST'])
def create_well():
    try:
        in_data=request.json    #input
    except Exception as e:
        return jsonify({"error": "Invalid JSON", "message": str(e)}), 400 # 400 = Bad Request
    # validation incoming data
    req_field=['well_name', 'uwi', 'field_name', 'latitude', 'longitude', 'kb_elevation']
    for field in req_field:
        if field not in in_data:
            return jsonify({"error": "Missing field", "message": f"'{field}' is required."}), 400
    
    #prepare the sql to add
    try:
        with engine.connect() as conn:
            tx_sql=text("INSERT INTO WellHeader (well_name, uwi, field_name, latitude, longitude, kb_elevation)"
        "VALUES (:well_name, :uwi, :field_name, :latitude, :longitude, :kb_elevation)"
        "RETURNING well_id;")
            
            result=conn.execute(tx_sql,in_data)
            new_id=result.fetchone().well_id # id added from the sql returns
            conn.commit()
            new_well_data=in_data.copy()
            new_well_data['well_id']=new_id
            # 201 = "Created" (the standard HTTP code for a successful POST)
            return jsonify({
                "message": "Well created successfully",
                "well": new_well_data
            }), 201
    except Exception as e:
        # Handle errors, e.g., 'well_name' or 'uwi' is not unique
        print(f"Error during database INSERT: {e}")
        return jsonify({"error": "Database Error", "message": str(e)}), 500

@app.route("/api/wells/")
def AllWellAPI():
    print("API req was sent to /api/wells")
    wells_list=[]
    try:
        with engine.connect() as conn:
            txt_well_api=text("SELECT well_id, well_name, uwi,latitude,longitude, kb_elevation, field_name FROM WellHeader")    
            ResWellAPI=conn.execute(txt_well_api)
            for row in ResWellAPI:
                well_data={
                         "well_id":row.well_id,
                         "well_name":row.well_name,
                         "uwi":row.uwi,
                         "field":row.field_name,
                         "location":{
                              "lat":row.latitude,
                              "lon":row.longitude
                         }
                    }
                wells_list.append(well_data)
        return jsonify(wells_list)
    except Exception as e:
        print(f"خطا در : {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)})

@app.route("/api/wells/<int:well_id>",methods=['PUT'])
def put_wells(well_id):
    try:
        in_data=request.json
    except Exception as e:
        return jsonify({"error": "Invalid JSON", "message": str(e)}), 400
    #validation
    req_fields=['well_name', 'uwi', 'field_name', 'latitude', 'longitude', 'kb_elevation']
    if not all(field in in_data for field in req_fields):
        return jsonify({"error": "Missing fields", "message": "All fields are required for a PUT update."}), 400
    try:
        with engine.connect() as conn:
            tx_sql=text("UPDATE WellHeader  SET well_name = :well_name,"
            "uwi = :uwi,"
            "field_name = :field_name,"
            "latitude = :latitude,"
            "longitude = :longitude,"
            "kb_elevation = :kb_elevation"
            " WHERE well_id= :well_id")
            in_data['well_id']=well_id
            result=conn.execute(tx_sql,in_data)
            conn.commit()
            if result.rowcount==0:
                return jsonify({"error":"Not Found", "message":f"No Well Found with ID ={well_id} to update"}),404
            return jsonify({
                "message": f"Well {well_id} updated successfully",
                "updated_data": in_data
            })
    except Exception as e:
        # Handle errors (like duplicate uwi or well_name)
        print(f"Error during database UPDATE: {e}")
        return jsonify({"error": "Database Error", "message": str(e)}), 500

@app.route("/api/wells/<int:well_id>", methods=['DELETE'])
def delete_well(well_id):
    try:
        with engine.connect() as conn:
            tx_sql=text("DELETE FROM WellHeader WHERE well_id=:well_id")
            result=conn.execute(tx_sql,{"well_id":well_id})
            conn.commit()
            if result.rowcount==0:
                return jsonify({"error":"Not FOund","message":f"No well founded with this ID = {well_id} to delete"}),404
            return jsonify({"message":f"Well {well_id} deleted successfully"})
            
    except Exception as e:
        print(f"Error during database DELETE: {e}")
        return jsonify({"error": "Database Error", "message": str(e)}), 500


@app.route("/api/wells/<int:well_id>",methods=['PATCH'])
def patch_well(well_id):
    try:
        in_data=request.json
    except Exception as e:
        return jsonify({"error":"Invalid jason", "message":str(e)}),400
    if in_data==[]:
        return jsonify({"error":"Bad Request","message":"No data provided"}),400
    valid_fields = ['well_name', 'uwi', 'field_name', 'latitude', 'longitude', 'kb_elevation']
    set_clause_parts=[]
    params={}
    for key, value in in_data.items():
        if key in valid_fields:
            set_clause_parts.append(f"{key} = :{key}")
            params[key]=value
        else:
            print(f"Warning: Ignoring invalid update field '{key}'")
    if not set_clause_parts:
        return jsonify({"error":"Bad Request","message":"No valid fields provided for update"}),400
    tx_sql=text("UPDATE WellHeader SET " + ", ".join(set_clause_parts) + " WHERE well_id = :well_id")
    params['well_id'] = well_id
    try:
        with engine.connect() as conn:
            result=conn.execute(tx_sql,params)
            conn.commit()
            if result.rowcount==0:
                return jsonify({"error":"Not Found","message":f"No well found with ID {well_id} to update."}), 404
            tx_sql1=text("SELECT * FROM WellHeader WHERE well_id=:well_id")
            result1=conn.execute(tx_sql1,{"well_id":well_id})
            updated_well=result1.fetchone()
            # Convert row to dictionary (we need to handle this manually)
            updated_data = {
                "well_id": updated_well.well_id,
                "well_name": updated_well.well_name,
                "uwi": updated_well.uwi,
                "field_name": updated_well.field_name,
                "latitude": updated_well.latitude,
                "longitude": updated_well.longitude,
                "kb_elevation": updated_well.kb_elevation
            }
        return jsonify({
                "message": f"Well {well_id} patched successfully",
                "updated_well": updated_data
            })

    except Exception as e:
        print(f"Error during database PATCH: {e}")
        return jsonify({"error": "Database Error", "message": str(e)}), 500

## ==========================================================
#  API Endpoint to Generate a 3-Panel Production Plot
# ==========================================================
@app.route("/api/wells/<int:well_id>/plot")
def get_plot_for_well_api(well_id):
    """
    Generates a 3-panel production plot (Oil, GOR, WC)
    and returns it as a PNG image.
    """
    print(f"API request received for 3-PANEL PLOT for well_id: {well_id}")
    
    # 1. SQL Query - We now need all rates
    sql_query = text("""
        SELECT report_date, oil_rate, gas_rate, water_rate
        FROM production 
        WHERE well_id = :id
        ORDER BY report_date ASC
    """)
    
    try:
        with engine.connect() as connection:
            # 2. Fetch data into Pandas
            df = pd.read_sql(sql_query, connection, params={"id": well_id})

        if df.empty:
            return jsonify({"error": "Not Found", "message": "No production data to plot."}), 404

        # 3. Engineering Calculations (The "Logic")
        # Set date as index (good for time-series plots)
        df.set_index('report_date', inplace=True)
        
        # Calculate GOR (scf/bbl)
        # We replace 0 oil rate with a tiny number to avoid divide-by-zero error
        df['gor'] = (df['gas_rate'] * 1000) / df['oil_rate'].replace(0, 0.001)
        
        # Calculate Water Cut (%)
        total_liquid = df['oil_rate'] + df['water_rate']
        df['wc'] = (df['water_rate'] / total_liquid.replace(0, 0.001)) * 100
        
        # Handle potential infinite or NaN values from division
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.fillna(0, inplace=True) # Fill any NaNs with 0 for plotting

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
        
        # Plot 1: Oil Rate
        ax1.plot(df.index, df['oil_rate'], color='green', label='Oil Rate')
        ax1.set_ylabel('Oil Rate (bbl/day)')
        ax1.legend()
        ax1.grid(True)
        ax1.set_title(f'Production Plots for Well ID: {well_id}', fontsize=14)

        # Plot 2: GOR
        ax2.plot(df.index, df['gor'], color='red', label='GOR')
        ax2.set_ylabel('GOR (scf/bbl)')
        ax2.legend()
        ax2.grid(True)

        # Plot 3: Water Cut
        ax3.plot(df.index, df['wc'], color='blue', label='Water Cut')
        ax3.set_ylabel('Water Cut (%)')
        ax3.set_xlabel('Date') # Only set X-label on the bottom plot
        ax3.legend()
        ax3.grid(True)

        # 5. Save the plot to a memory buffer
        plt.tight_layout() # Cleans up the plot margins
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig) # Close the figure to free up memory

        # 6. Send the PNG image as a file response
        return send_file(
            buf,
            mimetype='image/png',
            as_attachment=False,
            download_name=f'well_{well_id}_plots.png'
        )

    except Exception as e:
        print(f"Error during plot generation: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500









# get_summery(2)
if __name__ =="__main__":
    app.run(debug=True , port=5000)
