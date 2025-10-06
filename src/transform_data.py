import pandas as pd
from dateutil.parser import parse

def remove_dollar_sign(value):
    if pd.isna(value): 
        return None
    # remove $ sign and convert cost_price to float
    return round(float(str(value).replace('$', '')), 2)

def clean_stock(s):
    binary_map = {
        "low stock": 1,
        "low": 1,
        "unavailable": -1,
        "out of stock": 0
    }

    try:
        return int(s)
    except ValueError:
        # not a number, treat as text
        s_norm = str(s).strip().lower()
        return binary_map.get(s_norm, None)

def clean_date(s):
    if pd.isna(s): return s
    s = str(s).replace("\u00A0", " ").strip()
    s = s.strip('\'"“”‘’`')  # strip common quotes
    return s

def parse_date(x):
    if pd.isna(x):
        return pd.NaT

    s = str(x).strip().replace("\u00A0", " ")
    if s == "":
        return pd.NaT

    EXPLICIT_FORMATS = [
        "%Y-%m-%d", "%Y/%m/%d",
        "%m/%d/%Y", "%m/%d/%y",
        "%d/%m/%Y", "%d/%m/%y",
        "%b %d, %Y", "%B %d, %Y",
        "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%d %H:%M:%S.%f",
    ]

    for fmt in EXPLICIT_FORMATS:
        try:
            return pd.to_datetime(s, format=fmt)
        except Exception:
            continue

    # Fallback to generic parse
    try:
        return pd.to_datetime(s, errors='coerce')
    except Exception:
        return pd.NaT

def main():

    # Load data
    supplier_feed = pd.read_csv('../data/supplier_feed.csv')
    print("The data is loaded and initial data shape:", supplier_feed.shape)

    #duplicate rows
    supplier_feed = supplier_feed.drop_duplicates()
    print("After removing duplicates, data shape:", supplier_feed.shape)

    # clean cost_price
    print("Before cleaning cost_price, missing values:", supplier_feed['cost_price'].isna().sum())
    supplier_feed['cost_price'] = supplier_feed['cost_price'].apply(remove_dollar_sign)
    # fill missing cost_price with avg of the price of that product id
    supplier_feed['cost_price'] = supplier_feed['cost_price'].fillna(round(supplier_feed.groupby('part_id')['cost_price'].transform('mean'), 2))
    print("After cleaning cost_price, missing values:", supplier_feed['cost_price'].isna().sum())

    # fill missing stock_level with -1
    print("Before cleaning stock_level, missing values:", supplier_feed['stock_level'].isna().sum())
    supplier_feed.fillna({'stock_level': -1}, inplace=True)
    # fill string stock_level values with numeric equivalents
    supplier_feed["stock_level"] = supplier_feed["stock_level"].apply(clean_stock)
    print("After cleaning stock_level, missing values:", supplier_feed['stock_level'].isna().sum())

    # consistent date parsing
    supplier_feed["entry_date"] = supplier_feed["entry_date"].apply(parse_date)

    # Save cleaned data
    supplier_feed.to_csv('../data/supplier_feed_cleaned.csv', index=False)

if __name__ == "__main__":
    main()