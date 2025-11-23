from app.database import engine
from sqlalchemy import text
from flask import Blueprint, jsonify,request


well_bp = Blueprint('wells', __name__)

@well_bp.route("/api/wells",methods=['GET'])
def get_well():
    # well_list=[]
    try:
        with engine.connect() as conn:
            tx_sql=text("SELECT well_id, well_name, uwi,latitude,longitude, kb_elevation, field_name FROM well_header")
            result=conn.execute(tx_sql)
            # for row in result:
            well_list=[{"id": row.well_id ,"name": row.well_name, "field": row.field_name, "uwi": row.uwi} for row in result]
            return jsonify(well_list)
    except Exception as e:
        return jsonify({"error":str(e)}), 500


@well_bp.route("/api/wells", methods=['POST'])
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
            tx_sql=text("INSERT INTO well_header (well_name, uwi, field_name, latitude, longitude, kb_elevation)"
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

@well_bp.route("/api/wells/<int:well_id>",methods=['PUT'])
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
            tx_sql=text("UPDATE well_header  SET well_name = :well_name,"
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


@well_bp.route("/api/wells/<int:well_id>", methods=['DELETE'])
def delete_well(well_id):
    try:
        with engine.connect() as conn:
            tx_sql=text("DELETE FROM well_header WHERE well_id=:well_id")
            result=conn.execute(tx_sql,{"well_id":well_id})
            conn.commit()
            if result.rowcount==0:
                return jsonify({"error":"Not FOund","message":f"No well founded with this ID = {well_id} to delete"}),404
            return jsonify({"message":f"Well {well_id} deleted successfully"})
            
    except Exception as e:
        print(f"Error during database DELETE: {e}")
        return jsonify({"error": "Database Error", "message": str(e)}), 500


@well_bp.route("/api/wells/<int:well_id>",methods=['PATCH'])
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
    tx_sql=text("UPDATE well_header SET " + ", ".join(set_clause_parts) + " WHERE well_id = :well_id")
    params['well_id'] = well_id
    try:
        with engine.connect() as conn:
            result=conn.execute(tx_sql,params)
            conn.commit()
            if result.rowcount==0:
                return jsonify({"error":"Not Found","message":f"No well found with ID {well_id} to update."}), 404
            tx_sql1=text("SELECT * FROM well_header WHERE well_id=:well_id")
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


@well_bp.route("/api/wells/<int:well_id>")
def get_well_API(well_id):
    print(f"API req was for well {well_id} sent to /api/wells")
    #wells_list=[]
    try:
        with engine.connect() as conn:
            txt_well_api=text("SELECT well_id, well_name, uwi,latitude,longitude, kb_elevation, field_name FROM well_header WHERE well_id=:id" )
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
    







