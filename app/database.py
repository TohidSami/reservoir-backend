from sqlalchemy import create_engine
import os


db_url=os.environ.get(
    "DATABASE_URL", 
    # "postgresql://postgres:123salam@localhost:5432/test1"
    "postgresql://postgres:123456@localhost:5433/res_db"
)
# "postgresql://postgres:123salam@localhost:5432/test1"
engine=create_engine(db_url)