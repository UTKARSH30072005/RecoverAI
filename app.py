
import json
import uuid
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

from agent.live_processor import analyze_transaction, execute_transaction
from payment_gateway import create_payment_order, get_key_id


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RecoverAI | AI Revenue Recovery",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "payments.csv"
AUDIT_PATH = BASE_DIR / "data" / "audit_log.csv"


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-weight: 800 !important;
    }

    .stButton > button {
        min-height: 42px;
        border-radius: 9px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD DATA
# ============================================================

if not DATA_PATH.exists():
    st.error(f"❌ payments.csv not found at:\n\n{DATA_PATH}")
    st.stop()

try:
    df = pd.read_csv(DATA_PATH)
except Exception as exc:
    st.error(f"❌ Could not load payments.csv: {exc}")
    st.stop()


REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
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
    "recovery_probability",
    "recovered",
    "expected_recovery_amount",
    "actual_recovered_amount",
]

missing_columns = [c for c in REQUIRED_COLUMNS if c not in df.columns]

if missing_columns:
    st.error(
        "❌ Missing columns in payments.csv:\n\n"
        + "\n".join(f"- {c}" for c in missing_columns)
    )
    st.stop()


NUMERIC_COLUMNS = [
    "amount",
    "previous_successful_payments",
    "previous_failed_payments",
    "retry_count",
    "customer_lifetime_months",
    "days_since_last_payment",
    "is_subscription",
    "customer_lifetime_value",
    "recovery_probability",
    "recovered",
    "expected_recovery_amount",
    "actual_recovered_amount",
]

for column in NUMERIC_COLUMNS:
    df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

df["recovered"] = df["recovered"].astype(int)


# ============================================================
# HELPERS
# ============================================================

def format_rupees(value):
    try:
        return f"₹{float(value):,.2f}"
    except Exception:
        return "₹0.00"


def format_percent(value):
    try:
        return f"{float(value):.1f}%"
    except Exception:
        return "0.0%"


def generate_live_payment():
    row = df.sample(1).iloc[0]

    return {
        "transaction_id": (
            "LIVE_"
            + datetime.now().strftime("%H%M%S")
            + "_"
            + uuid.uuid4().hex[:6].upper()
        ),
        "customer_id": str(row["customer_id"]),
        "amount": round(
            max(100, float(row["amount"]) * np.random.uniform(0.85, 1.15)),
            2,
        ),
        "payment_method": str(row["payment_method"]),
        "failure_reason": str(row["failure_reason"]),
        "previous_successful_payments": int(row["previous_successful_payments"]),
        "previous_failed_payments": int(row["previous_failed_payments"]),
        "retry_count": int(row["retry_count"]),
        "customer_lifetime_months": int(row["customer_lifetime_months"]),
        "days_since_last_payment": int(row["days_since_last_payment"]),
        "is_subscription": int(row["is_subscription"]),
        "customer_lifetime_value": float(row["customer_lifetime_value"]),
    }


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "live_transaction": None,
    "live_analysis": None,
    "execution_result": None,
    "razorpay_order": None,
}

for key, default in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ============================================================
# DASHBOARD METRICS
# ============================================================

total_transactions = len(df)
revenue_at_risk = float(df["amount"].sum())
expected_recovery = float(df["expected_recovery_amount"].sum())
actual_recovery = float(df["actual_recovered_amount"].sum())
recovered_transactions = int(df["recovered"].sum())

recovery_rate = (
    recovered_transactions / total_transactions * 100
    if total_transactions
    else 0
)

average_probability = float(df["recovery_probability"].mean() * 100)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("# 💳 RecoverAI")
    st.caption("Autonomous AI Revenue Recovery")
    st.markdown("---")

    selected_page = st.radio(
        "Navigation",
        [
            "⚡ Live Command Center",
            "📊 Dashboard",
            "🎯 Recovery Opportunities",
            "💳 Payments",
            "👤 Customer Intelligence",
            "📈 Analytics",
            "📜 Audit Logs",
        ],
    )

    st.markdown("---")
    st.markdown("### System Status")
    st.success("AI Engine Online")
    st.success("ML Model Loaded")
    st.success("Decision Engine Online")
    st.success("Audit System Active")
    st.success("Razorpay Test Mode Ready")


