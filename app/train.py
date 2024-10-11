import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def train_model():
    # Charger le dataset de churn
    data = pd.read_csv('data/churn_dataset.csv')

    # Préparation des données
    X = data.drop('churn', axis=1)
    y = data['churn']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Modèle simple avec RandomForest
    model = RandomForestClassifier()

    # Suivi avec MLflow
    mlflow.start_run()
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    
    # Log des métriques
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(model, "model")

    mlflow.end_run()
