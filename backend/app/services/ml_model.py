import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from xgboost import XGBClassifier


def build_model() -> Pipeline:
    numeric_features = ["session_duration", "items_in_cart", "total_value"]
    categorical_features = ["device_type", "source"]

    categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ],
        remainder="drop",
    )

    model = XGBClassifier(use_label_encoder=False, eval_metric="logloss", verbosity=0)
    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", model)])
    return pipeline


def train_sample_model() -> Pipeline:
    X = pd.DataFrame([
        [2.5, 1, 30.0, "desktop", "organic"],
        [0.8, 4, 180.0, "mobile", "email"],
        [5.1, 2, 85.0, "desktop", "social"],
        [1.2, 0, 0.0, "mobile", "campaign"],
    ], columns=["session_duration", "items_in_cart", "total_value", "device_type", "source"])
    y = [0, 1, 0, 1]

    model = build_model()
    model.fit(X, y)
    return model


def predict_abandonment(model: Pipeline, payload: dict) -> float:
    sample = pd.DataFrame([{
        "session_duration": payload["session_duration"],
        "items_in_cart": payload["items_in_cart"],
        "total_value": payload["total_value"],
        "device_type": payload["device_type"],
        "source": payload["source"],
    }])
    probability = model.predict_proba(sample)[0][1]
    return float(probability)


def recommendation_for_probability(score: float) -> str:
    if score >= 0.7:
        return "Offer a discount or exit intent incentive to recover this cart."
    if score >= 0.4:
        return "Send a reminder email and optimize checkout messaging."
    return "Monitor the session and provide personalized product recommendations."
