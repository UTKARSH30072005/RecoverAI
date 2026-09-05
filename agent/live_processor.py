import sys
from pathlib import Path
from datetime import datetime

# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ============================================================
# IMPORT AI COMPONENTS
# ============================================================

from ml.predict import predict_recovery
from agent.decision_engine import decide_recovery_action
from agent.action_executor import execute_recovery_action
from agent.audit_logger import log_action


# ============================================================
# PROCESS TRANSACTION
# ============================================================

def analyze_transaction(transaction):

    # AI prediction
    prediction = predict_recovery(transaction)

    # AI decision
    decision = decide_recovery_action(
        transaction,
        prediction
    )

    return {
        "transaction": transaction,
        "prediction": prediction,
        "decision": decision
    }


# ============================================================
# EXECUTE TRANSACTION
# ============================================================

def execute_transaction(transaction, prediction, decision):

    execution = execute_recovery_action(
        transaction,
        decision
    )

    # Save audit log
    log_action(
        transaction,
        prediction,
        decision,
        execution
    )

    return execution