# ============================================================
# RECOVERAI — AUDIT LOGGER
# ============================================================

import csv
import os
from datetime import datetime


AUDIT_FILE = "data/audit_log.csv"


def log_action(transaction, prediction, decision, execution):
    """
    Store every AI recovery decision and execution
    in an audit log.
    """

    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)

    file_exists = os.path.exists(AUDIT_FILE)

    record = {
        "timestamp": datetime.now().isoformat(),
        "transaction_id": transaction["transaction_id"],
        "amount": transaction["amount"],
        "recovery_probability": round(
            prediction["recovery_probability"], 4
        ),
        "expected_recovery_amount": round(
            prediction["expected_recovery_amount"], 2
        ),
        "risk_level": prediction["risk_level"],
        "ai_action": decision["action"],
        "priority": decision["priority"],
        "confidence": round(
            decision["confidence"], 4
        ),
        "reason": decision["reason"],
        "execution_status": execution["status"],
        "reference_id": execution["reference_id"],
    }

    with open(
        AUDIT_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=record.keys()
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(record)

    return record


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    transaction = {
        "transaction_id": "TXN_TEST_001",
        "amount": 2500,
    }

    prediction = {
        "recovery_probability": 0.5774,
        "expected_recovery_amount": 1443.45,
        "risk_level": "MEDIUM",
    }

    decision = {
        "action": "ALTERNATE_PAYMENT",
        "priority": "MEDIUM",
        "confidence": 0.5774,
        "reason": (
            "Payment failure may be resolved using "
            "an alternate payment method."
        ),
    }

    execution = {
        "status": "EXECUTED",
        "reference_id": "ALT_4823FAD6",
    }

    record = log_action(
        transaction,
        prediction,
        decision,
        execution
    )

    print("=" * 65)
    print("RECOVERAI — AUDIT LOGGER")
    print("=" * 65)

    for key, value in record.items():
        print(f"{key:<30}: {value}")

    print()
    print(f"Audit log saved to: {AUDIT_FILE}")

    print("=" * 65)