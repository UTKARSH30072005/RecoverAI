# ============================================================
# RECOVERAI — COMPLETE AI REVENUE RECOVERY AGENT
# ============================================================

from ml.predict import predict_recovery
from agent.decision_engine import decide_recovery_action
from agent.action_executor import execute_recovery_action
from agent.audit_logger import log_action


def recover_payment(transaction):
    """
    Complete RecoverAI workflow.

    Prediction
        ↓
    Decision
        ↓
    Execution
        ↓
    Audit Log
    """

    # --------------------------------------------------------
    # STEP 1 — Predict recovery probability
    # --------------------------------------------------------

    prediction = predict_recovery(transaction)

    # --------------------------------------------------------
    # STEP 2 — Decide recovery action
    # --------------------------------------------------------

    decision = decide_recovery_action(
        transaction,
        prediction
    )

    # --------------------------------------------------------
    # STEP 3 — Execute recovery action
    # --------------------------------------------------------

    execution = execute_recovery_action(
        transaction,
        decision
    )

    # --------------------------------------------------------
    # STEP 4 — Create audit log
    # --------------------------------------------------------

    audit = log_action(
        transaction,
        prediction,
        decision,
        execution
    )

    # --------------------------------------------------------
    # STEP 5 — Return complete result
    # --------------------------------------------------------

    return {
        "transaction": transaction,
        "prediction": prediction,
        "decision": decision,
        "execution": execution,
        "audit": audit
    }


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    transaction = {
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

    result = recover_payment(transaction)

    prediction = result["prediction"]
    decision = result["decision"]
    execution = result["execution"]

    print("=" * 70)
    print("RECOVERAI — AUTONOMOUS REVENUE RECOVERY")
    print("=" * 70)

    print()
    print("TRANSACTION")
    print("-" * 70)

    print(f"Transaction ID : {transaction['transaction_id']}")
    print(f"Amount         : ₹{transaction['amount']:,.2f}")
    print(f"Payment Method : {transaction['payment_method']}")
    print(f"Failure Reason : {transaction['failure_reason']}")

    print()
    print("AI ANALYSIS")
    print("-" * 70)

    print(
        f"Recovery Probability : "
        f"{prediction['recovery_probability'] * 100:.2f}%"
    )

    print(
        f"Expected Recovery    : "
        f"₹{prediction['expected_recovery_amount']:,.2f}"
    )

    print(f"Risk Level           : {prediction['risk_level']}")

    print()
    print("AI DECISION")
    print("-" * 70)

    print(f"Action     : {decision['action']}")
    print(f"Priority   : {decision['priority']}")
    print(
        f"Confidence : "
        f"{decision['confidence'] * 100:.2f}%"
    )
    print(f"Reason     : {decision['reason']}")

    print()
    print("EXECUTION")
    print("-" * 70)

    print(f"Status       : {execution['status']}")
    print(f"Message      : {execution['message']}")
    print(f"Reference ID : {execution['reference_id']}")

    if "recovery_link" in execution:
        print(
            f"Recovery Link: "
            f"{execution['recovery_link']}"
        )

    print()
    print("AUDIT")
    print("-" * 70)

    print("AI decision successfully recorded.")
    print("Audit log: data/audit_log.csv")

    print()
    print("=" * 70)
    print("RECOVERY WORKFLOW COMPLETED")
    print("=" * 70)