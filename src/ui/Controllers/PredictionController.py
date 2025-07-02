import numpy as np
import pandas as pd


class PredictionController:
    def __init__(self, center_panel):
        self.center_panel = center_panel

    def to_dataframe(self, history: list[dict]) -> pd.DataFrame:
        df = pd.DataFrame(history)
        df["date"] = pd.to_datetime(df["date"])
        df["source"] = "real"
        df = df.groupby("date").agg({"price": "mean", "source": "first"}).reset_index()
        df.set_index("date", inplace=True)
        return df

    def extend_to_target(self, df: pd.DataFrame, target_date=None) -> pd.DataFrame:
        if target_date is None:
            target_date = pd.Timestamp("2025-07-01")
        else:
            target_date = pd.to_datetime(target_date)

        full_index = pd.date_range(start=df.index.min(), end=target_date, freq='D')
        df = df.reindex(full_index)
        df["price"] = df["price"].interpolate(method='linear')
        df["source"] = df["source"].fillna("interpolated")
        return df

    def get_predictions_until_target(self, df: pd.DataFrame, last_real_date: pd.Timestamp, target_date: pd.Timestamp) -> pd.DataFrame:
        horizon = (target_date - last_real_date).days

        if horizon <= 0:
            print("❌ Aucun jour à prédire.")
            return pd.DataFrame()

        future_dates = pd.date_range(start=last_real_date + pd.Timedelta(days=1), periods=horizon)
        preds = pd.DataFrame(index=future_dates)

        # Naïve
        preds["Naive"] = df["price"].dropna().iloc[-1]

        # Moyenne
        preds["Mean"] = df["price"].mean()

        # Saisonnalité
        seasonal_date = last_real_date - pd.DateOffset(months=1)
        if seasonal_date in df.index:
            val = df.loc[seasonal_date, "price"]
        else:
            td = df.index - seasonal_date
            closest = df.iloc[np.abs(td).argsort()[:1]]
            val = closest["price"].values[0]
        preds["Seasonal"] = val

        # Moyenne mobile
        window = df[df.index >= last_real_date - pd.Timedelta(days=30)]
        rolling_val = window["price"].mean() if not window.empty else df["price"].mean()
        preds["Rolling"] = rolling_val

        return preds

    def update_graph(self, ad: dict, history_data: list[dict]):
        df = self.to_dataframe(history_data)
        last_real_date = df.index.max()
        target_date = pd.Timestamp("2025-07-01")

        df = self.extend_to_target(df, target_date)
        preds = self.get_predictions_until_target(df, last_real_date, target_date)

        df_real = df[df["source"] == "real"]
        df_interp = df[df["source"] == "interpolated"]

        self.center_panel.update_graph(
            df_real=df_real,
            df_interp=df_interp,
            ad_price=ad["price"],
            ad_date=last_real_date,
            predictions=preds,
            title=f"{ad['type']} - {ad['id']} | {ad['region']}",
            force_xlim=target_date
        )
