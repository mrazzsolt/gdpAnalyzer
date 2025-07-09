import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest

class AIAnalysis:
    def __init__(self, data):
        self.data = data
    
    def perform_kmeans_clustering(self, n_clusters=3):
        gdp_trends = self.data.pivot(index='TIME_PERIOD', columns='geo', values='OBS_VALUE')
        gdp_trends = gdp_trends.ffill().bfill()

        print(f"K-means input országok száma: {gdp_trends.shape[1]}")  
        print(f"Országok listája: {list(gdp_trends.columns)}")

        if gdp_trends.shape[1] < n_clusters:
            raise ValueError(f"Túl kevés ország maradt ({gdp_trends.shape[1]}) a {n_clusters} klaszter létrehozásához.")


        gdp_trends = gdp_trends.T

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        gdp_trends['Cluster'] = kmeans.fit_predict(gdp_trends)

        plt.figure(figsize=(12, 6))
        sns.scatterplot(x=gdp_trends.index, y=gdp_trends.mean(axis=1), hue=gdp_trends['Cluster'], palette='viridis', s=100)
        plt.xlabel('Ország')
        plt.ylabel('Átlagos GDP érték')
        plt.title(f'GDP klaszterezés ({n_clusters} klaszter)')
        plt.xticks(rotation=90)
        plt.legend(title="Klaszter")
        plt.show()

    
    def detect_anomalies(self):
        gdp_trends = self.data.pivot(index='TIME_PERIOD', columns='geo', values='OBS_VALUE')
        gdp_trends = gdp_trends.ffill().bfill()
  
        gdp_trends = gdp_trends.diff().dropna(axis=0)
        
        iso_forest = IsolationForest(contamination=0.05, random_state=42)
        anomalies = iso_forest.fit_predict(gdp_trends.T)  
        
        anomaly_countries = gdp_trends.columns[np.where(anomalies == -1)]
        
        print(f"Anomáliát mutató országok: {list(anomaly_countries)}")

        plt.figure(figsize=(12, 6))
        for country in anomaly_countries:
            plt.plot(gdp_trends.index, gdp_trends[country], marker='o', linestyle='--', label=country)
        
        plt.xlabel('Év')
        plt.ylabel('GDP változás')
        plt.title('Anomáliák a GDP trendekben')
        plt.legend()
        plt.show()
    def plot_anomalies(self, anomaly_countries):
        plt.figure(figsize=(12, 6))
        for country in anomaly_countries:
            plt.plot(self.data[self.data['geo'] == country]['TIME_PERIOD'], 
                     self.data[self.data['geo'] == country]['OBS_VALUE'], 
                     marker='o', linestyle='--', label=country)

        plt.xlabel('Év')
        plt.ylabel('GDP érték')
        plt.title('Anomáliás országok GDP változásai')
        plt.legend()
        plt.show()
    def elbow_method(self, max_clusters=10):
        from sklearn.cluster import KMeans
        from kneed import KneeLocator  # Klaszter töréspont keresése
        
        gdp_trends = self.data.pivot(index='TIME_PERIOD', columns='geo', values='OBS_VALUE')
        gdp_trends = gdp_trends.ffill().bfill().dropna(axis=1).T  # Hiányzó adatok kitöltése
        
        inertia_values = []
        cluster_range = range(1, max_clusters + 1)
    
        for k in cluster_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(gdp_trends)
            inertia_values.append(kmeans.inertia_)
    
        # Az "elbow" pont kiszámítása
        knee_locator = KneeLocator(cluster_range, inertia_values, curve="convex", direction="decreasing")
        optimal_clusters = knee_locator.elbow  # Itt található a töréspont
    
        # Elbow-módszer grafikon kirajzolása
        plt.figure(figsize=(8, 5))
        plt.plot(cluster_range, inertia_values, marker='o', linestyle='--', color='b', label="Inertia")
        plt.axvline(x=optimal_clusters, color='r', linestyle='--', label=f'Optimális klaszter: {optimal_clusters}')
        plt.xlabel('Klaszterek száma')
        plt.ylabel('Inertia érték')
        plt.title('Elbow-módszer: Optimális klaszterszám keresése')
        plt.xticks(cluster_range)
        plt.legend()
        plt.grid(True)
        plt.show()
        
        print(f"Az optimális klaszterszám: {optimal_clusters}")
        return optimal_clusters  # Visszaadjuk az értéket
