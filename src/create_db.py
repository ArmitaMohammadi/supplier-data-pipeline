import sqlite3
import pandas as pd
import os


def create_database():

    supplier_feed_cleaned = pd.read_csv('../data/supplier_feed_cleaned.csv')
    product_metadata = pd.read_csv('../data/product_metadata.csv')
    db_path = '../data/parts_avatar.db'

    # Remove the existing database file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)

    # Create a new SQLite database (this will create the file)
    conn = sqlite3.connect(db_path)

    # Create supplier_feed table
    supplier_feed_cleaned.to_sql('supplier_feed', conn, if_exists='replace', index=False)

    # Create product_metadata table
    product_metadata.to_sql('product_metadata', conn, if_exists='replace', index=False)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()