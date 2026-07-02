import pandas as pd
from .feature_engineering import build_supervised_features, add_time_features
from .utils import OUTPUT_DIR, safe_int_array


def _make_one_day_features(history):
    temp = build_supervised_features(history)
    return temp.iloc[[-1]].copy()


def recursive_predict(daily, models, feature_cols, start_date="2014-09-01", end_date="2014-09-30"):
    history = daily.copy().sort_values("date").reset_index(drop=True)
    future_dates = pd.date_range(start_date, end_date, freq="D")
    results = []

    for d in future_dates:
        new_row = {"date": d}
        for c in history.columns:
            if c != "date" and c not in new_row:
                new_row[c] = history[c].iloc[-1]
        history = pd.concat([history, pd.DataFrame([new_row])], ignore_index=True)
        feat = _make_one_day_features(history)
        X = feat[feature_cols]

        purchase = sum(m.predict(X)[0] for m in models["total_purchase_amt"]) / len(models["total_purchase_amt"])
        redeem = sum(m.predict(X)[0] for m in models["total_redeem_amt"]) / len(models["total_redeem_amt"])

        history.loc[history.index[-1], "total_purchase_amt"] = max(purchase, 0)
        history.loc[history.index[-1], "total_redeem_amt"] = max(redeem, 0)
        results.append([int(d.strftime("%Y%m%d")), int(round(max(purchase, 0))), int(round(max(redeem, 0)))])

    sub = pd.DataFrame(results)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "submission.csv"
    sub.to_csv(out_path, index=False, header=False)
    return out_path, sub
