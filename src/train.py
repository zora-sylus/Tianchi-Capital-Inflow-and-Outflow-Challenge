from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import joblib
from .feature_engineering import get_feature_columns
from .utils import MODEL_DIR


def _fit_ensemble(X_train, y_train):
    models = [
        RandomForestRegressor(n_estimators=300, max_depth=12, random_state=2026, n_jobs=-1),
        ExtraTreesRegressor(n_estimators=300, max_depth=12, random_state=2026, n_jobs=-1),
        GradientBoostingRegressor(random_state=2026, n_estimators=180, learning_rate=0.05, max_depth=3),
    ]
    for m in models:
        m.fit(X_train, y_train)
    return models


def train_models(feature_df):
    feature_cols = get_feature_columns(feature_df)
    X = feature_df[feature_cols]

    models = {}
    scores = {}
    for target in ["total_purchase_amt", "total_redeem_amt"]:
        y = feature_df[target]
        X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, shuffle=False)
        model_list = _fit_ensemble(X_train, y_train)
        pred = sum(m.predict(X_valid) for m in model_list) / len(model_list)
        mae = mean_absolute_error(y_valid, pred)
        models[target] = model_list
        scores[target] = mae

    joblib.dump({"models": models, "feature_cols": feature_cols, "scores": scores}, MODEL_DIR / "capital_flow_models.pkl")
    return models, feature_cols, scores
