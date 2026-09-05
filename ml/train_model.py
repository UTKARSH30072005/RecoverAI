import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)

from xgboost import XGBClassifier


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("data/payments.csv")

print("=" * 60)
print("RECOVERAI — MODEL TRAINING")
print("=" * 60)

print(f"\nDataset size: {df.shape}")


# ============================================================
# 2. DEFINE TARGET
# ============================================================

target = "recovered"

y = df[target]


# ============================================================
# 3. SELECT FEATURES
# ============================================================

features = [
    "amount",
    "payment_method",
    "failure_reason",
    "previous_successful_payments",
    "previous_failed_payments",
    "retry_count",
    "customer_lifetime_months",
    "days_since_last_payment",
    "is_subscription",
    "customer_lifetime_value"
]

X = df[features]


print("\nFeatures used by model:")
for feature in features:
    print(f"  ✓ {feature}")


# ============================================================
# 4. IDENTIFY FEATURE TYPES
# ============================================================

categorical_features = [
    "payment_method",
    "failure_reason"
]

numeric_features = [
    "amount",
    "previous_successful_payments",
    "previous_failed_payments",
    "retry_count",
    "customer_lifetime_months",
    "days_since_last_payment",
    "is_subscription",
    "customer_lifetime_value"
]


# ============================================================
# 5. PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),
        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)


X_processed = preprocessor.fit_transform(X)


# ============================================================
# 6. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X_processed,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])


# ============================================================
# 7. TRAIN XGBOOST MODEL
# ============================================================

print("\nTraining XGBoost model...")

model = XGBClassifier(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric="logloss"
)

model.fit(
    X_train,
    y_train
)


# ============================================================
# 8. PREDICTION
# ============================================================

y_pred = model.predict(X_test)

y_probability = model.predict_proba(
    X_test
)[:, 1]


# ============================================================
# 9. MODEL EVALUATION
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred
)

recall = recall_score(
    y_test,
    y_pred
)

f1 = f1_score(
    y_test,
    y_pred
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)


print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(f"\nAccuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC-AUC   : {roc_auc:.4f}")


print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred
    )
)


# ============================================================
# 10. SAVE MODEL
# ============================================================

joblib.dump(
    model,
    "models/recovery_model.pkl"
)

joblib.dump(
    preprocessor,
    "models/preprocessor.pkl"
)


print("\n" + "=" * 60)
print("MODEL SAVED")
print("=" * 60)

print("\nModel:")
print("models/recovery_model.pkl")

print("\nPreprocessor:")
print("models/preprocessor.pkl")

print("\nTraining completed successfully!")