from sqlalchemy import create_engine, Column, String, ForeignKey, Integer, DECIMAL, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    sku = Column(String(255), nullable=False)
    url_scraped = Column(Text, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    percent_discount = Column(DECIMAL(5, 2), nullable=False)
    price_discount = Column(DECIMAL(10, 4), nullable=False)
    tax = Column(DECIMAL(10, 4), nullable=False)
    price_included_taxes = Column(DECIMAL(10,4), nullable=False)
    price_mt2 = Column(DECIMAL(10, 4))
    price_mtl = Column(DECIMAL(10, 4))
    stock_1 = Column(Integer, nullable=False)
    stock_2 = Column(Integer)
    stock_3 = Column(Integer)
    stock_comentarie_1 = Column(String(100))
    stock_comentarie_2 = Column(String(100))
    stock_comentarie_3 = Column(String(100))
    images = Column(Text)  # Use JSON type if supported by your database
    category = Column(Text)
    route_product = Column(Text)
    short_description = Column(Text)
    long_description = Column(Text)
    pdf = Column(Text)
    length = Column(DECIMAL(10, 2))
    width = Column(DECIMAL(10, 2))
    height = Column(DECIMAL(10, 2))
    weight = Column(DECIMAL(10, 2))
    main_color = Column(String(255))
    glossy_or_matte = Column(String(50))
    main_material = Column(String(255))
    origen = Column(String(255))
    LastScrappeddate = Column(DateTime, onupdate=func.now())
    Updateddate = Column(DateTime, onupdate=func.now())
    Createddate = Column(DateTime, default=func.now())
    Status = Column(String(50))


# Define your database connection
engine = create_engine('mariadb+mariadbconnector://sdk:TKnApQsKErGlXv6H@localhost/sdk_aarque')
#engine = create_engine('mysql://root:root@localhost/aarque')

# Create the tables
Base.metadata.create_all(engine)
