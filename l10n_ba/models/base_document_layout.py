# Copyright 2026 Viavista d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from markupsafe import Markup

from odoo import _, api, fields, models


class BaseDocumentLayout(models.TransientModel):
    _inherit = "base.document.layout"

    @api.model
    def _default_company_details(self):
        # OVERRIDE web/models/base_document_layout: append BiH memorandum
        # lines (JIB, court of registration + MBS, activity code) after the
        # standard address block. Each line is only appended if it has data.
        company_details = super()._default_company_details()
        company = self.env.company
        if company.country_code != "BA":
            return company_details
        if company.company_registry:
            company_details += Markup("<br/>%s") % _("JIB: %s", company.company_registry)
        if company.l10n_ba_court_name:
            court_line = company.l10n_ba_court_name
            if company.l10n_ba_court_registration:
                court_line += ", " + _("MBS: %s", company.l10n_ba_court_registration)
            company_details += Markup("<br/>%s") % court_line
        if company.l10n_ba_activity_code:
            company_details += Markup("<br/>%s") % _(
                "Activity code: %s", company.l10n_ba_activity_code
            )
        return company_details

    # Re-bind the default so the override above is picked up.
    company_details = fields.Html(default=_default_company_details)
