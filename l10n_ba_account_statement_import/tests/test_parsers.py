# Copyright 2026 Viavista d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
from datetime import date

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestParserXml(TransactionCase):
    """Test the BiH XML bank statement parser."""

    @classmethod
    def _read_sample(cls, filename):
        path = os.path.join(os.path.dirname(__file__), "samples", filename)
        with open(path, "rb") as f:
            return f.read()

    def test_parse_raiffeisen_xml(self):
        from ..wizard.parser_xml import parse_ba_xml

        data = self._read_sample("raiffeisen.xml")
        currency, account, statements = parse_ba_xml(data)

        self.assertEqual(currency, "BAM")
        self.assertEqual(account, "1610000123456789")
        self.assertEqual(len(statements), 1)

        stmt = statements[0]
        self.assertEqual(stmt["name"], "7")
        self.assertEqual(stmt["date"], date(2026, 4, 10))
        self.assertAlmostEqual(stmt["balance_start"], 2373.33)
        self.assertAlmostEqual(stmt["balance_end_real"], 3991.06)
        self.assertEqual(len(stmt["transactions"]), 7)

        # First transaction: credit
        txn = stmt["transactions"][0]
        self.assertAlmostEqual(txn["amount"], 1408.20)
        self.assertIn("TEMPLATE PARTNER", txn["payment_ref"])
        self.assertEqual(txn["date"], date(2026, 4, 10))

        # Second transaction: debit (bank fee)
        txn = stmt["transactions"][1]
        self.assertAlmostEqual(txn["amount"], -20.00)

    def test_parse_xml_not_ba_format(self):
        from ..wizard.parser_xml import parse_ba_xml

        with self.assertRaises(ValueError):
            parse_ba_xml(b"<root>not a BA statement</root>")

    def test_parse_xml_invalid(self):
        from ..wizard.parser_xml import parse_ba_xml

        with self.assertRaises(ValueError):
            parse_ba_xml(b"this is not xml at all")


@tagged("post_install", "-at_install")
class TestParserMt940(TransactionCase):
    """Test the BiH MT940 bank statement parser."""

    @classmethod
    def _read_sample(cls, filename):
        path = os.path.join(os.path.dirname(__file__), "samples", filename)
        with open(path, "rb") as f:
            return f.read()

    def test_parse_raiffeisen_mt940(self):
        from ..wizard.parser_mt940 import parse_mt940

        data = self._read_sample("raiffeisen.mt940")
        currency, account, statements = parse_mt940(data)

        self.assertEqual(currency, "BAM")
        self.assertEqual(account, "1610000123456789")
        self.assertEqual(len(statements), 1)

        stmt = statements[0]
        self.assertEqual(stmt["name"], "7")
        self.assertEqual(stmt["date"], date(2026, 4, 10))
        self.assertAlmostEqual(stmt["balance_start"], 2373.33)
        self.assertAlmostEqual(stmt["balance_end_real"], 3991.06)
        self.assertEqual(len(stmt["transactions"]), 7)

        # First transaction: credit
        txn = stmt["transactions"][0]
        self.assertAlmostEqual(txn["amount"], 1408.20)
        self.assertIn("TEMPLATE PARTNER", txn["payment_ref"])

        # Second transaction: debit
        txn = stmt["transactions"][1]
        self.assertAlmostEqual(txn["amount"], -20.00)

    def test_parse_mt940_not_valid(self):
        from ..wizard.parser_mt940 import parse_mt940

        with self.assertRaises(ValueError):
            parse_mt940(b"this is not mt940")
