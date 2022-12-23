from sqlalchemy import create_engine, MetaData

DB_USER = "postgres"
DB_NAME = "shop"
DB_PASSWORD = "admin"
DB_HOST = "127.0.0.1"


def add_date():
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        metaDats = MetaData(conn, schema="public")
        metaDats.reflect(bind=conn)
        table = metaDats.tables['public.item']
        items_list = [{"name": "Iphone 14", "price": 111111.11},
                      {"name": "Iphone 11", "price": 88888.88},
                      {"name": "Xiaomi 11", "price": 33333.33},
                      {"name": "Samsung Galaxy S22", "price": 55555.55}]
        for i in items_list:
            stmt = table.insert().values(**i)
            conn.execute(stmt)

        table = metaDats.tables['public.store']
        stores_list = [{"address": "ул. Мира д. 150"},
                       {"address": "ул. Южная д. 22"},
                       {"address": "ул. Северная д. 11"},
                       {"address": "ул. Восточная д. 33"}]

        for i in stores_list:
            stmt = table.insert().values(**i)
            conn.execute(stmt)


if __name__ == '__main__':
    add_date()
