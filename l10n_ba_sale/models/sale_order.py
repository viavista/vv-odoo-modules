# Copyright 2026 Viavista d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("product_id", "company_id")
    def _compute_tax_ids(self):
        # Strip taxes on sale-order lines when the company is registered in
        # BiH but is NOT a VAT taxpayer. Mirrors the override in
        # l10n_ba.account_move so that quotations match the invoice produced
        # from them. Article 44 of the BiH VAT Law.
        super()._compute_tax_ids()
        for line in self:
            company = line.company_id or line.order_id.company_id
            if (
                company.country_code == "BA"
                and not company.vat
                and line.tax_ids
            ):
                line.tax_ids = False
