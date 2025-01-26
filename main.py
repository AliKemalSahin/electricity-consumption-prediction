from fastapi import FastAPI
from typing import Optional
import numpy as np
import pandas as pd
import joblib
from statsmodels.tsa.arima.model import ARIMA
from scipy.stats import ks_2samp

app = FastAPI()

df = pd.read_csv("dataset.csv")
df["timestamp"] = pd.to_datetime(df["Tarih"] + " " + df["Saat"], format="%d.%m.%Y %H:%M")
df = df[["timestamp", "Tuketim"]]
df["Tuketim"] = df["Tuketim"].apply(lambda x: float(str(x).replace(".", "").replace(",", ".")))

class ARIMAPipeline:
    def __init__(self, order, steps, save_path):
        self.order = order
        self.steps = steps
        self.save_path = save_path
        self.model_fit = None

    def load(self):
        self.model_fit = joblib.load(self.save_path)

    def forecast(self, steps):
        if self.model_fit is None:
            raise RuntimeError("Model yüklenmedi.")
        return self.model_fit.forecast(steps=steps)

def load_arima_pipelines():
    pipeline_5d = ARIMAPipeline(order=(10, 1, 5), steps=5, save_path="saved_models/arima_5days.pkl")
    pipeline_24h = ARIMAPipeline(order=(10, 1, 5), steps=24, save_path="saved_models/arima_24hours.pkl")
    pipeline_5d.load()
    pipeline_24h.load()
    return pipeline_5d, pipeline_24h

arima_pipeline_5d, arima_pipeline_24h = load_arima_pipelines()

@app.get("/forecast5d")
def forecast5d(date: str = "2022-05-23", days: int = 5):
    try:
        forecast = arima_pipeline_5d.forecast(steps=days)
        dates = pd.date_range(start=date, periods=days, freq="D")
        return {"start_date": date, "predictions": dict(zip(dates.strftime('%Y-%m-%d'), forecast))}
    except ValueError as e:
        return {"error": str(e)}

@app.get("/forecast24h")
def forecast24h(date: str = "2022-05-23", hours: int = 24):
    try:
        forecast = arima_pipeline_24h.forecast(steps=hours)
        times = pd.date_range(start=date, periods=hours, freq="H")
        return {"start_date": date, "predictions": dict(zip(times.strftime('%Y-%m-%d %H:%M:%S'), forecast))}
    except ValueError as e:
        return {"error": str(e)}

# DRIFT
@app.get("/drift/electricity")
def detect_electricity_drift():
    recent_train_data = df[df["timestamp"] >= (df["timestamp"].max() - pd.Timedelta(days=5))]
    forecast = arima_pipeline_5d.forecast(steps=len(recent_train_data))
    drift_result = detect_drift(recent_train_data["Tuketim"], forecast)

    return {
        "drift_result": drift_result["drift_result"],
        "statistic": drift_result["statistic"],
        "pvalue": drift_result["pvalue"],
        "data1_mean": drift_result["data1_mean"],
        "data2_mean": drift_result["data2_mean"]
    }

def detect_drift(data1, data2):
    ks_result = ks_2samp(data1, data2)
    return {
        "drift_result": "Drift exists" if ks_result.pvalue < 0.05 else "No drift",
        "statistic": ks_result.statistic,
        "pvalue": ks_result.pvalue,
        "data1_mean": np.mean(data1),
        "data2_mean": np.mean(data2)
    }
