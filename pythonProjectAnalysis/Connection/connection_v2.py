from sqlalchemy import MetaData, create_engine

meta = MetaData(schema="JKH")

def getEngine():
    s = "postgresql://postgres:2001@localhost:5432/Infrastructure"
    engine = create_engine(s)
    engine.connect()
    return engine
