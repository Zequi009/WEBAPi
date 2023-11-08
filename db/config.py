from sqlmodel import create_engine, MetaData, Session

DRIVER = 'ODBC Driver 17 for SQL Server' 
SERVERNAME = 'DESKTOP-42FBDJK'
INSTANCENAME = '\SQLEXPRESS' 
DATABASE = 'ITSC_DB_v3' 
engine = create_engine(
    #pyodbc python y odbc significa open database connectivity (es un estándar de acceso a bd)
    f'mssql+pyodbc://@{SERVERNAME}{INSTANCENAME}/{DATABASE}?driver={DRIVER}'
)

def Get_Session():
    with Session(engine) as session:
        yield session

meta = MetaData()