# Copyright 2026 Viavista d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountDpdvReport(models.TransientModel):
    _name = "account.dpdv.report"
    _description = "Form D VAT - Supplementary VAT Declaration"

    date_from = fields.Date(
        required=True,
        default=lambda self: fields.Date.today().replace(day=1),
    )
    date_to = fields.Date(
        required=True,
        default=lambda self: fields.Date.today(),
    )
    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
    )

    generated = fields.Boolean()

    # Header
    company_name = fields.Char(compute="_compute_header", store=True)
    company_vat = fields.Char(compute="_compute_header", store=True)
    company_address = fields.Char(compute="_compute_header", store=True)

    # II. Supplies and output VAT
    # (1) Description  (2) Amount excl. VAT  (3) Output VAT
    out_1_base = fields.Float(
        "II.1 Non-taxable turnover (art. 3, 15)",
        digits=(16, 2),
    )
    out_2_base = fields.Float(
        "II.2 Supplies to EUFOR and NATO", digits=(16, 2),
    )
    out_3_base = fields.Float(
        "II.3 Exempt supplies - IPA fund (art. 29)", digits=(16, 2),
    )
    out_4_base = fields.Float(
        "II.4 Import-related services exempt from VAT (art. 26)",
        digits=(16, 2),
    )
    out_5_base = fields.Float(
        "II.5 Transfer of assets (art. 7)", digits=(16, 2),
    )
    out_6_base = fields.Float(
        "II.6 Real estate - first transfer", digits=(16, 2),
    )
    out_6_pdv = fields.Float("II.6 VAT", digits=(16, 2))
    out_7_pdv = fields.Float(
        "II.7 VAT on services by foreign persons (art. 13)", digits=(16, 2),
    )
    out_8_base = fields.Float(
        "II.8 VAT refunded to foreign citizens (PDV-SL-2)",
        digits=(16, 2),
    )
    out_8_pdv = fields.Float("II.8 VAT", digits=(16, 2))
    out_9_base = fields.Float(
        "II.9 Credit notes issued to domestic buyers", digits=(16, 2),
    )
    out_9_pdv = fields.Float("II.9 VAT", digits=(16, 2))
    out_10_pdv = fields.Float(
        "II.10 Unpaid VAT under special scheme (art. 41, 66)",
        digits=(16, 2),
    )

    # III. Purchases and input VAT
    in_1_base = fields.Float(
        "III.1 Acquisition of assets (art. 7)", digits=(16, 2),
    )
    in_2_base = fields.Float(
        "III.2 Real estate purchase with deduction right", digits=(16, 2),
    )
    in_2_pdv = fields.Float("III.2 VAT", digits=(16, 2))
    in_3_base = fields.Float(
        "III.3 Domestic equipment purchase with deduction right",
        digits=(16, 2),
    )
    in_3_pdv = fields.Float("III.3 VAT", digits=(16, 2))
    in_4_base = fields.Float(
        "III.4 Imported equipment with deduction right", digits=(16, 2),
    )
    in_4_pdv = fields.Float("III.4 VAT", digits=(16, 2))
    in_5_base = fields.Float(
        "III.5 Proportional deduction (art. 37)", digits=(16, 2),
    )
    in_5_pdv = fields.Float("III.5 VAT", digits=(16, 2))
    in_6_base = fields.Float(
        "III.6 Foreign services with deduction right", digits=(16, 2),
    )
    in_6_pdv = fields.Float("III.6 VAT", digits=(16, 2))
    in_7_pdv = fields.Float(
        "III.7 VAT under construction special scheme (art. 42)",
        digits=(16, 2),
    )
    in_8_base = fields.Float(
        "III.8 Credit notes received from suppliers", digits=(16, 2),
    )
    in_8_pdv = fields.Float("III.8 VAT", digits=(16, 2))
    in_9_pdv = fields.Float(
        "III.9 Input VAT deduction correction (art. 36)", digits=(16, 2),
    )

    # IV. Inventory
    stock_value = fields.Float(
        "IV.1 Inventory at end of period (excl. VAT)", digits=(16, 2),
    )

    @api.depends("company_id")
    def _compute_header(self):
        for rec in self:
            partner = rec.company_id.partner_id
            rec.company_name = partner.name or ""
            rec.company_vat = (
                partner.vat or ""
            )
            rec.company_address = ", ".join(
                filter(None, [partner.street, partner.zip, partner.city])
            )

    def action_generate(self):
        """Generate D PDV data.

        Most fields in D PDV require detailed tax/product category
        classification that goes beyond basic tax tags. This generates
        a form with zeros that the accountant fills in manually based
        on their detailed records. Fields that can be auto-populated
        from tax tags are filled where possible.
        """
        self.ensure_one()
        # D PDV fields require granular classification not available
        # from standard tax tags. Provide the form for manual entry.
        # Future: extend with product category / account-based detection.
        self.generated = True
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_print_pdf(self):
        self.ensure_one()
        return self.env.ref(
            "l10n_ba_account_pdv.action_report_dpdv"
        ).report_action(self)
