# clustering.py
import numpy as np
from sklearn.cluster import DBSCAN, OPTICS, MeanShift
from sklearn.preprocessing import StandardScaler

def perform_clustering(data):
    # Prepare the data
    coords = data[['Pinned Latitude', 'Pinned Longitude']].values
    scaler = StandardScaler()
    coords_scaled = scaler.fit_transform(coords)
    
    results = {}
    
    # DBSCAN
    dbscan = DBSCAN(eps=0.3, min_samples=5)
    dbscan_clusters = dbscan.fit_predict(coords_scaled)
    results['DBSCAN'] = dbscan_clusters.tolist()  # Convert to Python list
    
    # OPTICS
    optics = OPTICS(min_samples=5)
    optics_clusters = optics.fit_predict(coords_scaled)
    results['OPTICS'] = optics_clusters.tolist()  # Convert to Python list
    
    # Mean Shift
    ms = MeanShift(bandwidth=0.8)
    ms_clusters = ms.fit_predict(coords_scaled)
    results['MeanShift'] = ms_clusters.tolist()  # Convert to Python list
    
    return results