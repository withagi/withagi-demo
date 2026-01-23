from pydantic import BaseModel
from typing import List
class Product(BaseModel):
    id: int
    name: str
    price: float
    inventory: int
class Order(BaseModel):
    id: int
    customer_name: str
    items: List[int]
    total: float