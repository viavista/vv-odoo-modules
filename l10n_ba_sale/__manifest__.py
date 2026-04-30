# Copyright 2026 Viavista d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Bosnia and Herzegovina - Sales",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "summary": "Bridge between l10n_ba and Sales: auto-applies non-VAT fiscal position on quotations",
    "description": """
Bridge module that propagates BiH non-VAT taxpayer behavior to sales orders.

When the company is in Bosnia and Herzegovina but has no VAT number, sales
orders automatically use the "Non-VAT taxpayer" fiscal position (Article 44
of the BiH VAT Law), which strips VAT from order lines and ensures the
invoice notes the non-VAT status.
    """,
    "author": "Viavista d.o.o., Odoo Community Association (OCA)",
    "website": "https://github.com/viavista/viavista-odoo-modules",
    "license": "AGPL-3",
    "development_status": "Alpha",
    "maintainers": ["vv-zgalic"],
    "countries": ["ba"],
    "depends": [
        "l10n_ba",
        "sale",
    ],
    "auto_install": True,
    "data": [],
    "installable": True,
}
