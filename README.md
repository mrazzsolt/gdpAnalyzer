# gdpAnalyzer
This repository contains a script I used to practice downloading data via an API and analyzing the retrieved dataset.

By running getData.py, the latest GDP data from the Eurostat website is downloaded in CSV format. Then, executing dataAnalysis.py generates various charts and outputs.

By default, the script displays the top 10 countries by GDP for current_year - 2, but this can be adjusted using the year_offset parameter.

The first interactive chart is a heatmap visualizing the top 5 GDP countries in Europe. It includes a correlation matrix, where values closer to 1.0 indicate stronger synchronization in GDP trends.

The second chart is a boxplot, which provides insights into GDP stability. A smaller box indicates a more stable GDP, while outliers outside the box represent unusual GDP values. A high number of outliers suggests an unstable economy.

The third chart is a line graph displaying the GDP trends of four countries by default. The parameters can be expanded or modified, requiring country codes that are present in the CSV file.

In the fourth step, Hungary’s GDP is analyzed, showing year-over-year changes along with a trend line created using linear regression.

The fifth step opens an interactive chart in a web browser, created as a practice exercise with Plotly. Currently, it includes all countries and requires further development to improve its clarity and presentation.

The last chart presents Hungary’s GDP growth rate, allowing for an analysis of its economic expansion over time.
