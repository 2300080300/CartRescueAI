from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

MODEL_PATH = Path(__file__).with_name("cart_rescue_model.joblib")
NUMERIC_FEATURES = ["session_duration", "items_in_cart", "total_value"]
CATEGORICAL_FEATURES = ["device_type", "traffic_source"]
_model: Pipeline | None = None


def build_model() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", "passthrough", NUMERIC_FEATURES),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )
    classifier = RandomForestClassifier(
        n_estimators=250,
        max_depth=10,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    return Pipeline([("preprocessor", preprocessor), ("classifier", classifier)])


def training_dataset() -> tuple[pd.DataFrame, list[int]]:
    rows = [
        (0.4, 0, 0, "mobile", "social", 1), (0.7, 1, 1299, "mobile", "campaign", 1),
        (1.0, 2, 3499, "mobile", "social", 1), (1.2, 3, 8999, "mobile", "email", 1),
        (1.5, 1, 4999, "desktop", "social", 1), (1.8, 4, 12999, "mobile", "organic", 1),
        (2.0, 2, 15999, "desktop", "campaign", 1), (2.2, 5, 24999, "mobile", "social", 1),
        (2.5, 3, 29999, "desktop", "email", 1), (2.8, 6, 45999, "mobile", "organic", 1),
        (3.0, 2, 7999, "tablet", "campaign", 1), (3.4, 7, 59999, "mobile", "email", 1),
        (0.6, 0, 0, "desktop", "organic", 1), (1.1, 1, 799, "tablet", "social", 1),
        (1.7, 2, 5999, "desktop", "social", 1), (2.4, 4, 18999, "mobile", "campaign", 1),
        (3.8, 1, 999, "desktop", "organic", 0), (4.2, 2, 4999, "desktop", "organic", 0),
        (5.0, 1, 12999, "desktop", "email", 0), (6.5, 3, 19999, "desktop", "organic", 0),
        (7.2, 2, 8999, "tablet", "email", 0), (8.0, 4, 29999, "desktop", "organic", 0),
        (9.5, 5, 44999, "desktop", "email", 0), (10.0, 1, 2499, "mobile", "organic", 0),
        (11.5, 2, 15999, "desktop", "campaign", 0), (12.0, 6, 69999, "desktop", "organic", 0),
        (4.8, 3, 7999, "tablet", "organic", 0), (5.4, 5, 34999, "desktop", "social", 0),
        (6.0, 2, 11999, "mobile", "email", 0), (7.5, 4, 25999, "desktop", "email", 0),
        (8.5, 3, 21999, "tablet", "campaign", 0), (10.5, 5, 49999, "desktop", "organic", 0),
    ]
    columns = ["session_duration", "items_in_cart", "total_value", "device_type", "traffic_source"]
    frame = pd.DataFrame([row[:-1] for row in rows], columns=columns)
    return frame, [row[-1] for row in rows]


def train_and_save_model() -> Pipeline:
    features, labels = training_dataset()
    model = build_model()
    model.fit(features, labels)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model


def load_model() -> Pipeline:
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else train_and_save_model()
    return _model


def payload_to_frame(payload: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame([{
        "session_duration": payload["session_duration"],
        "items_in_cart": payload["items_in_cart"],
        "total_value": payload["total_value"],
        "device_type": payload["device_type"],
        "traffic_source": payload.get("traffic_source", payload.get("source", "direct")),
    }])


def predict_abandonment(model: Pipeline, payload: dict[str, Any]) -> float:
    return float(model.predict_proba(payload_to_frame(payload))[0][1])


def recommendation_for_probability(score: float) -> str:
    if score >= 0.7:
        return "Offer a discount or exit intent incentive to recover this cart."
    if score >= 0.4:
        return "Send a reminder email and optimize checkout messaging."
    return "Monitor the session and provide personalized product recommendations."
