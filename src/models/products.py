from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.models import Base, session

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description= Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    active= Column(Integer, default=1)  # 1 for active, 0 for inactive

    def __init__(self, name, description, price, stock, category_id, active=1):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.category_id = category_id
        self.active = active

    def __repr__(self):
         return f"<Products(id={self.id}, name='{self.name}', price={self.price}, stock={self.stock}, category_id={self.category_id}, active={self.active})>" 
    
    def get():
     products = session.query(Products).all()
     return products