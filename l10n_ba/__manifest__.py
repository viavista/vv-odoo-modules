# Copyright 2026 Viavista d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Bosnia and Herzegovina - Accounting",
    "version": "19.0.2.0.0",
    "category": "Accounting/Localizations/Account Charts",
    "summary": "Chart of accounts, taxes, fiscal positions and invoice memorandum for Bosnia and Herzegovina",
    "description": """
Localization for companies in Bosnia and Herzegovina.

Includes:
- Chart of accounts (Pravilnik o kontnom okviru, Sl. novine FBiH 81/21)
- VAT taxes and fiscal positions (incl. non-VAT taxpayer with Article 44 note)
- Court of registration and MBS fields on res.company
- Auto-generated company memorandum block (JIB, court, MBS, activity code)
- Invoice template extensions: place of issue, full bank-accounts list
- Bosnian, Croatian and Serbian (Latin) translations
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
        "views/res_company_views.xml",
        "views/res_partner_views.xml",
        "views/report_invoice.xml",
    ],
    "demo": [
        "demo/demo_company.xml",
    ],
    "installable": True,
}
