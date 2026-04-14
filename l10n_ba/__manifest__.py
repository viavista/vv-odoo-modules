# Copyright 2026 Viavista d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Bosnia and Herzegovina - Accounting",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations/Account Charts",
    "summary": "Chart of accounts, taxes and fiscal positions for Bosnia and Herzegovina",
    "description": """
Chart of accounts for companies in Bosnia and Herzegovina.

Sources:
- Rulebook on chart of accounts and account contents for companies
  (Official Gazette of FBiH, No. 81/21)
    """,
    "author": "Viavista d.o.o., Odoo Community Association (OCA)",
    "website": "https://github.com/viavista/viavista-odoo-modules",
    "license": "AGPL-3",
    "development_status": "Alpha",
    "maintainers": ["vv-zgalic"],
    "countries": ["ba"],
    "icon": "/account/static/description/l10n.png",
    "depends": [
        "account",
        "base_vat",
    ],
    "auto_install": ["account"],
    "data": [
        "data/l10n_ba_chart_data.xml",
        "data/account_tax_report_data.xml",
        "views/res_partner_views.xml",
    ],
    "demo": [
        "demo/demo_company.xml",
    ],
    "installable": True,
}
