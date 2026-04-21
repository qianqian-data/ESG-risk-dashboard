# ESG Risk Dashboard — S&P 500 (Sustainalytics-Inspired Model)

## Business Context
ESG rating agencies like Sustainalytics charge significant fees for their proprietary scores. This project replicates the core logic of their weighted risk model using publicly available data, achieving **88.6% match rate** with official ratings across 430 S&P 500 companies.

## Live Dashboard
🔗 [View Interactive Dashboard on Tableau Public](https://public.tableau.com/app/profile/qianqian.z7250/viz/ESGRiskDashboardSP500Sustainalytics-InspiredModel/ESGRiskDashboard#1)

## Project Structure
| File | Description |
|------|-------------|
| `week1_clean.py` | Data cleaning and preprocessing |
| `week2_model.py` | Weighted ESG scoring model |
| `esg_scored.csv` | Final scored dataset (430 companies) |

## Methodology
**Step 1 — Data Cleaning**
- Source: [S&P 500 ESG Risk Ratings](https://www.kaggle.com/datasets/pritish509/s-and-p-500-esg-risk-ratings) via Kaggle
- Removed 73 companies with missing E/S/G scores
- Final dataset: 430 companies across 11 sectors

**Step 2 — Weighted Scoring Model**
Inspired by Sustainalytics' risk framework, different industries carry different ESG risk drivers:

| Sector | E Weight | S Weight | G Weight |
|--------|----------|----------|----------|
| Energy | 50% | 25% | 25% |
| Financial Services | 20% | 30% | 50% |
| Healthcare | 20% | 50% | 30% |
| Technology | 25% | 45% | 30% |

**Step 3 — Risk Classification**
Used percentile-based thresholds calibrated to match Sustainalytics' official distribution:
- Negligible / Low / Medium / High / Severe

## Key Findings
- ✅ Model achieved **88.6% match rate** with official Sustainalytics ratings
- 🔴 **Energy sector** carries the highest average ESG risk (avg score: 12.5)
- 🟢 **Real Estate** has the lowest ESG risk exposure (avg score: 4.5)
- ⚠️ Our model flags **Energy companies as more severe** than official ratings — reflecting a conservative view on carbon transition risk

## Tools
`Python` `pandas` `Tableau` `CSV`
