# ============================================================
# RECOVERAI — RECOVERY DECISION ENGINE
# ============================================================

def decide_recovery_action(transaction, prediction):
    """
    Decide the best recovery action based on:
    - ML recovery probability
    - transaction amount
    - retry history
    - customer history
    - failure reason
    """

    probability = prediction["recovery_probability"]
    amount = transaction["amount"]
    retry_count = transaction["retry_count"]
    previous_successful = transaction["previous_successful_payments"]
    previous_failed = transaction["previous_failed_payments"]
    failure_reason = transaction["failure_reason"]

    # --------------------------------------------------------
    # SAFETY RULE 1 — Too many retries
    # --------------------------------------------------------

    if retry_count >= 3:
        return {
            "action": "HUMAN_REVIEW",
            "priority": "LOW",
            "reason": "Maximum retry limit reached.",
            "confidence": 0.95
        }

    # --------------------------------------------------------
    # SAFETY RULE 2 — High-value transaction
    # --------------------------------------------------------

    if amount >= 5000 and probability < 0.60:
        return {
            "action": "HUMAN_REVIEW",
            "priority": "HIGH",
            "reason": "High-value payment with uncertain recovery probability.",
            "confidence": 0.88
        }

    # --------------------------------------------------------
    # RULE 3 — High recovery probability
    # --------------------------------------------------------

    if probability >= 0.75 and retry_count == 0:
        return {
            "action": "AUTO_RETRY",
            "priority": "HIGH",
            "reason": "High probability of successful recovery.",
            "confidence": probability
        }

    # --------------------------------------------------------
    # RULE 4 — Payment method / technical issues
    # --------------------------------------------------------

    if failure_reason in [
        "Timeout",
        "Technical Error",
        "Bank Declined"
    ] and probability >= 0.50:

        return {
            "action": "ALTERNATE_PAYMENT",
            "priority": "MEDIUM",
            "reason": "Payment failure may be resolved using an alternate payment method.",
            "confidence": probability
        }

    # --------------------------------------------------------
    # RULE 5 — Loyal customer
    # --------------------------------------------------------

    if previous_successful >= 5 and probability >= 0.50:
        return {
            "action": "PAYMENT_REMINDER",
            "priority": "MEDIUM",
            "reason": "Customer has a strong successful payment history.",
            "confidence": probability
        }

    # --------------------------------------------------------
    # RULE 6 — Medium recovery probability
    # --------------------------------------------------------

    if probability >= 0.50:
        return {
            "action": "PAYMENT_REMINDER",
            "priority": "MEDIUM",
            "reason": "Moderate recovery probability; reminder is a low-risk intervention.",
            "confidence": probability
        }

    # --------------------------------------------------------
    # RULE 7 — Low probability
    # --------------------------------------------------------

    return {
        "action": "HUMAN_REVIEW",
        "priority": "LOW",
        "reason": "Low probability of automated recovery.",
        "confidence": 1 - probability
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

    test_prediction = {
        "recovery_probability": 0.5774
    }

    decision = decide_recovery_action(
        test_transaction,
        test_prediction
    )

    print("=" * 60)
    print("RECOVERAI — DECISION ENGINE")
    print("=" * 60)

    print(f"Transaction ID : {test_transaction['transaction_id']}")
    print(f"Amount         : ₹{test_transaction['amount']:,.2f}")
    print(
        f"Recovery Prob. : "
        f"{test_prediction['recovery_probability'] * 100:.2f}%"
    )

    print()
    print(f"Action         : {decision['action']}")
    print(f"Priority       : {decision['priority']}")
    print(f"Confidence     : {decision['confidence'] * 100:.2f}%")
    print(f"Reason         : {decision['reason']}")

    print("=" * 60)