# ============================================================
# LIVE COMMAND CENTER
# ============================================================

if selected_page == "⚡ Live Command Center":

    st.title("⚡ Live Command Center")
    st.caption("Detect → Predict → Decide → Recover → Audit")

    # --------------------------------------------------------
    # PAYMENT CHECKOUT HEADER
    # Native Streamlit only - no HTML here.
    # --------------------------------------------------------

    st.markdown("---")
    st.header("💳 Continue to Payment")
    st.write(
        "Create a Razorpay Test Mode order and open the secure checkout."
    )

    st.warning(
        "🟠 Razorpay Test Mode: no real money will be charged."
    )

    # --------------------------------------------------------
    # PAYMENT AMOUNT
    # --------------------------------------------------------

    st.subheader("💰 Payment Details")

    payment_amount = st.number_input(
        "Payment Amount (₹)",
        min_value=10.0,
        max_value=100000.0,
        value=100.0,
        step=100.0,
        key="payment_amount",
    )

    if st.button(
        "💳 CREATE RAZORPAY TEST ORDER",
        use_container_width=True,
        key="create_razorpay_order",
    ):
        try:
            receipt_id = "recoverai_" + uuid.uuid4().hex[:10]

            order = create_payment_order(
                amount=payment_amount,
                receipt_id=receipt_id,
            )

            st.session_state.razorpay_order = order
            st.success("✅ Razorpay Test Mode order created successfully.")

        except Exception as exc:
            st.error(f"❌ Razorpay order creation failed: {exc}")

    # --------------------------------------------------------
    # ORDER + CUSTOMER + SUMMARY
    # Native Streamlit only.
    # --------------------------------------------------------

    if st.session_state.razorpay_order is not None:

        order = st.session_state.razorpay_order
        order_amount = float(order["amount"]) / 100

        st.markdown("---")
        st.subheader("📋 Order Information")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Amount", f"₹{order_amount:,.2f}")

        with c2:
            st.metric("Currency", str(order["currency"]))

        with c3:
            st.metric("Status", str(order["status"]).upper())

        with c4:
            st.metric("Environment", "TEST MODE")

        st.write("**Razorpay Order ID**")
        st.code(str(order["id"]), language="text")

        st.markdown("---")
        st.subheader("👤 Customer Information")

        customer_col1, customer_col2 = st.columns(2)

        with customer_col1:
            checkout_name = st.text_input(
                "Customer Name",
                value="RecoverAI Customer",
                key="checkout_name",
            )

        with customer_col2:
            checkout_email = st.text_input(
                "Email Address",
                value="customer@recoverai.demo",
                key="checkout_email",
            )

        checkout_phone = st.text_input(
            "Mobile Number",
            value="9999999999",
            max_chars=10,
            key="checkout_phone",
        )

        st.markdown("---")
        st.subheader("💰 Payment Summary")

        summary_col1, summary_col2 = st.columns(2)

        with summary_col1:
            st.write("**Product**")
            st.write("RecoverAI Payment Recovery")
            st.write("**Payment Gateway**")
            st.write("Razorpay")
            st.write("**Environment**")
            st.write("Test Mode")
            st.write("**Customer**")
            st.write(checkout_name)

        with summary_col2:
            st.metric("Total Payable", f"₹{order_amount:,.2f}")
            st.write("🔒 Secure Razorpay Checkout")
            st.write("UPI • Cards • Net Banking • Wallets")

        st.info(
            "🔒 RecoverAI does not store card, UPI, or banking credentials. "
            "This demonstration uses Razorpay Test Mode."
        )

        # ----------------------------------------------------
        # RAZORPAY CHECKOUT
        #
        # This is the ONLY HTML block in the payment section.
        # ----------------------------------------------------

        safe_name = str(checkout_name)
        safe_email = str(checkout_email)
        safe_phone = (
            str(checkout_phone)
            .replace(" ", "")
            .replace("-", "")
        )

        razorpay_key = str(get_key_id())
        razorpay_order_id = str(order["id"])
        razorpay_amount = int(order["amount"])
        razorpay_currency = str(order["currency"])

        checkout_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<script src="https://checkout.razorpay.com/v1/checkout.js"></script>

