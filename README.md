\# 🛢️ US Crude Oil Inventory Automated Pipeline \& Power BI Dashboard



An end-to-end data engineering and business intelligence project that automates the ingestion of U.S. weekly crude oil inventory data and visualizes market trends, historical comparisons, and key inventory shocks.



\---



\## 🚀 Architecture \& Workflow

1\. \*\*Data Ingestion (AWS Lambda):\*\* A Python-based serverless function fetches real-time and historical weekly crude oil inventory data directly from the official \*\*U.S. Energy Information Administration (EIA) API\*\*.

2\. \*\*Storage \& Processing:\*\* Raw data is stored and structured for analysis.

3\. \*\*Visualization \& BI (Power BI):\*\* Connects to the processed dataset to deliver an executive-level grid-style dashboard featuring dynamic KPIs, multi-year trend analysis, and automated date hierarchies.



\---



\## 📊 Key Dashboard Features

\* \*\*Executive KPI Cards:\*\* Tracks Current Inventory, Weekly Changes, 4-Week Moving Average, and Year-to-Date (YTD) Net Changes dynamically.

\* \*\*Historical Trend Analysis:\*\* A 3-year multi-period line chart displaying long-term inventory trajectories.

\* \*\*Monthly Aggregations:\*\* Clean column charts categorized by chronological month abbreviations (`Jan` to `Dec`) to monitor seasonal inventory builds and draws.

\* \*\*Top Market Shocks:\*\* Filtered data views highlighting the most significant weekly inventory changes.

\* \*\*Interactive Slicers:\*\* Instant year-filtering (`2024`, `2025`, `2026`) that updates all visuals synchronously.



\---



\## 🛠️ Tech Stack

\* \*\*Language:\*\* Python (`boto3`, `requests`, Pandas)

\* \*\*Cloud \& Automation:\*\* AWS Lambda, Amazon S3

\* \*\*Business Intelligence:\*\* Microsoft Power BI, DAX, Power Query

\* \*\*Version Control:\*\* Git \& GitHub



\---



\## 📁 Repository Structure

```text

us-crude-oil-pipeline/

│

├── lambda_function.py      # Python script for AWS Lambda (EIA API integration)

├── dashboard.pbix          # Power BI Executive Dashboard file

└── README.md               # Project documentation

