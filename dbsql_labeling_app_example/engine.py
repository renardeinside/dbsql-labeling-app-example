from itertools import chain
from typing import List, Optional

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from dbsql_labeling_app_example.engine_provider import get_prepared_engine

engine = get_prepared_engine()
Base = declarative_base(bind=engine)


class Label(Base):
    __tablename__ = "labels"

    label_id = Column(Integer, primary_key=True)
    text = Column(String)
    label = Column(String)
