import numpy as np
import pandas as pd


def _date_col(df):
    for c in ["report_date", "mfd_date", "date", "day"]:
        if c in df.columns:
            return c
    raise ValueError("没有找到日期字段")


def prepare_daily_table(balance, interest=None, shibor=None):
    date_col = _date_col(balance)
    balance = balance.copy()
    balance[date_col] = pd.to_datetime(balance[date_col].astype(str), format="%Y%m%d", errors="coerce")

    daily = balance.groupby(date_col).agg(
        total_purchase_amt=("total_purchase_amt", "sum"),
        total_redeem_amt=("total_redeem_amt", "sum"),
    ).reset_index().rename(columns={date_col: "date"})

    full_dates = pd.date_range(daily["date"].min(), daily["date"].max(), freq="D")
    daily = daily.set_index("date").reindex(full_dates).rename_axis("date").reset_index()
    daily[["total_purchase_amt", "total_redeem_amt"]] = daily[["total_purchase_amt", "total_redeem_amt"]].interpolate().ffill().bfill()

    if interest is not None:
        interest = interest.copy()
        dcol = _date_col(interest)
        interest[dcol] = pd.to_datetime(interest[dcol].astype(str), format="%Y%m%d", errors="coerce")
        interest = interest.rename(columns={dcol: "date"})
        daily = daily.merge(interest, on="date", how="left")

    if shibor is not None:
        shibor = shibor.copy()
        dcol = _date_col(shibor)
        shibor[dcol] = pd.to_datetime(shibor[dcol].astype(str), format="%Y%m%d", errors="coerce")
        shibor = shibor.rename(columns={dcol: "date"})
        daily = daily.merge(shibor, on="date", how="left")

    for c in daily.columns:
        if c != "date":
            daily[c] = pd.to_numeric(daily[c], errors="coerce")
    daily = daily.ffill().bfill()
    return daily


def add_time_features(df):
    df = df.copy()
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["dayofweek"] = df["date"].dt.dayofweek
    df["dayofyear"] = df["date"].dt.dayofyear
    df["weekofyear"] = df["date"].dt.isocalendar().week.astype(int)
    df["is_weekend"] = (df["dayofweek"] >= 5).astype(int)
    df["is_month_start"] = df["date"].dt.is_month_start.astype(int)
    df["is_month_end"] = df["date"].dt.is_month_end.astype(int)
    return df


def build_supervised_features(daily):
    df = add_time_features(daily)
    targets = ["total_purchase_amt", "total_redeem_amt"]

    for target in targets:
        for lag in [1, 2, 3, 4, 5, 6, 7, 14, 21, 28, 30]:
            df[f"{target}_lag_{lag}"] = df[target].shift(lag)
        for win in [3, 7, 14, 21, 30]:
            shifted = df[target].shift(1)
            df[f"{target}_roll_mean_{win}"] = shifted.rolling(win).mean()
            df[f"{target}_roll_std_{win}"] = shifted.rolling(win).std()
            df[f"{target}_roll_min_{win}"] = shifted.rolling(win).min()
            df[f"{target}_roll_max_{win}"] = shifted.rolling(win).max()

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna().reset_index(drop=True)
    return df


def get_feature_columns(df):
    exclude = {"date", "total_purchase_amt", "total_redeem_amt"}
    return [c for c in df.columns if c not in exclude]
