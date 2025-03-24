import pandas as pd
from sqlalchemy import create_engine, Integer, String, Float
import chardet
# auto detect encoding 
with open('cellphones_products.csv' , 'rb') as f:
    result = chardet.detect(f.read(100000))
detected_encoding =result['encoding']
print("🕵️ Detected encoding : ",detected_encoding)


# Load the CSV
df = pd.read_csv('cellphones_products.csv' , encoding=detected_encoding)

# Convert column names to lowercase
df.columns = [c.lower() for c in df.columns] 

# Define the database connection
engine = create_engine('postgresql://postgres:123456789@localhost:5432/postgres')
try: 
    with engine.connect() as connection: 
        print("✅ >>> connection database successfull >>> ")
except Exception as e:
    print(f"⚠️ >>>  database connection fail >>> {e}")

# Define column types
from sqlalchemy.types import Integer, String, Float, Date , DECIMAL , Boolean 

dtype_mapping = {
    'Id': Integer(),
    'Name': String(255),
    'Price': Integer(),
    'Quantity' : Integer(),
    'image' : String(),
    'CategoryId' : Integer(),
    'isNew' : Boolean(), 
    'isSale' : Boolean()
}

# # Write to PostgreSQL with specific types
df.to_sql("Products", engine, if_exists='append', index=False , dtype=dtype_mapping)
