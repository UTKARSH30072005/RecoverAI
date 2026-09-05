import pandas as pd
import numpy as np

# Reproducibility
np.random.seed(42)

# Number of transactions
N = 10000

# -----------------------------
# Basic transaction information
# -----------------------------

transaction_id = [f"TXN{100000 + i}" for i in range(N)]
customer_id = [f"CUST{1000 + np.random.randint(1, 3001)}" for _ in range(N)]

amount = np.round(
    np.random.lognormal(mean=7.5, sigma=1.0, size=N),
    2
)

amount = np.clip(amount, 100, 100000)

payment_methods = ["UPI", "Card", "NetBanking", "Wallet"]

payment_method = np.random.choice(
    payment_methods,
    size=N,
    p=[0.50, 0.30, 0.15, 0.05]
)

failure_reasons = [
    "Timeout",
    "Insufficient Funds",
    "Card Declined",
    "Bank Declined",
    "Technical Error",
    "Authentication Failed"
]

failure_reason = np.random.choice(
    failure_reasons,
    size=N,
    p=[0.20, 0.18, 0.20, 0.15, 0.12, 0.15]
)

# -----------------------------
# Customer behaviour
# -----------------------------

previous_successful_payments = np.random.poisson(
    lam=8,
    size=N
)

previous_failed_payments = np.random.poisson(
    lam=2,
    size=N
)

retry_count = np.random.choice(
    [0, 1, 2, 3, 4],
    size=N,
    p=[0.45, 0.30, 0.15, 0.07, 0.03]
)

customer_lifetime_months = np.random.randint(
    1,
    61,
    size=N
)

days_since_last_payment = np.random.randint(
    1,
    181,
    size=N
)

is_subscription = np.random.choice(
    [0, 1],
    size=N,
    p=[0.65, 0.35]
)

# -----------------------------
# Customer value
# -----------------------------

customer_lifetime_value = np.round(
    np.random.lognormal(mean=9, sigma=1.0, size=N),
    2
)

customer_lifetime_value = np.clip(
    customer_lifetime_value,
    500,
    500000
)

# -----------------------------
# Create recovery probability
# -----------------------------

score = np.zeros(N)

# Positive factors
score += previous_successful_payments * 0.08
score += is_subscription * 0.15
score += np.minimum(customer_lifetime_months, 36) * 0.01

# Negative factors
score -= previous_failed_payments * 0.08
score -= retry_count * 0.15

# Failure reason influence
score += np.where(failure_reason == "Timeout", 0.30, 0)
score += np.where(failure_reason == "Technical Error", 0.25, 0)
score += np.where(failure_reason == "Insufficient Funds", 0.05, 0)
score -= np.where(failure_reason == "Card Declined", 0.15, 0)
score -= np.where(failure_reason == "Bank Declined", 0.10, 0)
score -= np.where(failure_reason == "Authentication Failed", 0.05, 0)

# Payment method influence
score += np.where(payment_method == "UPI", 0.08, 0)
score += np.where(payment_method == "Card", 0.02, 0)

# High-value transactions slightly harder to recover
score -= np.log1p(amount) * 0.015

# Randomness
score += np.random.normal(
    0,
    0.35,
    N
)

# Convert score to probability
recovery_probability = 1 / (1 + np.exp(-score))

# -----------------------------
# Recovery outcome
# -----------------------------

recovered = np.random.binomial(
    1,
    recovery_probability
)

# -----------------------------
# Expected recovery amount
# -----------------------------

expected_recovery_amount = np.round(
    amount * recovery_probability,
    2
)

# Actual recovered amount
actual_recovered_amount = np.where(
    recovered == 1,
    amount,
    0
)

# -----------------------------
# Create DataFrame
# -----------------------------

df = pd.DataFrame({
    "transaction_id": transaction_id,
    "customer_id": customer_id,
    "amount": amount,
    "payment_method": payment_method,
    "failure_reason": failure_reason,
    "previous_successful_payments": previous_successful_payments,
    "previous_failed_payments": previous_failed_payments,
    "retry_count": retry_count,
    "customer_lifetime_months": customer_lifetime_months,
    "days_since_last_payment": days_since_last_payment,
    "is_subscription": is_subscription,
    "customer_lifetime_value": customer_lifetime_value,
    "recovery_probability": np.round(recovery_probability, 4),
    "recovered": recovered,
    "expected_recovery_amount": expected_recovery_amount,
    "actual_recovered_amount": actual_recovered_amount
})

# Save dataset
output_path = "data/payments.csv"

df.to_csv(output_path, index=False)

print("=" * 60)
print("RecoverAI Dataset Generated Successfully!")
print("=" * 60)

print(f"Total transactions: {len(df):,}")
print(f"Total failed revenue: ₹{df['amount'].sum():,.2f}")
print(f"Recovered revenue: ₹{df['actual_recovered_amount'].sum():,.2f}")
print(
    f"Recovery rate: {df['recovered'].mean() * 100:.2f}%"
)

print("\nDataset columns:")
print(df.columns.tolist())

print("\nFirst 5 records:")
print(df.head())

print("\nDataset saved to:")
print(output_path)