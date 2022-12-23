from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from models import *


async def get_stores(session: AsyncSession) -> list[Store]:
    # result = await session.execute(select(Store).order_by(Store.population.desc()).limit(20))
    result = await session.execute(select(Store))
    return result.scalars().all()


async def get_items(session: AsyncSession) -> list[Item]:
    result = await session.execute(select(Item))
    return result.scalars().all()


async def get_sales(session: AsyncSession) -> list[Sales]:
    result = await session.execute(select(Sales))
    return result.scalars().all()


async def get_top_items(session: AsyncSession) -> list[Sales]:
    result = await session.execute(
        select(Sales.item_id, Item.name, func.sum(Item.price)).join(Item, Item.id == Sales.item_id).group_by(Sales.item_id, Item.name).order_by(desc(func.sum(Item.price))))
    return result.all()


async def get_top_stores(session: AsyncSession) -> list[Sales]:
    result = await session.execute(
        select(Sales.store_id, func.count(Sales.store_id), Store.address).join(Store, Store.id == Sales.store_id).group_by(Sales.store_id, Store.address).order_by(desc(func.count(Sales.store_id))))
    return result.all()


def add_sale(session: AsyncSession, item_id: int, store_id: int):
    # sale_time = datetime.now()
    new_sale = Sales(item_id=item_id, store_id=store_id)
    session.add(new_sale)
    return new_sale
