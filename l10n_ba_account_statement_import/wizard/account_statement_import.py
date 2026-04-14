# Copyright 2026 Viavista d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import models

from .parser_mt940 import parse_mt940
from .parser_xml import parse_ba_xml

_logger = logging.getLogger(__name__)


class AccountStatementImport(models.TransientModel):
    _inherit = "account.statement.import"

    def _parse_file(self, data_file):
        """Parse BiH bank statement files (XML or MT940)."""
        # Try BA XML format (<IZ ...> root element)
        try:
            _logger.debug("Trying BiH XML parser.")
            return parse_ba_xml(data_file)
        except ValueError:
            pass

        # Try BA MT940 format ({1:F01... header)
        try:
            _logger.debug("Trying BiH MT940 parser.")
            return parse_mt940(data_file)
        except ValueError:
            pass

        return super()._parse_file(data_file)
