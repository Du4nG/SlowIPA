from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings as s

SQLALCHEMY_DATABASE_URL = f'postgresql://{s.database_username}:{s.database_password}@{s.database_hostname}/{s.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal  = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
       
# trường hợp dùng sql thuần 
'''
while True:
    try:
        conn = psycopg2.connect(host='localhost', 
                                database='fastapi',
                                port=5432,
                                user='postgres', password=1,
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Connected!')
        break
    except Exception as error:
        print('Error:', error)
        time.sleep(2)
'''