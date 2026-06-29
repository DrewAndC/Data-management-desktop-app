import pandas as pd
import numpy as np
import os

def load_data(file_paths):
    dfs = []

    for fp in file_paths: 
        df = pd.read_csv(fp)

        # clean columns from all three files
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        cols = df.columns.tolist()

        if "cafe_location" in cols:
            df["segment_type"] = "cafe"

        elif "invoice_id" in cols:
            df["segment_type"] = "commercial"

        elif "order_id" in cols:
            df["segment_type"] = "domestic"

        else:
            raise ValueError(f"Unknown file structure: {fp}")

        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)
def clean_data(df):

    # standardise column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    df = df.rename(columns={
        "qty_sold": "qty",
    })

    # finds qty in columns
    qty_cols = df.loc[:, df.columns == "qty"]

    # combine all qty columns into one
    df["qty"] = qty_cols.sum(axis=1)

    # remove duplicates
    df = df.loc[:, ~df.columns.duplicated()]

    # required columns
    required_cols = ['qty', 'unit_cost', 'list_unit_price', 'date']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # ensure discount exists
    if 'discount_pct' not in df.columns:
        df['discount_pct'] = 0

    # fill missing numeric values
    for col in ['qty', 'unit_cost', 'list_unit_price', 'discount_pct']:
        if col not in df.columns:
            df[col] = 0
        df[col] = df[col].fillna(0)

        cafe_mask = df["segment_type"] == "cafe"

    # if cafe qty is all zero → treat each row as 1 sale
    if df.loc[cafe_mask, "qty"].sum() == 0:
        print("Fixing cafe qty → setting to 1 per transaction")
        df.loc[cafe_mask, "qty"] = 1

    # convert discount format
    if df['discount_pct'].max() > 1:
        df['discount_pct'] = df['discount_pct'] / 100

    # convert dates
    df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')    
    df = df.dropna(subset=['date'])

    print("\n=== CAFE RAW CHECK ===")

    cafe = df[df["segment_type"] == "cafe"]

    print(cafe[['qty', 'unit_cost', 'list_unit_price']].head(10))
    print(cafe[['qty', 'unit_cost', 'list_unit_price']].describe())
    print("\nCAFE COLUMNS:")
    print(df[df["segment_type"] == "cafe"].columns)

    return df

def process_monthly(df):

    # reset index + remove duplicate columns (safety)
    df = df.copy()
    df = df.reset_index(drop=True)
    df = df.loc[:, ~df.columns.duplicated()]

    # ensure segment consistency
    df['segment_type'] = df['segment_type'].astype(str).str.lower()

    # calculations
    df['net_unit_price'] = df['list_unit_price'] * (1 - df['discount_pct'])
    df['revenue'] = df['qty'] * df['net_unit_price']
    df['cost'] = df['qty'] * df['unit_cost']
    df['profit'] = df['revenue'] - df['cost']

    # extract month
    df['month'] = df['date'].dt.to_period('M')

    # company data
    monthly = df.groupby('month', as_index=False).agg({
        'revenue': 'sum',
        'cost': 'sum',
        'profit': 'sum'
    })

    monthly = monthly.sort_values('month').reset_index(drop=True)

    # revenue growth
    monthly['revenue_growth'] = monthly['revenue'].pct_change().fillna(0) * 100

    # segment data
    monthly_segment = df.groupby(['month', 'segment_type'], as_index=False).agg({
        'revenue': 'sum',
        'cost': 'sum',
        'profit': 'sum'
    })

    monthly_segment = monthly_segment.sort_values(['segment_type', 'month']).reset_index(drop=True)

    # customer metrics
    if 'customer_id' in df.columns:

        domestic = df[df['segment_type'] == 'domestic']
        commercial = df[df['segment_type'] == 'commercial']

        domestic_counts = domestic.groupby('month', as_index=False)['customer_id'].nunique()
        commercial_counts = commercial.groupby('month', as_index=False)['customer_id'].nunique()

        domestic_counts.rename(columns={'customer_id': 'unique_domestic_customers'}, inplace=True)
        commercial_counts.rename(columns={'customer_id': 'active_commercial_customers'}, inplace=True)

        monthly = monthly.merge(domestic_counts, on='month', how='left')
        monthly = monthly.merge(commercial_counts, on='month', how='left')

    else:
        monthly['unique_domestic_customers'] = 0
        monthly['active_commercial_customers'] = 0

    # fill missing
    monthly['unique_domestic_customers'] = monthly['unique_domestic_customers'].fillna(0)
    monthly['active_commercial_customers'] = monthly['active_commercial_customers'].fillna(0)

    # margins
    monthly['margin'] = np.where(
        monthly['revenue'] != 0,
        (monthly['profit'] / monthly['revenue']) * 100,
        0
    )

    monthly_segment['margin'] = np.where(
        monthly_segment['revenue'] != 0,
        (monthly_segment['profit'] / monthly_segment['revenue']) * 100,
        0
    )

    # give sale types kpi calculation previous and change values
    for col in ['revenue', 'cost', 'profit', 'margin']:
        monthly_segment[f"{col}_prev"] = (
            monthly_segment.groupby("segment_type")[col].shift(1)
        )
        monthly_segment[f"{col}_change"] = (
            monthly_segment[col] - monthly_segment[f"{col}_prev"]
        )

    monthly_segment = monthly_segment.fillna(0)

    # prev + change
    for col in [
        'revenue', 'cost', 'profit', 'margin',
        'unique_domestic_customers',
        'active_commercial_customers',
        'revenue_growth'
    ]:
        monthly[f"{col}_prev"] = monthly[col].shift(1)
        monthly[f"{col}_change"] = monthly[col] - monthly[f"{col}_prev"]

    monthly = monthly.fillna(0)

    # convert month to string for GUI
    monthly['month'] = monthly['month'].astype(str)
    monthly_segment['month'] = monthly_segment['month'].astype(str)

    return monthly, monthly_segment