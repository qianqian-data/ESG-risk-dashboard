import pandas as pd

# ============================================================
# STEP 1 : Load Data
# ============================================================
df = pd.read_csv(r'D:\ESG Portfolio\SP 500 ESG Risk Ratings.csv')

print("✅ Data loaded successfully")
print(f"Raw data：{df.shape[0]} rows，{df.shape[1]} columns\n")

# ============================================================
# STEP 2 : Keep only relevant columns
# ============================================================
# From 15 columns, select the 8 columns needed for our ESG scoring model
cols_needed = [
    'Symbol', 'Name', 'Sector',
    'Total ESG Risk score',
    'Environment Risk Score',
    'Social Risk Score',
    'Governance Risk Score',
    'ESG Risk Level'
]

df = df[cols_needed]
print("✅ Core columns selected")

# ============================================================
# STEP 3 : Rename columns
# ============================================================
# Rename to short lowercase names for easier coding later
df = df.rename(columns={
    'Total ESG Risk score'   : 'total_esg',
    'Environment Risk Score' : 'E_score',    # Environment dimension
    'Social Risk Score'      : 'S_score',    # Social dimension
    'Governance Risk Score'  : 'G_score',    # Governance dimension
    'ESG Risk Level'         : 'official_risk_level',  # Official risk level
    'Sector'                 : 'sector',     # Industry sector
    'Symbol'                 : 'symbol',     #  Stock ticker
    'Name'                   : 'name'        # Company name
})
print("✅ Columns renamed\n")

# ============================================================
# STEP 4 : Check and handle missing values
# ============================================================
print("=== Missing values per column ===")
print(df.isnull().sum())

# Drop rows where any of E/S/G scores are missing
# Reason: if any dimension is missing, our weighted model cannot compute a score
df = df.dropna(subset=['E_score', 'S_score', 'G_score', 'total_esg'])
print(f"\n✅ Companies remaining after cleaning：{df.shape[0]} \n")

# ============================================================
# STEP 5 : Check sector distribution
# ============================================================
# Important: later we will assign different weights per sector
# We need the exact sector names to match our weights dictionary
print("=== Sector distribution ===")
print(df['sector'].value_counts())

# ============================================================
# STEP 6 : Check official risk level distribution
# ============================================================
# Sustainalytics classifies ESG risk into 5 levels
# We will replicate this classification logic later
print("\n=== Official risk level distribution ===")
print(df['official_risk_level'].value_counts())

# ============================================================
# STEP 7 : Save cleaned data
# ============================================================
# Save as a new file, never overwrite the raw data (best practice)
df.to_csv(r'D:\ESG Portfolio\esg_clean.csv', index=False)
print("\n✅Cleaned data saved as：esg_clean.csv")

# ============================================================
# STEP 8 : Preview final dataframe
# ============================================================
print("\n=== Preview first 5 rows ===")
print(df.head())