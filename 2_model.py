import pandas as pd

# ============================================================
# STEP 1 : Load cleaned data
# ============================================================
# Use the cleaned data from Week 1, not the raw CSV
df = pd.read_csv(r'D:\ESG Portfolio\esg_clean.csv')
print(f"✅ Data loaded：{df.shape[0]} companies\n")

# ============================================================
# STEP 2 : Define industry weights
# ============================================================
# Core business logic: ESG risk drivers vary by industry
#
# Energy        → E weight highest (carbon emissions, pollution)
# Financial     → G weight highest (governance & compliance)
# Healthcare    → S weight highest (patient safety, pricing)
# Technology    → S weight higher (data privacy, diversity)
# Real Estate   → G weight higher (transparency)
# Others use equal weights

industry_weights = {
    'Energy':                 {'E': 0.50, 'S': 0.25, 'G': 0.25},
    'Financial Services':     {'E': 0.20, 'S': 0.30, 'G': 0.50},
    'Healthcare':             {'E': 0.20, 'S': 0.50, 'G': 0.30},
    'Technology':             {'E': 0.25, 'S': 0.45, 'G': 0.30},
    'Real Estate':            {'E': 0.25, 'S': 0.30, 'G': 0.45},
    'Utilities':              {'E': 0.50, 'S': 0.25, 'G': 0.25},
    'Basic Materials':        {'E': 0.45, 'S': 0.30, 'G': 0.25},
    'Industrials':            {'E': 0.40, 'S': 0.30, 'G': 0.30},
    'Consumer Cyclical':      {'E': 0.30, 'S': 0.40, 'G': 0.30},
    'Consumer Defensive':     {'E': 0.30, 'S': 0.40, 'G': 0.30},
    'Communication Services': {'E': 0.25, 'S': 0.45, 'G': 0.30},
}

# ============================================================
# STEP 3 : Calculate weighted ESG risk score
# ============================================================
def calculate_weighted_score(row):
    # Get weights for this company's sector
    # If sector not in dictionary, use equal weights as default
    weights = industry_weights.get(
        row['sector'],
        {'E': 0.33, 'S': 0.33, 'G': 0.34}  # default equal weights
    )
    
    # Weighted sum formula
    score = (row['E_score'] * weights['E'] +
             row['S_score'] * weights['S'] +
             row['G_score'] * weights['G'])
    
    return round(score, 2)

# Apply function to each row, creating a new column
df['weighted_risk_score'] = df.apply(calculate_weighted_score, axis=1)
print("✅ Weighted risk scores calculated")

# ============================================================
# STEP 4 :Risk level classification
# ============================================================
# Replicating Sustainalytics' 5-tier risk classification
# Negligible < 10 ≤ Low < 20 ≤ Medium < 30 ≤ High < 40 ≤ Severe

# STEP 4b : Explore score distribution first
# ============================================================
# Before classifying, understand the actual score distribution
print("=== Weighted score statistics ===")
print(df['weighted_risk_score'].describe())

# Use percentiles to set thresholds, matching Sustainalytics' distribution
# Official: Negligible≈1%,  Low≈44%,  Medium≈43%,  High≈12%, Severe≈1%
negligible_threshold = df['weighted_risk_score'].quantile(0.01)
low_threshold        = df['weighted_risk_score'].quantile(0.45)
medium_threshold     = df['weighted_risk_score'].quantile(0.88)
severe_threshold     = df['weighted_risk_score'].quantile(0.99)

print(f"\n Calibrated thresholds：")
print(f"  Negligible : < {negligible_threshold:.2f}")
print(f"  Low        : < {low_threshold:.2f}")
print(f"  Medium     : < {medium_threshold:.2f}")
print(f"  High       : < {severe_threshold:.2f}")
print(f"  Severe     : >= {severe_threshold:.2f}")
# ============================================================
def risk_category(score):
    if score < negligible_threshold:  return 'Negligible'
    elif score < low_threshold:       return 'Low'
    elif score < medium_threshold:    return 'Medium'
    elif score < severe_threshold:    return 'High'
    else:                             return 'Severe' 
df['model_risk_level'] = df['weighted_risk_score'].apply(risk_category)
print("✅ Risk levels assigned\n")
# ============================================================
# STEP 5 : Model validation
# ============================================================
# Key step: compare our model output vs official Sustainalytics ratings
# I validated my model against the official ratings"

print("=== Our model distribution ===")
print(df['model_risk_level'].value_counts())

print("\n=== Official distribution (for comparison) ===")
print(df['official_risk_level'].value_counts())

# Calculate how often our classification matches the official one
match = (df['model_risk_level'] == df['official_risk_level']).sum()
total = len(df)
accuracy = round(match / total * 100, 1)
print(f"\n✅ Match rate with official ratings：{accuracy}%")
print("（Note: differences expected, real model uses more dimensions）")

# ============================================================
# STEP 6 :Companies with biggest divergence
# ============================================================
# Find companies where we scored much higher than official
# These can be flagged as "worth watching" in the dashboard

print("\n=== Top 10 highest risk companies ===")
top10 = df[['name', 'sector', 'weighted_risk_score', 
            'model_risk_level', 'official_risk_level']]\
          .sort_values('weighted_risk_score', ascending=False)\
          .head(10)
print(top10.to_string(index=False))

# ============================================================
# STEP 7 : Save final scored data
# ============================================================
df.to_csv(r'D:\ESG Portfolio\esg_scored.csv', index=False)
print("\n✅ Scored data saved as：esg_scored.csv")
print("Next step：Tableau Dashboard")