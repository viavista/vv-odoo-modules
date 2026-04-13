# Copyright 2026 Viavista d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_ba_jib = fields.Char(
        string="JIB",
        help="Jedinstveni identifikacioni broj (Unique Identification Number)",
    )

    @api.model
    def _commercial_fields(self):
        return super()._commercial_fields() + ["l10n_ba_jib"]

    @api.depends("vat", "country_id")
    def _compute_company_registry(self):
        super()._compute_company_registry()
        for partner in self.filtered(
            lambda p: p.country_id.code == "BA" and p.vat
        ):
            vat_country, vat_number = self._split_vat(partner.vat)
            if vat_country in ("BA", ""):
                partner.company_registry = vat_number
