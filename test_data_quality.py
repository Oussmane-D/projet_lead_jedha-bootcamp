from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import pandas as pd

def test_data_quality():
    # Charger les données de référence et actuelles
    reference_data = pd.read_csv('data/churn_dataset_reference.csv')
    current_data = pd.read_csv('data/churn_dataset_current.csv')

    # Création d'un tableau de bord pour détecter la dérive des données
    dashboard = Dashboard(tabs=[DataDriftTab()])
    dashboard.calculate(reference_data, current_data)
    
    # Sauvegarder le rapport
    dashboard.save("reports/data_drift_report.html")
