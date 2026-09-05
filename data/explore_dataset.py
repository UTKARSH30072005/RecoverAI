import pandas as pd

# Load dataset
df = pd.read_csv("data/payments.csv")

print("=" * 60)
print("RECOVERAI DATASET ANALYSIS")
print("=" * 60)

# --------------------------------------------------
# 1. Dataset shape
# --------------------------------------------------

print("\n1. DATASET SIZE")
print("-" * 40)
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

# --------------------------------------------------
# 2. Column information
# --------------------------------------------------

print("\n2. COLUMN INFORMATION")
print("-" * 40)

print(df.info())

# --------------------------------------------------
# 3. Missing values
# --------------------------------------------------

print("\n3. MISSING VALUES")
print("-" * 40)

missing = df.isnull().sum()

print(missing)

# --------------------------------------------------
# 4. Duplicate transactions
# --------------------------------------------------

print("\n4. DUPLICATE TRANSACTIONS")
print("-" * 40)

duplicates = df["transaction_id"].duplicated().sum()

print(f"Duplicate transaction IDs: {duplicates}")

# --------------------------------------------------
# 5. Recovery statistics
# --------------------------------------------------

print("\n5. RECOVERY STATISTICS")
print("-" * 40)

recovery_rate = df["recovered"].mean() * 100

print(f"Recovery rate: {recovery_rate:.2f}%")

print(
    f"Failed revenue: "
    f"₹{df['amount'].sum():,.2f}"
)

print(
    f"Recovered revenue: "
    f"₹{df['actual_recovered_amount'].sum():,.2f}"
)

# --------------------------------------------------
# 6. Payment methods
# --------------------------------------------------

print("\n6. PAYMENT METHODS")
print("-" * 40)

print(
    df["payment_method"]
    .value_counts()
)

# --------------------------------------------------
# 7. Failure reasons
# --------------------------------------------------

print("\n7. FAILURE REASONS")
print("-" * 40)

print(
    df["failure_reason"]
    .value_counts()
)

# --------------------------------------------------
# 8. Recovery by failure reason
# --------------------------------------------------

print("\n8. RECOVERY RATE BY FAILURE REASON")
print("-" * 40)

failure_recovery = (
    df.groupby("failure_reason")["recovered"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

print(
    failure_recovery.round(2)
)

# --------------------------------------------------
# 9. Recovery by payment method
# --------------------------------------------------

print("\n9. RECOVERY RATE BY PAYMENT METHOD")
print("-" * 40)

method_recovery = (
    df.groupby("payment_method")["recovered"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

print(
    method_recovery.round(2)
)

# --------------------------------------------------
# 10. Numeric statistics
# --------------------------------------------------

print("\n10. NUMERIC STATISTICS")
print("-" * 40)

print(
    df.describe().round(2)
)

print("\n" + "=" * 60)
print("DATASET VALIDATION COMPLETE")
print("=" * 60)