from sqlalchemy import create_engine, text, SQLColumnExpression
import sys

DataBase1='postgresql://postgres:123salam@localhost:5432/test1'
try:            # خب این برای این که ببنی وصل میشود یا نه  
    engine=create_engine(DataBase1)

    with engine.connect() as connection:
        print("اتصال موفقیت آمیز بود")

        sqlcom=text("SELECT well_name, field_name FROM WellHeader")

        output1=connection.execute(sqlcom)

        for row in output1:
            print(f"نام چاه :  {row.well_name}  field : {row.field_name}")
except Exception as e:
    print("cant connect")
    print(f"خطا: {e}")
    sys.exit()

def get_all_wells():
    with engine.connect() as conn:
        Forgetwells=text('SELECT well_name, field_name FROM WellHeader')
        resgetwells=conn.execute(Forgetwells)
        for row in resgetwells:
            print(f" well nemes: {row.well_name} and field name is : {row.field_name}")
            print ( "-" *20)
def add_new_well(name, uwi, fi, lat, lon, kb):
    
    txAdd=text("""INSERT INTO WellHeader (well_name, uwi, latitude, longitude, kb_elevation , field_name )    VALUES (:well_name, :uwi, :lat, :lon, :kb, :fi)""")
    inAdd={
        "well_name":name,
        "uwi":uwi,
        "lat":lat,
        "lon":lon,
        "kb":kb,
        "fi":fi,
    }
    try:
        with engine.connect() as conn:
         conn.execute(txAdd,inAdd)
         conn.commit()
         print(f"well {name} added successfully ")
    except Exception as e:
        print("can't add that")
        print(f"the error: {e}")
    print("-" *20)

def find_well(name):
    txFind=text("SELECT * FROM WellHeader WHERE well_name = :name")
    inFind={"name":name}
    try:
        with engine.connect() as conn:
            resFind=conn.execute(txFind,inFind)
            wF=resFind.fetchone()
            if wF:
                print(f"ID : {wF.well_id}")
                print(f"the well name is : {wF.well_name}")
                print(f"the uwi is :{wF.uwi}")
            else:
                print(f"can't find the {name} well")
    except Exception as e:
        print(f"cant find that because {e}")
if __name__ == "__main__":
    get_all_wells()
    add_new_well(
        name="Well-C13", 
        uwi="UWI-003", 
        fi="Gachsaran", 
        lat=29.54321, 
        lon=49.12345, 
        kb=210.0
    )
    get_all_wells()
    
    # 4. حالا فقط چاه "Well-A1" را پیدا کن
    find_well("Well-C13")
    
    # 5. سعی کن چاهی که وجود ندارد را پیدا کنی
    find_well("Non-Existent-Well")                