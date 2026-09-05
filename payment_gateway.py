import os
import razorpay
from dotenv import load_dotenv

load_dotenv()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
    raise RuntimeError(
        "Razorpay API keys are missing from .env"
    )

client = razorpay.Client(
    auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
)


def create_payment_order(amount, receipt_id):

    order_data = {
        "amount": int(amount * 100),
        "currency": "INR",
        "receipt": receipt_id
    }

    return client.order.create(
        data=order_data
    )


def get_key_id():

    return RAZORPAY_KEY_ID


def verify_payment_signature(
    razorpay_order_id,
    razorpay_payment_id,
    razorpay_signature
):

    try:

        client.utility.verify_payment_signature({
            "razorpay_order_id":
                razorpay_order_id,

            "razorpay_payment_id":
                razorpay_payment_id,

            "razorpay_signature":
                razorpay_signature
        })

        return True

    except Exception:

        return False


if __name__ == "__main__":

    print(
        "Creating Razorpay Test Mode order..."
    )

    order = create_payment_order(
        amount=100,
        receipt_id="recoverai_test_001"
    )

    print("\nOrder created successfully!")

    print(
        "Order ID:",
        order["id"]
    )

    print(
        "Amount:",
        order["amount"] / 100,
        "INR"
    )

    print(
        "Currency:",
        order["currency"]
    )

    print(
        "Status:",
        order["status"]
    )