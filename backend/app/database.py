import os 

from sqlalchemy import URL, create_engine

database_url = URL.create(
    drivername  =   "postgresql+psycopg",
    username    =   os.environ["DB_USER"],
    password    =   os.environ["DB_PASSWORD"],
    host        =   os.environ["DB_HOST"],
    port        =   int(os.environ["DB_PORT"]),
    database    =   os.environ["DB_NAME"],
)

engine = create_engine(
    url             = database_url,
    pool_pre_ping   = True,
    connect_args    = {"connect_timeout": 5},
)

