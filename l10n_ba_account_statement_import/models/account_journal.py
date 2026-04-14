# Copyright 2026 Viavista d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    def _get_bank_statements_available_import_formats(self):
        res = super()._get_bank_statements_available_import_formats()
        res.extend(["MT940 (BiH)", "XML (BiH)"])
        return res
