from sqlalchemy import BLOB, Column, Float, Integer, String

from refactor_app.db import Base


class Sesssion(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, index=True)
    image_1 = Column(BLOB)
    image_2 = Column(BLOB)
    max_user_score = Column(Float)
    min_user_score = Column(Float)
    max_avg_score = Column(Float)
    min_avg_score = Column(Float)
    max_title = Column(String)
    min_title = Column(String)
    avg_score_diff = Column(Float)
    true_score_diff = Column(Float)
    plot = Column(BLOB)
