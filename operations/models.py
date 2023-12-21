from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, ForeignKey

metadata = MetaData()

####### Проверка функционала для внедрения в products (для тестирования новых функций)
operation = Table(
    "operation",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("quantity", String),
    Column("figi", String),
    Column("instrument_type", String, nullable=True),
    Column("date", TIMESTAMP),
    Column("type", String),
)

class OperationCreate(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str
####################################



product = Table(
    "product",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("type", String, nullable=False),
    Column("variety", String, nullable=False),
    Column("maker", String, nullable=False),
    Column("description", String, nullable=False),
    Column("img", String, nullable=False),
    Column("availability", Integer, nullable=False),
    Column("characteristic", String, nullable=False),
)

class ProductCreate(BaseModel):
    id: int
    name: str
    type: str
    variety: str
    maker: str
    description: str
    img: str
    maker: str
    availability: int
    characteristic: str





basket = Table(
    "basket",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("product_id", Integer)
)

class BasketCreate(BaseModel):
    user_id: int
    product_id: int






order = Table(
    "order",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("product_id", Integer, nullable=False),
)

class OrderCreate(BaseModel):
    user_id: int
    product_id: int