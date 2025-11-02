from sqlalchemy import Column, Integer, String, Float
from database import Base

class cars(Base):
    __tablename__ = 'sample_car'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    price = Column(Float, index=True)
    # price_rs = Column(Float, index=True)