# Copyright 2026 Viavista d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_ba_court_name = fields.Char(
        string="Court of Registration",
        help="Court where the company is registered "
             "(e.g. Općinski sud u Širokom Brijegu).",
    )
    l10n_ba_court_registration = fields.Char(
        string="Court Registration Number (MBS)",
        help="Matični broj subjekta upisa — registration entry number "
             "issued by the court. Format varies by canton.",
    )
    l10n_ba_activity_code = fields.Char(
        string="Activity Code",
        help="Šifra djelatnosti — classification code per KD2010.",
    )
