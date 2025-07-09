# GDP ANALYZER

**GDP Analyzer** is a Python-based GDP data analysis and visualization tool designed to process Eurostat data. It uses a combination of `pandas`, `matplotlib`, `seaborn`, `plotly`, and AI-based techniques (clustering and anomaly detection) to explore and visualize European GDP trends.

---

## Project Overview

- **Source:** Eurostat GDP dataset in CSV format  
- **Main Objective:** Analyze GDP trends, visualize key insights, and apply basic AI for clustering and anomaly detection  
- **Data Scope:** Focused on GDP in current year minus two (`year_offset=2`), but this can be adjusted  

---

## Features

### 1. Top 10 GDP Countries

Displays the top 10 European countries by GDP (current year - offset).

---

### 2. Correlation Heatmap

Heatmap based on the GDP of the top 5 countries.

- Shows the correlation between GDP trends: values closer to `1.0` indicate stronger synchronization.

---

### 3. Boxplot: GDP Stability

Visualizes GDP distribution of the top 10 countries.

- Narrow boxes suggest stable GDP values  
- Outliers indicate abnormal GDP fluctuations or economic instability

---

### 4. Time Series Plot

Line plots showing GDP evolution for selected countries over time.

- Only includes years shared across all selected countries to ensure consistency

---

### 5. Hungary’s GDP Trend

Linear regression trend line applied to Hungary’s GDP data.

---

### 6. Hungary's GDP Growth Rate

Calculates year-over-year GDP growth rate.

- Visualized in a separate line graph

---

### 7. Interactive Time Series Plot (Plotly)

Interactive GDP visualization across all countries.

- Uses `plotly.express` for web-based display

---

### 8. AI-Based Clustering & Anomaly Detection

- **K-Means Clustering:** Groups countries into economic clusters  
- **Elbow Method:** Determines optimal number of clusters  
- **Anomaly Detection:** Uses `IsolationForest` to detect unusual GDP changes  
- **Anomaly Visualization:** Highlights GDP trends of anomalous countries

---

## Setup & Usage

```bash
1. Install dependencies

pip install -r requirements.txt

2. Add your GDP data
python getData.py
This downloads the latest GDP data from the Eurostat website in CSV format.

3. Run the analysis
python dataAnalysis.py