import json
import re
import csv

INPUT_FILE = "quickcart_data/raw_data.jsonl"
OUTPUT_FILE = "quickcart_data/clean_transactions.csv"


def normalize_amount(raw_amount):
    """
    Normalizes all currency formats into a single float column
    """
    if raw_amount is None:
        return None
    # Case 1: integer (assume cents)
    if isinstance(raw_amount, int):
        return raw_amount / 100.0
    # Case 2: string
    if isinstance(raw_amount, str):
        cleaned = raw_amount.strip().replace("$", "")
        # must be a number
        if re.match(r"^\d+(\.\d+)?$", cleaned):
            return float(cleaned)
    return None


def is_test_transaction(record):
    """
    Identify test or sandbox events.
    """
    email = record.get("entity", {}).get("customer", {}).get("email", "")
    flags = record.get("payload", {}).get("flags", [])  # will be [] if missing/None

    if email and "test" in email.lower():
        return True
    if isinstance(flags, list):
        if any("test" in str(flag).lower() for flag in flags):
            return True
    elif isinstance(flags, str):
        if "test" in flags.lower():
            return True
    return False


def extract_fields(record):
    """
    Extract and flatten the nested JSON into a simple dict.
    """
    event = record.get("event", {})
    entity = record.get("entity", {})
    payload = record.get("payload", {})
    payment = entity.get("payment", {})
    order = entity.get("order", {})
    customer = entity.get("customer", {})

    # Split timestamp into date and time
    timestamp = event.get("ts")
    date = None
    time = None
    if timestamp:
        if "T" in timestamp:
            parts = timestamp.split("T")
            date = parts[0]
            time = parts[1].replace("Z", "") if len(parts) > 1 else None
        else:
            date = timestamp

    return {
        "payment_id": payment.get("id").replace("pay_", "", 1) if payment.get("id") else None,
        "order_id": order.get("id").replace("ord_", "", 1) if order.get("id") else None,
        "provider": payment.get("provider"),
        "customer_email": customer.get("email"),
        "raw_amount": payload.get("Amount"),
        "currency": payload.get("currency"),
        "status": payload.get("status"),
        "date": date,
        "time": time
    }


def is_valid_record(row):
    """
    Rules for determining whether a record is acceptable:
        - payment_id must exist
        - amount must be valid
        - currency must exist
    """
    if not row.get("payment_id"):
        return False
    if row.get("amount_usd") is None:
        return False
    if not row.get("currency"):
        return False

    return True



# Main pipeline


def main():
    clean_rows = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            # Parse JSON safely
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                print(f"[WARN] Malformed JSON at line {line_number}")
                continue

            # Filter out test/sandbox data
            if is_test_transaction(record):
                continue

            # Extract fields
            row = extract_fields(record)

            # Normalize amount
            row["amount_usd"] = normalize_amount(row["raw_amount"])

            # Validate record
            if not is_valid_record(row):
                continue

            clean_rows.append(row)


    # Output a clean csv file

    fieldnames = [
        "payment_id",
        "order_id",
        "provider",
        "customer_email",
        "amount_usd",
        "currency",
        "status",
        "date",
        "time"
    ]

    # Filter rows to only include fieldnames
    filtered_rows = [{field: row.get(field) for field in fieldnames} for row in clean_rows]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)


    print(f"Completed extraction and cleaning")
    print(f"Clean rows: {len(clean_rows)}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()