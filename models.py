from datetime import datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer, Float, DateTime
from base import Base


# Описание моделей БД
class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), unique=True, comment="Наименование товарной позиции")
    price = Column(Float, comment="Стоимость единицы товара")


class Store(Base):
    __tablename__ = "store"
    id = Column(Integer, autoincrement=True, primary_key=True)
    address = Column(String(255), comment="Адрес магазина")


class Sales(Base):
    __tablename__ = "sales"
    id = Column(Integer, autoincrement=True, primary_key=True)
    sale_time = Column(DateTime, nullable=False, default=datetime.now)
    item_id = Column(Integer, ForeignKey('item.id'))
    store_id = Column(Integer, ForeignKey('store.id'))
