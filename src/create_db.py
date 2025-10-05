import sqlite3
import pandas as pd


supplier_feed_cleaned = pd.read_csv('../data/supplier_feed_cleaned.csv')
product_metadata = pd.read_csv('../data/product_metadata.csv')


conn = sqlite3.connect('../data/parts_avatar.db')

supplier_feed_cleaned.to_sql('supplier_feed', conn, if_exists='replace', index=False)
product_metadata.to_sql('product_metadata', conn, if_exists='replace', index=False)

conn.close