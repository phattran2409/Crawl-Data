from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection
engine = create_engine('postgresql://postgres:123456789@localhost:5432/postgres')

# Define the base class
Base = declarative_base()

# Define the table with a primary key
class Product(Base):
    __tablename__ = 'Products'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Price = Column(Integer)
    Quantity = Column(Integer)
    image = Column(String)
    CategoryId = Column(Integer)
    isNew = Column(Boolean, default=False)
    isSale = Column(Boolean, default=False)

# Create the table
Base.metadata.create_all(engine)

# Create session
Session = sessionmaker(bind=engine)
session = Session()

# Insert data from DataFrame
import pandas as pd
df = pd.read_csv('cellphones_products.csv' , encoding='ISO-8859-1')

# Convert DataFrame to list of dictionaries
data = df.to_dict(orient="records")

# Insert into database
session.bulk_insert_mappings(Product, data)
session.commit()

print("Data inserted successfully with Primary Key!")
