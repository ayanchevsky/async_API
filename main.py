from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, validator
from base import init_models
from base import get_session
import service
import add_date_to_db
import uvicorn as uvicorn


app = FastAPI()


class Store(BaseModel):
    id: int
    address: str

class StoreIn(BaseModel):
    address: str

class StoreTop(BaseModel):
    id: int
    address: str
    income: int                                             # Float ?

class Item(BaseModel):
    id: int
    name: str
    price: float

class ItemIn(BaseModel):
    name: str
    price: float

class ItemTop(BaseModel):
    id: int
    name: str
    sales_amount: int


class SaleIn(BaseModel):
    item_id: int
    store_id: int

    @validator('item_id', 'store_id', pre=True, always=True)
    def check_id(cls, v):
        if not isinstance(v, int) or v <= 0:
            #raise ValueError({"error": "Не корректные данные"})
            raise HTTPException(status_code=400, detail="Не корректные данные")
        return v


class Sale(BaseModel):
    id: int
    sale_time: datetime
    item_id: int
    store_id: int


@app.on_event("startup")
async def startup():
    # Drop and crate all tables in db
    await init_models()
    # add new data to db
    add_date_to_db.add_date()
    print("Done")


@app.get("/stores/", response_model=list[Store])
async def get_stores(session: AsyncSession = Depends(get_session)):
    stores = await service.get_stores(session)
    return [Store(id=c.id, address=c.address) for c in stores]


@app.get("/items/", response_model=list[Item])
async def get_items(session: AsyncSession = Depends(get_session)):
    items = await service.get_items(session)
    return [Item(id=c.id, name=c.name, price=c.price) for c in items]


@app.get("/sales/", response_model=list[Sale])
async def get_sales(session: AsyncSession = Depends(get_session)):
    sales = await service.get_sales(session)
    return [Sale(id=c.id, sale_time=c.sale_time, item_id=c.item_id, store_id=c.store_id) for c in sales]


@app.post("/sales/")
async def add_city(sale: SaleIn, session: AsyncSession = Depends(get_session)):
    new_sale = service.add_sale(session, sale.item_id, sale.store_id)
    await session.commit()
    return new_sale


@app.get("/items/top/", response_model=list[ItemTop])
async def get_sales_top(session: AsyncSession = Depends(get_session)):
    top_items = await service.get_top_items(session)
    return [ItemTop(id=c[0], name=c[2], sales_amount=c[1]) for c in top_items]


@app.get("/stores/top/", response_model=list[StoreTop])
async def get_stores_top(session: AsyncSession = Depends(get_session)):
    top_stores = await service.get_top_stores(session)
    return [StoreTop(id=c[0], address=c[1], income=c[2]) for c in top_stores]


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
