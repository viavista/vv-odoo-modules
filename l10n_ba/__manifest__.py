# Copyright 2026 Viavista d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "BiH - Računovodstvo",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations/Account Charts",
    "summary": "Kontni plan, porezi i fiskalne pozicije za Bosnu i Hercegovinu",
    "description": """
Kontni plan za privredna društva u Bosni i Hercegovini

Izvori:
- Pravilnik o kontnom okviru i sadržaju konta za privredna društva
  (Službene novine Federacije BiH, broj 81/21)
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
