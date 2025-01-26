import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
import joblib

# 1. Veri Yükleme ve Ön İşleme
def load_and_preprocess_data():
    df = pd.read_csv("dataset.csv")
    df["timestamp"] = pd.to_datetime(df["Tarih"] + " " + df["Saat"], format="%d.%m.%Y %H:%M")
    df = df[["timestamp", "Tuketim"]]
    df["Tuketim"] = df["Tuketim"].apply(lambda x: float(str(x).replace(".", "").replace(",", ".")))

    for lag in range(1, 121):
        df[f"Lag{lag}"] = df["Tuketim"].shift(lag)
    for lag in range(1, 25):
        df[f"Lag{lag}_24"] = df["Tuketim"].shift(lag)

    df.dropna(inplace=True)
    return df

# 2. ARIMA Modelini Pipeline İçin Sarma
class ARIMAModel(BaseEstimator, TransformerMixin):
    def __init__(self, order=(1, 1, 1), steps=5):
        self.order = order
        self.steps = steps
        self.model_fit = None

    def fit(self, X, y=None):
        self.model_fit = ARIMA(X, order=self.order).fit()
        return self

    def transform(self, X):
        forecast = self.model_fit.forecast(steps=self.steps)
        return forecast

# 3. Pipeline Tanımı
def create_pipeline(order, steps, save_path):
    return Pipeline([
        ('arima', ARIMAModel(order=order, steps=steps))
    ])

# 4. Eğitim ve Tahmin İşlemleri
def train_and_save_pipeline(df, order, steps, save_path, freq, index_col):
    pipeline = create_pipeline(order=order, steps=steps, save_path=save_path)
    X = df[[index_col, 'Tuketim']].set_index(index_col)
    forecast = pipeline.fit(X).transform(X)

    # Modeli kaydet
    joblib.dump(pipeline.named_steps['arima'].model_fit, save_path)

    # Tahmin sonuçlarını düzenle
    forecast_index = pd.date_range(start=X.index[-1], periods=steps + 1, freq=freq)[1:]
    forecast_series = pd.Series(forecast, index=forecast_index)
    return forecast_series

# 6. 5 Günlük Tahmin
forecast_5d = train_and_save_pipeline(
    df=df, 
    order=(10, 1, 5), 
    steps=5, 
    save_path="saved_models/arima_5days.pkl",
    freq="D",
    index_col="timestamp"
)

# 7. 24 Saatlik Tahmin
forecast_24h = train_and_save_pipeline(
    df=df, 
    order=(10, 1, 5), 
    steps=24, 
    save_path="saved_models/arima_24hours.pkl",
    freq="H",
    index_col="timestamp"
)