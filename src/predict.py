import os
import pandas as pd
import numpy as np


def recursive_predict(daily, models, feature_cols):
    history = daily.copy()

    history["total_purchase_amt"] = history["total_purchase_amt"].astype(float)
    history["total_redeem_amt"] = history["total_redeem_amt"].astype(float)

    pred_dates = pd.date_range("2014-09-01", "2014-09-30")
    results = []

    for date in pred_dates:
        temp = history.copy()
        row = pd.DataFrame({"report_date": [date]})
        row["dayofweek"] = date.dayofweek
        row["day"] = date.day
        row["month"] = date.month
        row["is_weekend"] = int(date.dayofweek >= 5)

        for col in feature_cols:
            if col not in row.columns:
                row[col] = 0

        X = row[feature_cols]

        purchase = float(models["total_purchase_amt"][0].predict(X)[0])
        redeem = float(models["total_redeem_amt"][0].predict(X)[0])

        purchase = max(purchase, 0)
        redeem = max(redeem, 0)

        results.append([
            int(date.strftime("%Y%m%d")),
            int(round(purchase)),
            int(round(redeem))
        ])

        new_row = pd.DataFrame({
            "report_date": [date],
            "total_purchase_amt": [float(purchase)],
            "total_redeem_amt": [float(redeem)]
        })

        history = pd.concat([history, new_row], ignore_index=True)

    sub = pd.DataFrame(results, columns=["report_date", "purchase", "redeem"])

    os.makedirs("output", exist_ok=True)
    out_path = "output/submission.csv"

    sub.to_csv(out_path, index=False, header=False)

    return out_path, sub