import pandas as pd
import joblib


# ============================================================
# RECOVERAI — RECOVERY PREDICTION ENGINE
# ============================================================

MODEL_PATH = "models/recovery_model.pkl"
PREPROCESSOR_PATH = "models/preprocessor.pkl"


# Load trained model and preprocessor
model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)


FEATURES = [
    "amount",
    "payment_method",
    "failure_reason",
    "previous_successful_payments",
    "previous_failed_payments",
    "retry_count",
    "customer_lifetime_months",
    "days_since_last_payment",
    "is_subscription",
    "customer_lifetime_value",
]


def predict_recovery(transaction):
    """
    Predict recovery probability for a failed payment.
    """

    # Convert transaction into DataFrame
    df = pd.DataFrame([transaction])

    # Keep only model features
    X = df[FEATURES]

    # Apply preprocessing
    X_processed = preprocessor.transform(X)

    # Predict probability
    probability = model.predict_proba(X_processed)[0][1]

    # Expected recoverable revenue
    expected_recovery = transaction["amount"] * probability

    # Risk classification
    if probability >= 0.75:
        risk_level = "HIGH"
    elif probability >= 0.50:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "transaction_id": transaction.get("transaction_id", "UNKNOWN"),
        "amount": transaction["amount"],
        "recovery_probability": probability,
        "expected_recovery_amount": expected_recovery,
        "risk_level": risk_level,
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_transaction = {
        "transaction_id": "TXN_TEST_001",
        "amount": 2500,
        "payment_method": "UPI",
        "failure_reason": "Timeout",
        "previous_successful_payments": 12,
        "previous_failed_payments": 1,
        "retry_count": 0,
        "customer_lifetime_months": 18,
        "days_since_last_payment": 5,
        "is_subscription": 1,
        "customer_lifetime_value": 45000,
    }

    result = predict_recovery(test_transaction)

    print("=" * 60)
    print("RECOVERAI — RECOVERY PREDICTION")
    print("=" * 60)

    print(f"Transaction ID       : {result['transaction_id']}")
    print(f"Amount                : ₹{result['amount']:,.2f}")
    print(
        f"Recovery Probability : "
        f"{result['recovery_probability'] * 100:.2f}%"
    )
    print(
        f"Expected Recovery    : "
        f"₹{result['expected_recovery_amount']:,.2f}"
    )
    print(f"Risk Level            : {result['risk_level']}")

    print("=" * 60)