import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import linregress
import plotly.express as px
from datetime import datetime

class GDPDataAnalyzer:
    def __init__(self, file_path, year_offset=2):
        self.file_path = file_path
        self.year_offset = year_offset
        self.year = datetime.now().year - self.year_offset
        self.data = self.load_data()
        self.gdp_data = self.filter_gdp_data()

    def load_data(self):
        return pd.read_csv(self.file_path, low_memory=False)

    def filter_gdp_data(self):
        gdp_data = self.data[(self.data['na_item'] == 'B1GQ') & 
                             (self.data['unit'] == 'CP_MEUR') & 
                             (self.data['TIME_PERIOD'] == self.year)]
        gdp_data = gdp_data.dropna(subset=['OBS_VALUE'])
        gdp_data = gdp_data[~gdp_data['geo'].isin(['EU27_2020', 'EA', 'EA12', 'EA19', 'EA20'])]
        return gdp_data

    def get_top10_gdp_countries(self):
        top10_gdp_countries = self.gdp_data.sort_values(by='OBS_VALUE', ascending=False).head(10)
        print(f"\nTop 10 GDP ország {self.year}-ban:")
        print(top10_gdp_countries[['geo', 'OBS_VALUE']])
        return top10_gdp_countries

    def prepare_data_for_analysis(self):
        #self.data = self.data.drop_duplicates(subset=['TIME_PERIOD', 'geo'])
        self.data = self.data[(self.data['na_item'] == 'B1GQ') & (self.data['unit'] == 'CP_MEUR')]
        self.data = self.data[~self.data['geo'].isin(['EU27_2020', 'EA', 'EA12', 'EA19', 'EA20'])]
        self.data['TIME_PERIOD'] = pd.to_datetime(self.data['TIME_PERIOD'], format='%Y')
        self.data = self.data.dropna(subset=['OBS_VALUE'])
        self.data = self.data.dropna(subset=['TIME_PERIOD'])
        self.data = self.data[self.data['TIME_PERIOD'].dt.year >= 2000]

    def plot_heatmap(self, top5_countries):
        pivot_data = self.data[self.data['geo'].isin(top5_countries)].pivot(index='TIME_PERIOD', columns='geo', values='OBS_VALUE')
        correlation_matrix = pivot_data.corr() #korrelációs mátrix készítés, minnél közelebb van az 1.0-hoz annál egységesebben mozognak.
        plt.figure(figsize=(10, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('GDP korreláció - Top 5 ország')
        plt.show()

    def plot_boxplot(self, top10_gdp_countries): #Minnél kisebb a doboz annál stabilabb a GDP. A dobozon kívüli pontok szokatlan GDP-értékeket, ha sok van ingadozó gazdaságra utal.
        boxplot_data = self.data[(self.data['geo'].isin(top10_gdp_countries['geo'])) & (self.data['unit'] == 'CP_MEUR')]
        plt.figure(figsize=(12, 8))
        sns.boxplot(x='geo', y='OBS_VALUE', data=boxplot_data)
        plt.title('GDP eloszlás - Top 10 ország')
        plt.xlabel('Ország')
        plt.ylabel('GDP (CLV05_MEUR)')
        plt.xticks(rotation=90)
        plt.show()

    def plot_time_series(self, countries):  
        plt.figure(figsize=(14, 8))
        gdp_values = [self.data[(self.data['geo'] == country) & (self.data['unit'] == 'CP_MEUR')]['OBS_VALUE'] for country in countries]
        min_gdp = min([values.min() for values in gdp_values])
        max_gdp = max([values.max() for values in gdp_values])
        for country in countries:
            country_data = self.data[(self.data['geo'] == country) & (self.data['unit'] == 'CP_MEUR')]
            plt.plot(country_data['TIME_PERIOD'].dt.year, country_data['OBS_VALUE'], label=country, marker='o')

        years = country_data['TIME_PERIOD'].dt.year
        plt.xticks(years, rotation=45)
        y_ticks = range(int(min_gdp // 500000 * 500000), int(max_gdp) + 500000, 500000)
        plt.yticks(y_ticks)
        plt.title('GDP trendek')
        plt.xlabel('Év')
        plt.ylabel('GDP (Millió euró)')
        plt.legend()
        plt.grid(True)
        plt.show()

    def analyze_hungary_gdp_trend(self):
        hungary_gdp = self.data[(self.data['geo'] == 'HU') & (self.data['unit'] == 'CP_MEUR')]
        years = hungary_gdp['TIME_PERIOD'].dt.year
        gdp_values = hungary_gdp['OBS_VALUE']
        slope, intercept, r_value, p_value, std_err = linregress(years, gdp_values)
        plt.figure(figsize=(10, 6))
        plt.plot(years, gdp_values, label='GDP', marker='o')
        plt.plot(years, intercept + slope * years, label='Trendvonal', linestyle='--')
        plt.title('Magyarország GDP trendje')
        plt.xlabel('Év')
        plt.ylabel('GDP (Millió euró)')
        plt.legend()
        plt.grid(True)
        plt.xticks(years, rotation=45)
        plt.show()
        print(f"Trend meredeksége: {slope:.2f}, R^2 érték: {r_value**2:.2f}")
        hungary_gdp.loc[:, 'GDP_growth_rate'] = hungary_gdp['OBS_VALUE'].pct_change() * 100
        return hungary_gdp

    def plot_interactive_time_series(self):
        fig = px.line(self.data[self.data['unit'] == 'CP_MEUR'],x='TIME_PERIOD', y='OBS_VALUE', 
                      color='geo',title='GDP trendek országok szerint',labels={'OBS_VALUE': 'GDP (CP_MEUR)', 'TIME_PERIOD': 'Év'})
        fig.update_layout(xaxis=dict(tickmode='array',tickvals=self.data['TIME_PERIOD'].dt.year.unique(),
                                     ticktext=[str(year) for year in self.data['TIME_PERIOD'].dt.year.unique()]))
        fig.show()

    def plot_hungary_gdp_growth_rate(self, hungary_gdp):
        hungary_gdp = hungary_gdp[hungary_gdp['TIME_PERIOD'].dt.year >= 2000]
        plt.figure(figsize=(10, 6))
        plt.plot(hungary_gdp['TIME_PERIOD'].dt.year, hungary_gdp['GDP_growth_rate'], label='GDP növekedési ráta', marker='o')
        plt.title('Magyarország GDP növekedési rátája')
        plt.xlabel('Év')
        plt.ylabel('Növekedési ráta (%)')
        plt.legend()
        plt.grid(True)
        plt.xticks(hungary_gdp['TIME_PERIOD'].dt.year, rotation=45)
        plt.show()


file_path = 'eurostat_gdp_data.csv'
year_offset = 2
analyzer = GDPDataAnalyzer(file_path, year_offset=year_offset)
top10_gdp_countries = analyzer.get_top10_gdp_countries()
analyzer.prepare_data_for_analysis()
#analyzer.plot_heatmap(top10_gdp_countries.head(5)['geo'])
#analyzer.plot_boxplot(top10_gdp_countries)
analyzer.plot_time_series(['HU', 'AT', 'DE', 'FR'])
#hungary_gdp = analyzer.analyze_hungary_gdp_trend()
#analyzer.plot_interactive_time_series()
#analyzer.plot_hungary_gdp_growth_rate(hungary_gdp)