<style>
html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    min-height: 560px;
    background: #ffffff;
    font-family: Arial, Helvetica, sans-serif;
}

body {
    padding: 12px;
    box-sizing: border-box;
}

.checkout-card {
    width: 100%;
    max-width: 760px;
    margin: 0 auto;
    padding: 26px;
    box-sizing: border-box;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    background: #ffffff;
}

.title {
    color: #0f172a;
    font-size: 24px;
    font-weight: 800;
    text-align: center;
}

.subtitle {
    color: #64748b;
    font-size: 14px;
    text-align: center;
    margin-top: 6px;
    margin-bottom: 24px;
}

.customer-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 22px;
}

.row {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    padding: 9px 0;
}

.label {
    color: #64748b;
    font-size: 14px;
}

.value {
    color: #0f172a;
    font-size: 14px;
    font-weight: 650;
    text-align: right;
    word-break: break-word;
}

.amount-box {
    text-align: center;
    border-top: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
    padding: 24px;
    margin-bottom: 24px;
}

.amount-label {
    color: #64748b;
    font-size: 14px;
}

.amount {
    color: #0f172a;
    font-size: 38px;
    font-weight: 800;
    margin-top: 7px;
}

.pay-button {
    width: 100%;
    border: 0;
    border-radius: 10px;
    padding: 17px;
    background: #2563eb;
    color: #ffffff;
    font-size: 17px;
    font-weight: 800;
    cursor: pointer;
}

.pay-button:hover {
    background: #1d4ed8;
}

.security {
    text-align: center;
    color: #16a34a;
    font-size: 14px;
    font-weight: 650;
    margin-top: 15px;
}

.test-mode {
    text-align: center;
    margin-top: 14px;
    padding: 10px;
    border-radius: 8px;
    background: #fff7ed;
    color: #c2410c;
    font-size: 13px;
    font-weight: 700;
}
</style>
</head>

<body>

<div class="checkout-card">

    <div class="title">💳 RecoverAI Secure Checkout</div>

    <div class="subtitle">
        Secure payment powered by Razorpay
    </div>

    <div class="customer-box">

        <div class="row">
            <span class="label">Customer</span>
            <span class="value" id="customer-name"></span>
        </div>

        <div class="row">
            <span class="label">Email</span>
            <span class="value" id="customer-email"></span>
        </div>

        <div class="row">
            <span class="label">Mobile</span>
            <span class="value" id="customer-phone"></span>
        </div>

        <div class="row">
            <span class="label">Order ID</span>
            <span class="value" id="order-id"></span>
        </div>

    </div>

    <div class="amount-box">

        <div class="amount-label">
            Total Payable
        </div>

        <div class="amount" id="payment-amount"></div>

    </div>

    <button class="pay-button" onclick="openRazorpay()">
        🔐 PAY NOW WITH RAZORPAY
    </button>

    <div class="security">
        🔒 Secure Razorpay Checkout
    </div>

    <div class="test-mode">
        🟠 RAZORPAY TEST MODE — NO REAL MONEY
    </div>

</div>

<script>

const customerName = __CUSTOMER_NAME__;
const customerEmail = __CUSTOMER_EMAIL__;
const customerPhone = __CUSTOMER_PHONE__;
const orderId = __ORDER_ID__;
const razorpayKey = __RAZORPAY_KEY__;
const paymentAmount = __PAYMENT_AMOUNT__;
const paymentCurrency = __PAYMENT_CURRENCY__;

document.getElementById("customer-name").textContent = customerName;
document.getElementById("customer-email").textContent = customerEmail;
document.getElementById("customer-phone").textContent = customerPhone;
document.getElementById("order-id").textContent = orderId;

document.getElementById("payment-amount").textContent =
    "₹" +
    (paymentAmount / 100).toLocaleString("en-IN", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });

