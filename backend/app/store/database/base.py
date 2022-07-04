from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

meta = MetaData()
Base = declarative_base(meta)
