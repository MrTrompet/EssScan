# ml_model.py
import xgboost as xgb
import pandas as pd
from config import feature_columns
from ta.trend import SMAIndicator
from ta.volatility import BollingerBands

# Modelo XGBoost simplificado
MODEL = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=3,
    learning_rate=0.05,
    random_state=42
)

def add_extra_features(data):
    """
    Agrega las features requeridas: SMA larga y Bandas de Bollinger.
    """
    data = data.copy()
    data['sma_long'] = SMAIndicator(data['close'], window=25).sma_indicator()
    bb = BollingerBands(data['close'], window=20, window_dev=2)
    data['bb_low'] = bb.bollinger_lband()
    data['bb_medium'] = bb.bollinger_mavg()
    data['bb_high'] = bb.bollinger_hband()
    return data

def train_ml_model(data):
    """
    Entrena el modelo ML con datos históricos.
    """
    data = add_extra_features(data)
    features = data[feature_columns].pct_change().dropna()
    target = (features['close'] > 0).astype(int)
    MODEL.fit(features, target)

def predict_cross_strength(data):
    """
    Retorna la probabilidad (score) de una señal fuerte usando el modelo ML.
    """
    data = add_extra_features(data)
    features = data[feature_columns].pct_change().dropna().iloc[-1:][feature_columns]
    prob = MODEL.predict_proba(features)[0]  # [prob_0, prob_1]
    return prob[1]
