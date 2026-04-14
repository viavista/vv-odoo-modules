# Copyright 2026 Viavista d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""Parser for BiH bank XML statement format.

Expected structure::

    <IZ RACUN="1610000XXXXXXXXX" VALUTA="KM"
        POCETNI_SALDO="2,373.33" KONACNI_SALDO="3,991.06"
        DATUM_IZVODA="10.04.2026" BROJ_IZVODA="7" ...>
        <PR RED_BR="1" SIFRA_DOZNAKE="8310939286"
            NALOGOPRIMAC_1="..." SVRHA="..."
            KNJIZENJE="C" IZNOS="1,408.20"
            DATUM_VALUTE="10.04.2026" DATUM_NALOGA="10.04.2026"/>
    </IZ>

Used by Raiffeisen BA and potentially other BiH banks.
"""

import xml.etree.ElementTree as ET
from datetime import datetime


# BiH banks use "KM" for BAM (convertible mark)
_CURRENCY_MAP = {
    "KM": "BAM",
}


def _parse_amount(value):
    """Parse amount string with comma as decimal separator.

    '1408,20' -> 1408.20
    '2.373,33' -> 2373.33  (if thousands separator is used)
    """
    value = value.strip()
    # Remove thousands separator (dot) if comma is decimal separator
    if "," in value:
        value = value.replace(".", "").replace(",", ".")
    return float(value)


def _parse_date(value):
    """Parse date in DD.MM.YYYY format."""
    return datetime.strptime(value.strip(), "%d.%m.%Y").date()


def parse_ba_xml(data_file):
    """Parse a BiH bank XML statement file.

    :param data_file: raw file content (bytes)
    :returns: tuple (currency_code, account_number, [statement_data])
    :raises ValueError: if the file is not a valid BiH XML statement
    """
    try:
        root = ET.fromstring(data_file)
    except ET.ParseError as e:
        raise ValueError(f"Not a valid XML file: {e}") from e

    if root.tag != "IZ":
        raise ValueError(f"Not a BiH bank XML statement (root tag: {root.tag})")

    account_number = root.get("RACUN")
    currency_raw = root.get("VALUTA", "")
    currency_code = _CURRENCY_MAP.get(currency_raw.upper(), currency_raw.upper())
    statement_date = _parse_date(root.get("DATUM_IZVODA"))
    statement_number = root.get("BROJ_IZVODA", "")

    transactions = []
    for pr in root.findall("PR"):
        direction = pr.get("KNJIZENJE", "").upper()
        amount = _parse_amount(pr.get("IZNOS", "0"))
        if direction == "D":
            amount = -amount

        # Build partner name from NALOGOPRIMAC fields
        partner_parts = [
            pr.get("NALOGOPRIMAC_1", "").strip(),
            pr.get("NALOGOPRIMAC_2", "").strip(),
            pr.get("NALOGOPRIMAC_3", "").strip(),
        ]
        partner_name = " ".join(p for p in partner_parts if p) or ""

        red_br = pr.get("RED_BR", "")
        sifra = pr.get("SIFRA_DOZNAKE", "")

        transactions.append(
            {
                "date": _parse_date(pr.get("DATUM_VALUTE", pr.get("DATUM_NALOGA"))),
                "amount": amount,
                "payment_ref": pr.get("SVRHA", ""),
                "partner_name": partner_name,
                "unique_import_id": f"{statement_number}-{red_br}-{sifra}",
            }
        )

    statement = {
        "name": statement_number,
        "date": statement_date,
        "balance_start": _parse_amount(root.get("POCETNI_SALDO", "0")),
        "balance_end_real": _parse_amount(root.get("KONACNI_SALDO", "0")),
        "transactions": transactions,
    }

    return currency_code, account_number, [statement]
