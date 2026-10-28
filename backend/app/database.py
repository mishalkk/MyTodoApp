import os 

from sqlalchemy import URL, create_engine
from collections.abc import Generator
from sqlalchemy.orm import Session, sessionmaker


database_url = URL.create(
    drivername  =   "postgresql+psycopg",
    username    =   os.environ["DB_USER"],
    password    =   os.environ["DB_PASSWORD"],
    host        =   os.environ["DB_HOST"],
    port        =   int(os.environ["DB_PORT"]),
    database    =   os.environ["DB_NAME"],
)

# TODO: Do we need a init_db() function which create all the tables

engine = create_engine(
    url             = database_url,
    pool_pre_ping   = True,
    connect_args    = {"connect_timeout": 5},
)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session 
        

