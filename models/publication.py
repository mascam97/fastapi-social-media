from config.database import Base
from sqlalchemy import Column, Integer, String

class Publication(Base):

    __tablename__ = "publications"

    id = Column(Integer, primary_key = True)
    title = Column(String)
    content = Column(String)
    state = Column(String)