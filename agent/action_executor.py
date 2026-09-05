# ============================================================
# RECOVERAI — ACTION EXECUTOR
# ============================================================

from datetime import datetime
import uuid


def execute_recovery_action(transaction, decision):
    """
    Execute a SAFE simulated recovery action.

    No real payment is processed.
    """


    action = decision["action"]

    transaction_id = transaction["transaction_id"]
    amount = transaction["amount"]

    # --------------------------------------------------------
    # AUTO RETRY
    # --------------------------------------------------------

    if action == "AUTO_RETRY":

        result = {
            "status": "EXECUTED",
            "action": "AUTO_RETRY",
            "message": "Payment retry scheduled successfully.",
            "reference_id": f"RETRY_{uuid.uuid4().hex[:8].upper()}",
        }

    # --------------------------------------------------------
    # PAYMENT REMINDER
    # --------------------------------------------------------

    elif action == "PAYMENT_REMINDER":

        result = {
            "status": "EXECUTED",
            "action": "PAYMENT_REMINDER",
            "message": "Payment reminder generated successfully.",
            "reference_id": f"REM_{uuid.uuid4().hex[:8].upper()}",
        }

    # --------------------------------------------------------
    # ALTERNATE PAYMENT
    # --------------------------------------------------------

    elif action == "ALTERNATE_PAYMENT":

        recovery_link = (
            f"https://recoverai.demo/pay/"
            f"{uuid.uuid4().hex[:12]}"
        )

        result = {
            "status": "EXECUTED",
            "action": "ALTERNATE_PAYMENT",
            "message": "Alternate payment request generated.",
            "recovery_link": recovery_link,
            "reference_id": f"ALT_{uuid.uuid4().hex[:8].upper()}",
        }

    # --------------------------------------------------------
    # HUMAN REVIEW
    # --------------------------------------------------------

    elif action == "HUMAN_REVIEW":

        result = {
            "status": "ESCALATED",
            "action": "HUMAN_REVIEW",
            "message": "Transaction escalated to recovery specialist.",
            "reference_id": f"REV_{uuid.uuid4().hex[:8].upper()}",
        }

    # --------------------------------------------------------
    # UNKNOWN ACTION
    # --------------------------------------------------------

    else:

        result = {
            "status": "FAILED",
            "action": action,
            "message": "Unknown recovery action.",
            "reference_id": None,
        }

    # --------------------------------------------------------
    # Common metadata
    # --------------------------------------------------------

    result["transaction_id"] = transaction_id
    result["amount"] = amount
    result["timestamp"] = datetime.now().isoformat()

    return result


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    transaction = {
        "transaction_id": "TXN_TEST_001",
        "amount": 2500,
    }

    decision = {
        "action": "ALTERNATE_PAYMENT"
    }

    result = execute_recovery_action(
        transaction,
        decision
    )

    print("=" * 65)
    print("RECOVERAI — ACTION EXECUTOR")
    print("=" * 65)

    print(f"Transaction ID : {result['transaction_id']}")
    print(f"Amount         : ₹{result['amount']:,.2f}")
    print(f"Action         : {result['action']}")
    print(f"Status         : {result['status']}")
    print(f"Message        : {result['message']}")

    if "recovery_link" in result:
        print(f"Recovery Link  : {result['recovery_link']}")

    print(f"Reference ID   : {result['reference_id']}")
    print(f"Timestamp      : {result['timestamp']}")

    print("=" * 65)