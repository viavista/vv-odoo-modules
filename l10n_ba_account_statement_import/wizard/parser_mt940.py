# Copyright 2026 Viavista d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""Parser for MT940 (SWIFT) bank statement format used by BiH banks.

Structure::

    {1:F01RZBABA2SAXXX...}{2:I940...}{4:
    :20:PPU          /260410         <- transaction reference
    :25:1610000XXXXXXXXX             <- account number
    :28C:7                           <- statement number
    :60F:C260410BAM2373,33           <- opening balance
    :61:260410C        1408,20NMSC8310939286   <- transaction
    :86:description text             <- transaction details
    :62F:C260410BAM3991,06           <- closing balance
    -}

Used by Raiffeisen BA and other BiH banks using SWIFT MT940 format.
"""

import re
from datetime import datetime


def _parse_mt940_amount(value):
    """Parse MT940 amount with comma as decimal separator.

    '1408,20' -> 1408.20
    """
    return float(value.replace(",", "."))


def _parse_mt940_date(value):
    """Parse YYMMDD date format."""
    return datetime.strptime(value, "%y%m%d").date()


def _parse_balance_field(value):
    """Parse :60F: or :62F: balance field.

    Format: C/D + YYMMDD + currency + amount
    Example: 'C260410BAM2373,33'
    Returns: (direction, date, currency, amount)
    """
    match = re.match(
        r"^([CD])(\d{6})([A-Z]{3})([\d,]+)$",
        value.strip(),
    )
    if not match:
        raise ValueError(f"Invalid balance field: {value}")
    direction, date_str, currency, amount_str = match.groups()
    amount = _parse_mt940_amount(amount_str)
    if direction == "D":
        amount = -amount
    return _parse_mt940_date(date_str), currency, amount


def _parse_transaction_line(value):
    """Parse :61: transaction line.

    Format: YYMMDD + C/D + amount + type + reference
    Example: '260410C        1408,20NMSC8310939286'
    """
    match = re.match(
        r"^(\d{6})"  # value date YYMMDD
        r"(\d{4})?"  # optional entry date MMDD
        r"(C|D|RC|RD)"  # debit/credit mark
        r"\s*([\d,]+)"  # amount
        r"([A-Z]\w{3})"  # transaction type (4 chars)
        r"(.*)$",  # reference
        value.strip(),
    )
    if not match:
        raise ValueError(f"Invalid :61: line: {value}")
    date_str, _entry_date, direction, amount_str, _txn_type, reference = match.groups()
    amount = _parse_mt940_amount(amount_str)
    if direction in ("D", "RD"):
        amount = -amount
    if direction in ("RC", "RD"):
        amount = -amount  # reversal
    return {
        "date": _parse_mt940_date(date_str),
        "amount": amount,
        "reference": reference.strip(),
    }


def parse_mt940(data_file):
    """Parse an MT940 bank statement file.

    :param data_file: raw file content (bytes)
    :returns: tuple (currency_code, account_number, [statement_data])
    :raises ValueError: if the file is not a valid MT940 file
    """
    try:
        content = data_file.decode("utf-8", errors="replace")
    except (UnicodeDecodeError, AttributeError) as e:
        raise ValueError(f"Cannot decode file: {e}") from e

    if "{1:" not in content and ":20:" not in content:
        raise ValueError("Not an MT940 file")

    # Extract tag blocks
    tags = {}
    current_tag = None
    current_value = []

    # Split into lines, handle both \r\n and \n
    lines = content.replace("\r\n", "\n").split("\n")

    # Strip SWIFT envelope
    body = content
    block4_match = re.search(r"\{4:\s*\n?(.*?)(?:-\}|$)", body, re.DOTALL)
    if block4_match:
        body = block4_match.group(1)

    lines = body.strip().split("\n")
    transactions = []
    account_number = None
    statement_number = None
    balance_start = None
    balance_end = None
    currency_code = None
    statement_date = None

    current_tag = None
    current_value = ""

    def _process_tag(tag, value):
        nonlocal account_number, statement_number, currency_code
        nonlocal balance_start, balance_end, statement_date

        if tag == "25":
            account_number = value.strip()
        elif tag == "28C":
            statement_number = value.strip().split("/")[0]
        elif tag == "60F":
            date, currency_code, amount = _parse_balance_field(value)
            balance_start = amount
            statement_date = date
        elif tag == "62F":
            _, _, amount = _parse_balance_field(value)
            balance_end = amount
        elif tag == "61":
            txn = _parse_transaction_line(value)
            transactions.append(txn)
        elif tag == "86":
            # :86: is the description for the preceding :61:
            if transactions:
                transactions[-1]["description"] = value.strip()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        tag_match = re.match(r"^:(\d{2}[A-Z]?):(.*)$", line)
        if tag_match:
            if current_tag:
                _process_tag(current_tag, current_value)
            current_tag = tag_match.group(1)
            current_value = tag_match.group(2)
        elif current_tag:
            current_value += " " + line

    # Process last tag
    if current_tag:
        _process_tag(current_tag, current_value)

    if not account_number and not transactions:
        raise ValueError("No account number or transactions found in MT940")

    # Build OCA-compatible statement data
    statement_transactions = []
    for idx, txn in enumerate(transactions, start=1):
        description = txn.get("description", "")
        statement_transactions.append(
            {
                "date": txn["date"],
                "amount": txn["amount"],
                "payment_ref": description or txn.get("reference", ""),
                "unique_import_id": (
                    f"{statement_number}-{idx}-{txn.get('reference', '')}"
                ),
            }
        )

    statement = {
        "name": statement_number or "",
        "date": statement_date,
        "balance_start": balance_start or 0.0,
        "balance_end_real": balance_end or 0.0,
        "transactions": statement_transactions,
    }

    return currency_code or "BAM", account_number, [statement]
