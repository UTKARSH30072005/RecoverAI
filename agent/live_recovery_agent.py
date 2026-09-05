import sys
from pathlib import Path

# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ============================================================
# IMPORT EXISTING AI COMPONENTS
# ============================================================

from ml.predict import predict_recovery
from agent.decision_engine import decide_recovery_action
from agent.action_executor import execute_recovery_action
from agent.audit_logger import log_action


# ============================================================
# PROCESS ONE LIVE PAYMENT
# ============================================================

def process_live_payment(transaction):

    print("\n")
    print("=" * 70)
    print("              RECOVERAI — AI RECOVERY AGENT")
    print("=" * 70)

    # --------------------------------------------------------
    # PAYMENT
    # --------------------------------------------------------

    print("\n[1] PAYMENT EVENT")
    print("-" * 50)

    print(f"Transaction ID : {transaction['transaction_id']}")
    print(f"Customer ID    : {transaction['customer_id']}")
    print(f"Amount         : ₹{transaction['amount']:,.2f}")
    print(f"Payment Method : {transaction['payment_method']}")
    print(f"Failure Reason : {transaction['failure_reason']}")

    # --------------------------------------------------------
    # AI PREDICTION
    # --------------------------------------------------------

    prediction = predict_recovery(transaction)

    print("\n[2] AI ANALYSIS")
    print("-" * 50)

    print(
        f"Recovery Probability : "
        f"{prediction['recovery_probability'] * 100:.2f}%"
    )

    print(
        f"Expected Recovery    : "
        f"₹{prediction['expected_recovery_amount']:,.2f}"
    )

    print(
        f"Risk Level           : "
        f"{prediction['risk_level']}"
    )

    # --------------------------------------------------------
    # DECISION
    # --------------------------------------------------------

    decision = decide_recovery_action(
        transaction,
        prediction
    )

    print("\n[3] AI DECISION")
    print("-" * 50)

    print(
        f"Recommended Action : "
        f"{decision['action']}"
    )

    print(
        f"Priority           : "
        f"{decision['priority']}"
    )

    print(
        f"Confidence         : "
        f"{decision['confidence'] * 100:.2f}%"
    )

    print(
        f"Reason             : "
        f"{decision['reason']}"
    )

    # --------------------------------------------------------
    # ACTION EXECUTION
    # --------------------------------------------------------

    execution = execute_recovery_action(
        transaction,
        decision
    )

    print("\n[4] RECOVERY ACTION")
    print("-" * 50)

    print(
        f"Status       : "
        f"{execution['status']}"
    )

    print(
        f"Message      : "
        f"{execution['message']}"
    )

    print(
        f"Reference ID : "
        f"{execution['reference_id']}"
    )

    if "recovery_link" in execution:

        print(
            f"Recovery Link: "
            f"{execution['recovery_link']}"
        )

    # --------------------------------------------------------
    # AUDIT
    # --------------------------------------------------------

    audit = log_action(
        transaction,
        prediction,
        decision,
        execution
    )

    print("\n[5] AUDIT")
    print("-" * 50)

    print(
        f"Audit Status : "
        f"{audit}"
    )

    print("\n")
    print("=" * 70)
    print("              RECOVERY WORKFLOW COMPLETED")
    print("=" * 70)

    return {
        "transaction": transaction,
        "prediction": prediction,
        "decision": decision,
        "execution": execution
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_transaction = {
        "transaction_id": "LIVE_TEST_001",
        "customer_id": "CUST_TEST",
        "amount": 7500,
        "payment_method": "UPI",
        "failure_reason": "Timeout",
        "previous_successful_payments": 12,
        "previous_failed_payments": 1,
        "retry_count": 0,
        "customer_lifetime_months": 18,
        "days_since_last_payment": 5,
        "is_subscription": 1,
        "customer_lifetime_value": 45000
    }

    process_live_payment(test_transaction)