function openRazorpay() {

    const options = {
        key: razorpayKey,
        amount: paymentAmount,
        currency: paymentCurrency,
        name: "RecoverAI",
        description: "AI Revenue Recovery Payment",
        order_id: orderId,

        prefill: {
            name: customerName,
            email: customerEmail,
            contact: customerPhone
        },

        notes: {
            platform: "RecoverAI",
            environment: "Test Mode"
        },

        theme: {
            color: "#2563eb"
        },

        modal: {
            confirm_close: true,
            escape: true
        },

        handler: function(response) {

            alert(
                "Payment Successful!\\n\\n" +
                "Payment ID: " +
                response.razorpay_payment_id
            );
        }
    };

    const razorpay = new Razorpay(options);

    razorpay.on(
        "payment.failed",
        function(response) {

            alert(
                "Payment Failed\\n\\n" +
                response.error.description
            );
        }
    );

    razorpay.open();
}

</script>

</body>
</html>
"""

        checkout_html = checkout_html.replace(
            "__CUSTOMER_NAME__",
            json.dumps(safe_name),
        )

        checkout_html = checkout_html.replace(
            "__CUSTOMER_EMAIL__",
            json.dumps(safe_email),
        )

        checkout_html = checkout_html.replace(
            "__CUSTOMER_PHONE__",
            json.dumps(safe_phone),
        )

        checkout_html = checkout_html.replace(
            "__ORDER_ID__",
            json.dumps(razorpay_order_id),
        )

        checkout_html = checkout_html.replace(
            "__RAZORPAY_KEY__",
            json.dumps(razorpay_key),
        )

        checkout_html = checkout_html.replace(
            "__PAYMENT_AMOUNT__",
            str(razorpay_amount),
        )

        checkout_html = checkout_html.replace(
            "__PAYMENT_CURRENCY__",
            json.dumps(razorpay_currency),
        )

        st.markdown("---")
        st.subheader("🔐 Secure Razorpay Checkout")

        components.html(
            checkout_html,
            height=720,
            scrolling=True,
        )

    # --------------------------------------------------------
    # RECOVERAI LIVE AI SYSTEM
    # --------------------------------------------------------

    st.markdown("---")
    st.header("🤖 RecoverAI Autonomous Agent")
    st.write(
        "Every failed payment is analyzed by the ML model, "
        "then the decision engine selects a bounded recovery action."
    )

    control_col1, control_col2 = st.columns(2)

    with control_col1:
        generate_payment = st.button(
            "⚡ GENERATE LIVE PAYMENT",
            use_container_width=True,
            key="generate_live_payment",
        )

    with control_col2:
        reset_system = st.button(
            "↻ RESET",
            use_container_width=True,
            key="reset_live_system",
        )

    if reset_system:
        st.session_state.live_transaction = None
        st.session_state.live_analysis = None
        st.session_state.execution_result = None
        st.session_state.razorpay_order = None
        st.rerun()

    if generate_payment:
        st.session_state.live_transaction = generate_live_payment()
        st.session_state.live_analysis = None
        st.session_state.execution_result = None

    if st.session_state.live_transaction is None:
        st.info(
            "Click **GENERATE LIVE PAYMENT** to simulate a new failed payment event."
        )

    else:

        transaction = st.session_state.live_transaction

        st.header("🔴 Payment Failure Detected")

        e1, e2, e3, e4 = st.columns(4)

        with e1:
            st.metric(
                "Transaction ID",
                transaction["transaction_id"],
            )

        with e2:
            st.metric(
                "Customer ID",
                transaction["customer_id"],
            )

        with e3:
            st.metric(
                "Amount",
                format_rupees(transaction["amount"]),
            )

        with e4:
            st.metric(
                "Payment Method",
                transaction["payment_method"],
            )

        st.warning(
            f"Failure Reason: {transaction['failure_reason']}"
        )

        if st.session_state.live_analysis is None:
            try:
                with st.spinner("🤖 AI agent analyzing payment..."):
                    st.session_state.live_analysis = analyze_transaction(
                        transaction
                    )
            except Exception as exc:
                st.error(f"❌ AI analysis failed: {exc}")
                st.stop()

        analysis = st.session_state.live_analysis
        prediction = analysis["prediction"]
        decision = analysis["decision"]

        st.markdown("---")
        st.header("🧠 AI Recovery Prediction")

        p1, p2, p3 = st.columns(3)

        with p1:
            st.metric(
                "Recovery Probability",
                format_percent(
                    prediction["recovery_probability"] * 100
                ),
            )

        with p2:
            st.metric(
                "Expected Recovery",
                format_rupees(
                    prediction["expected_recovery_amount"]
                ),
            )

        with p3:
            st.metric(
                "Risk Level",
                str(prediction["risk_level"]),
            )

        st.header("👤 Customer Intelligence")

        ci1, ci2, ci3, ci4 = st.columns(4)

        with ci1:
            st.metric(
                "Successful Payments",
                transaction["previous_successful_payments"],
            )

        with ci2:
            st.metric(
                "Previous Failures",
                transaction["previous_failed_payments"],
            )

        with ci3:
            st.metric(
                "Customer Lifetime",
                f"{transaction['customer_lifetime_months']} months",
            )

        with ci4:
            st.metric(
                "Customer Lifetime Value",
                format_rupees(
                    transaction["customer_lifetime_value"]
                ),
            )

        st.header("🤖 AI Recommendation")

        st.success(
            f"Recommended Action: **{decision['action']}**"
        )

        d1, d2 = st.columns(2)

        with d1:
            st.metric(
                "Priority",
                str(decision["priority"]),
            )

        with d2:
            st.metric(
                "Confidence",
                format_percent(
                    decision["confidence"] * 100
                ),
            )

        st.info(
            f"💡 **Why this action?**\n\n{decision['reason']}"
        )

        st.header("⚡ Recovery Action")

        if st.session_state.execution_result is None:

            st.warning(
                "This is a simulated bounded recovery action. "
                "No real money movement is performed by the AI action."
            )

            if st.button(
                f"⚡ EXECUTE {decision['action']}",
                use_container_width=True,
                key="execute_recovery",
            ):

                try:
                    with st.spinner("Executing recovery workflow..."):
                        st.session_state.execution_result = (
                            execute_transaction(
                                transaction,
                                prediction,
                                decision,
                            )
                        )

                    st.rerun()

                except Exception as exc:
                    st.error(f"❌ Recovery execution failed: {exc}")

        else:

            result = st.session_state.execution_result

            if result.get("status") == "EXECUTED":
                st.success("✅ Recovery action executed successfully.")
            else:
                st.warning(
                    f"Action status: {result.get('status', 'UNKNOWN')}"
                )

            r1, r2, r3 = st.columns(3)

            with r1:
                st.metric(
                    "Status",
                    str(result.get("status", "N/A")),
                )

            with r2:
                st.metric(
                    "Reference ID",
                    str(result.get("reference_id", "N/A")),
                )

            with r3:
                st.metric(
                    "Amount",
                    format_rupees(
                        result.get(
                            "amount",
                            transaction["amount"],
                        )
                    ),
                )

            st.info(
                str(
                    result.get(
                        "message",
                        "Recovery action processed.",
                    )
                )
            )

            if result.get("recovery_link"):
                st.write("### 🔗 Recovery Link")
                st.code(
                    str(result["recovery_link"]),
                    language="text",
                )

            st.success("✓ Action recorded in the AI audit log.")


# ============================================================
# DASHBOARD
# ============================================================

elif selected_page == "📊 Dashboard":

    st.title("📊 Revenue Recovery Dashboard")
    st.caption(
        "AI-powered visibility into failed-payment revenue and recovery."
    )

    st.success(
        f"🟢 System Online • {total_transactions:,} payment records loaded"
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(
            "Revenue at Risk",
            format_rupees(revenue_at_risk),
        )

    with k2:
        st.metric(
            "Expected Recovery",
            format_rupees(expected_recovery),
        )

    with k3:
        st.metric(
            "Recovered Revenue",
            format_rupees(actual_recovery),
        )

    with k4:
        st.metric(
            "Recovery Rate",
            format_percent(recovery_rate),
        )

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric("Failed Payments", f"{total_transactions:,}")

    with s2:
        st.metric("Recovered Payments", f"{recovered_transactions:,}")

    with s3:
        st.metric(
            "Average AI Probability",
            format_percent(average_probability),
        )

    with s4:
        st.metric(
            "Recovery Opportunities",
            f"{len(df):,}",
        )

    st.markdown("---")

    chart1, chart2 = st.columns(2)

    with chart1:
        st.subheader("💳 Recovery by Payment Method")

        method_data = (
            df.groupby("payment_method")["actual_recovered_amount"]
            .sum()
            .reset_index()
        )

        fig1 = px.bar(
            method_data,
            x="payment_method",
            y="actual_recovered_amount",
            labels={
                "payment_method": "Payment Method",
                "actual_recovered_amount": "Recovered Revenue (₹)",
            },
        )

        fig1.update_layout(
            template="plotly_white",
            height=400,
        )

        st.plotly_chart(
            fig1,
            use_container_width=True,
        )

    with chart2:
        st.subheader("⚠️ Revenue at Risk by Failure")

        failure_data = (
            df.groupby("failure_reason")["amount"]
            .sum()
            .reset_index()
            .sort_values("amount", ascending=False)
        )

        fig2 = px.bar(
            failure_data,
            x="failure_reason",
            y="amount",
            labels={
                "failure_reason": "Failure Reason",
                "amount": "Revenue at Risk (₹)",
            },
        )

        fig2.update_layout(
            template="plotly_white",
            height=400,
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
        )

    st.subheader("🎯 Top Recovery Opportunities")

    top = (
        df.sort_values(
            "expected_recovery_amount",
            ascending=False,
        )
        .head(15)
        .copy()
    )

    top["Recovery %"] = (
        top["recovery_probability"] * 100
    ).round(1)

    top["Expected Recovery"] = (
        top["expected_recovery_amount"].round(2)
    )

    st.dataframe(
        top[
            [
                "transaction_id",
                "customer_id",
                "amount",
                "payment_method",
                "failure_reason",
                "Recovery %",
                "Expected Recovery",
                "retry_count",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# RECOVERY OPPORTUNITIES
# ============================================================

elif selected_page == "🎯 Recovery Opportunities":

    st.title("🎯 Recovery Opportunities")
    st.caption(
        "Transactions ranked by expected recoverable revenue."
    )

    opportunities = df.copy()

    opportunities["priority_score"] = (
        opportunities["amount"]
        * opportunities["recovery_probability"]
    )

    opportunities = opportunities.sort_values(
        "priority_score",
        ascending=False,
    )

    opportunities["Recovery Probability"] = (
        opportunities["recovery_probability"] * 100
    ).round(1)

    opportunities["Expected Recovery"] = (
        opportunities["expected_recovery_amount"].round(2)
    )

    st.dataframe(
        opportunities[
            [
                "transaction_id",
                "customer_id",
                "amount",
                "payment_method",
                "failure_reason",
                "Recovery Probability",
                "Expected Recovery",
                "retry_count",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# PAYMENTS
# ============================================================

elif selected_page == "💳 Payments":

    st.title("💳 Payment Transactions")

    filter1, filter2 = st.columns(2)

    with filter1:
        payment_methods = (
            ["All"]
            + sorted(
                df["payment_method"]
                .astype(str)
                .unique()
                .tolist()
            )
        )

        selected_method = st.selectbox(
            "Payment Method",
            payment_methods,
            key="payment_method_filter",
        )

    with filter2:
        failure_reasons = (
            ["All"]
            + sorted(
                df["failure_reason"]
                .astype(str)
                .unique()
                .tolist()
            )
        )

        selected_reason = st.selectbox(
            "Failure Reason",
            failure_reasons,
            key="failure_reason_filter",
        )

    filtered_df = df.copy()

    if selected_method != "All":
        filtered_df = filtered_df[
            filtered_df["payment_method"].astype(str)
            == selected_method
        ]

    if selected_reason != "All":
        filtered_df = filtered_df[
            filtered_df["failure_reason"].astype(str)
            == selected_reason
        ]

    st.info(f"{len(filtered_df):,} transactions found")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# CUSTOMER INTELLIGENCE
# ============================================================

elif selected_page == "👤 Customer Intelligence":

    st.title("👤 Customer Intelligence")
    st.caption(
        "Customer history, payment behavior, and recovery potential."
    )

    customer_data = (
        df.groupby("customer_id")
        .agg(
            transactions=("transaction_id", "count"),
            total_amount=("amount", "sum"),
            recovered_amount=("actual_recovered_amount", "sum"),
            avg_recovery_probability=("recovery_probability", "mean"),
            successful_payments=(
                "previous_successful_payments",
                "max",
            ),
            previous_failures=(
                "previous_failed_payments",
                "max",
            ),
        )
        .reset_index()
    )

    customer_data["avg_recovery_probability"] = (
        customer_data["avg_recovery_probability"] * 100
    ).round(1)

    customer_data = customer_data.rename(
        columns={
            "total_amount": "Total Amount",
            "recovered_amount": "Recovered Amount",
            "avg_recovery_probability": "Average Recovery Probability (%)",
            "successful_payments": "Successful Payments",
            "previous_failures": "Previous Failures",
        }
    )

    st.dataframe(
        customer_data,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# ANALYTICS
# ============================================================

elif selected_page == "📈 Analytics":

    st.title("📈 Recovery Analytics")

    a1, a2, a3, a4 = st.columns(4)

    with a1:
        st.metric(
            "Revenue at Risk",
            format_rupees(revenue_at_risk),
        )

    with a2:
        st.metric(
            "Expected Recovery",
            format_rupees(expected_recovery),
        )

    with a3:
        st.metric(
            "Actual Recovery",
            format_rupees(actual_recovery),
        )

    with a4:
        st.metric(
            "Recovery Rate",
            format_percent(recovery_rate),
        )

    st.subheader("⚠️ Failure Analysis")

    failure_analysis = (
        df.groupby("failure_reason")
        .agg(
            transactions=("transaction_id", "count"),
            revenue_at_risk=("amount", "sum"),
            recovered_revenue=("actual_recovered_amount", "sum"),
            expected_recovery=("expected_recovery_amount", "sum"),
        )
        .reset_index()
    )

    failure_analysis["recovery_rate"] = (
        failure_analysis["recovered_revenue"]
        / failure_analysis["revenue_at_risk"]
        * 100
    ).fillna(0).round(2)

    st.dataframe(
        failure_analysis,
        use_container_width=True,
        hide_index=True,
    )

    fig3 = px.pie(
        failure_analysis,
        names="failure_reason",
        values="revenue_at_risk",
        title="Revenue at Risk Distribution",
    )

    fig3.update_layout(
        template="plotly_white",
        height=450,
    )

    st.plotly_chart(
        fig3,
        use_container_width=True,
    )


# ============================================================
# AUDIT LOGS
# ============================================================

elif selected_page == "📜 Audit Logs":

    st.title("📜 AI Audit Logs")
    st.caption(
        "Complete history of AI decisions and recovery actions."
    )

    if AUDIT_PATH.exists():

        try:
            audit_df = pd.read_csv(AUDIT_PATH)

            st.success(
                f"✓ {len(audit_df):,} audit records"
            )

            if len(audit_df) > 0:
                if "timestamp" in audit_df.columns:
                    audit_df = audit_df.sort_values(
                        "timestamp",
                        ascending=False,
                    )

                st.dataframe(
                    audit_df,
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info(
                    "No recovery actions have been executed yet."
                )

        except Exception as exc:
            st.error(f"❌ Could not read audit log: {exc}")

    else:
        st.info(
            "Audit log will appear after the first recovery action."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "RecoverAI • Autonomous AI Revenue Recovery • "
    "Synthetic demonstration environment • "
    "Razorpay Test Mode"
)
