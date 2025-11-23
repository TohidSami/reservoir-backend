from app.database import engine
from sqlalchemy import text
print("slam")
def int_db():
    print("khod")
    with engine.connect() as conn:
        print("salam")
        conn.execute(text(""" CREATE TABLE IF NOT EXISTS "well_header"(
                          well_id SERIAL PRIMARY KEY,
                          well_name VARCHAR(100) NOT NULL UNIQUE,
                          uwi VARCHAR(50) UNIQUE,
                          field_name VARCHAR(100),
                          latitude FLOAT,
                          longitude FLOAT,
                          kb_elevation FLOAT); """))
        conn.execute(text("""
                            CREATE TABLE IF NOT EXISTS "production_data"(
                          prod_id SERIAL PRIMARY KEY,
                          well_id INTEGER REFERENCES "well_header"(well_id) ON DELETE CASCADE,
                          report_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                          oil_rate FLOAT,
                          gas_rate FLOAT,
                          water_rate FLOAT);
                            """))
        conn.execute(text(""" 
                            CREATE INDEX IF NOT EXISTS idx_prod_date
                            ON "production_data" (well_id, report_date);
                          """))
        conn.commit()
        print("tables ready")
if __name__=="__main__":
        int_db()