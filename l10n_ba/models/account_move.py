# Copyright 2026 Viavista d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends("product_id", "product_uom_id")
    def _compute_tax_ids(self):
        # Strip taxes on customer-invoice product lines when the company is
        # registered in BiH but is NOT a VAT taxpayer (no VAT number set).
        # Article 44 of the BiH VAT Law: companies below the threshold do not
        # charge VAT. A note is added to the printed invoice via the template.
        super()._compute_tax_ids()
        out_types = ("out_invoice", "out_refund", "out_receipt")
        for line in self:
            move = line.move_id
            company = move.company_id
            if (
                company.country_code == "BA"
                and not company.vat
                and move.move_type in out_types
                and line.display_type == "product"
                and line.tax_ids
            ):
                line.tax_ids = False
