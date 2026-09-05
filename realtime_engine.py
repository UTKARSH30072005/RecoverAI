import pandas as pd
import random
import time
from datetime import datetime
from pathlib import Path
import uuid

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

PAYMENTS_FILE = DATA_DIR / "payments.csv"
LIVE_EVENTS_FILE = DATA_DIR / "live_events.csv"


# ============================================================
# LOAD EXISTING CUSTOMER DATA
# ============================================================

df = pd.read_csv(PAYMENTS_FILE)


# ============================================================
# GENERATE A REAL-TIME PAYMENT EVENT
# ============================================================

def generate_payment_event():

    row = df.sample(1).iloc[0]

    transaction_id = (
        "LIVE_"
        + datetime.now().strftime("%Y%m%d%H%M%S")
        + "_"
        + uuid.uuid4().hex[:6].upper()
    )

    event_time = datetime.now().isoformat(timespec="seconds")

    amount = round(
        random.uniform(
            max(100, row["amount"] * 0.7),
            row["amount"] * 1.3
        ),
        2
    )

    payment_method = random.choice(
        ["UPI", "Card", "NetBanking", "Wallet"]
    )

    failure_reason = random.choice(
        [
            "Timeout",
            "Insufficient Funds",
            "Card Declined",
            "Bank Declined",
            "Technical Error",
            "Authentication Failed"
        ]
    )

    event = {
        "event_time": event_time,
        "transaction_id": transaction_id,
        "customer_id": row["customer_id"],
        "amount": amount,
        "payment_method": payment_method,
        "failure_reason": failure_reason,
        "previous_successful_payments": int(
            row["previous_successful_payments"]
        ),
        "previous_failed_payments": int(
            row["previous_failed_payments"]
        ),
        "retry_count": int(
            row["retry_count"]
        ),
        "customer_lifetime_months": int(
            row["customer_lifetime_months"]
        ),
        "days_since_last_payment": int(
            row["days_since_last_payment"]
        ),
        "is_subscription": int(
            row["is_subscription"]
        ),
        "customer_lifetime_value": float(
            row["customer_lifetime_value"]
        ),
        "event_type": "PAYMENT_FAILED"
    }

    return event


# ============================================================
# SAVE LIVE EVENT
# ============================================================

def save_event(event):

    event_df = pd.DataFrame([event])

    if LIVE_EVENTS_FILE.exists():

        event_df.to_csv(
            LIVE_EVENTS_FILE,
            mode="a",
            header=False,
            index=False
        )

    else:

        event_df.to_csv(
            LIVE_EVENTS_FILE,
            index=False
        )


# ============================================================
# LIVE EVENT STREAM
# ============================================================

def start_stream(interval=5):

    print("\n")
    print("=" * 65)
    print("        RECOVERAI — LIVE PAYMENT EVENT ENGINE")
    print("=" * 65)
    print("Status : LIVE")
    print("Mode   : Synthetic Real-Time Payment Stream")
    print("Press CTRL+C to stop.")
    print("=" * 65)

    try:

        while True:

            event = generate_payment_event()

            save_event(event)

            print("\n")
            print("● NEW PAYMENT EVENT")
            print("-" * 50)
            print(f"Time            : {event['event_time']}")
            print(f"Transaction ID  : {event['transaction_id']}")
            print(f"Customer ID     : {event['customer_id']}")
            print(f"Amount          : ₹{event['amount']:,.2f}")
            print(f"Payment Method  : {event['payment_method']}")
            print(f"Failure Reason  : {event['failure_reason']}")
            print(f"Event Type      : {event['event_type']}")
            print("-" * 50)

            time.sleep(interval)

    except KeyboardInterrupt:

        print("\n")
        print("=" * 65)
        print("LIVE PAYMENT STREAM STOPPED")
        print("=" * 65)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    start_stream(interval=5)