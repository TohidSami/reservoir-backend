from flask import Flask, jsonify
from sqlalchemy import create_engine, text
import sys



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
    
if __name__ =="__main__":
    app.run(debug=True , port=5000)
