import pandas as pd
import sqlalchemy
import os
from datetime import datetime

# --- CONFIGURATION ---
DB_NAME = 'fraud_system.db'

# AUTO-LOCATE THE CSV FILE
# This tells Python: "Look for the CSV in the same folder as this script file"
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'fraud_data.csv')

def extract_data():
    print(f"[{datetime.now()}] Loading Transaction Stream...")
    try:
        # Use the auto-detected path
        df = pd.read_csv(csv_path)
        print(f" -> Ingested {len(df)} transactions.")
        return df
    except FileNotFoundError:
        print(f"Error: Could not find file at: {csv_path}")
        print("Make sure 'fraud_data.csv' is in the same folder as this script!")
        return None

def transform_data(df):
    print(f"[{datetime.now()}] Analyzing Risk Factors...")
    
    # 1. STANDARDIZE COLUMN NAMES
    # This turns "Transaction_Date" into "transaction_date" and "Fraud_Flag" into "fraud_flag"
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # 2. DATE PARSING (Fixed for your dataset)
    # We look for 'transaction_date' now
    if 'transaction_date' in df.columns:
        # errors='coerce' means "if you find a weird date, just make it NaT (Not a Time) instead of crashing"
        df['trans_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    else:
        print("WARNING: 'transaction_date' column missing. Using current time.")
        df['trans_date'] = datetime.now()

    # 3. FEATURE ENGINEERING: "Hour of Day"
    # If the date parsing failed (NaT), fill it with 0 (midnight) so the script continues
    df['trans_date'] = df['trans_date'].fillna(datetime.now())
    df['hour'] = df['trans_date'].dt.hour
    
    # 4. RISK SCORING
    def calculate_risk(row):
        score = 0
        # Your column is 'amount' (after lowercasing)
        amount = row.get('amount', 0)
        
        # Rule 1: High Amount
        if amount > 1000: score += 50
        
        # Rule 2: Weird Hours (11 PM to 4 AM)
        if 23 <= row['hour'] or row['hour'] <= 4: score += 20
        
        # Rule 3: Online Transactions
        # Your column is 'merchant_category'
        category = str(row.get('merchant_category', ''))
        if 'net' in category or 'online' in category: score += 30
        
        return score

    print(" -> Calculating Risk Scores...")
    df['risk_score'] = df.apply(calculate_risk, axis=1)
    
    # 5. ROUTING (Fixed for your dataset)
    # We look for 'fraud_flag' (1 = Fraud, 0 = Safe)
    # Note: Sometimes 'fraud_flag' is a string "1" or integer 1. We check for both just in case.
    is_fraud = (df['fraud_flag'] == 1) | (df['fraud_flag'] == '1')
    is_high_risk = df['risk_score'] > 40
    
    high_risk_df = df[is_high_risk | is_fraud].copy()
    low_risk_df = df[~(is_high_risk | is_fraud)].copy()
    
    print(f" -> Routing Complete: {len(high_risk_df)} Suspicious, {len(low_risk_df)} Safe.")
    
    return low_risk_df, high_risk_df

def load_data(low_risk, high_risk):
    print(f"[{datetime.now()}] Saving to Secure Database...")
    engine = sqlalchemy.create_engine(f'sqlite:///{DB_NAME}')
    
    low_risk.to_sql('transactions_safe', engine, if_exists='replace', index=False)
    high_risk.to_sql('transactions_suspicious', engine, if_exists='replace', index=False)
    
    print(" -> Data successfully routed and saved.")

if __name__ == "__main__":
    raw = extract_data()
    if raw is not None:
        safe, suspicious = transform_data(raw)
        load_data(safe, suspicious)