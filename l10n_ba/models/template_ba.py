# Copyright 2026 Viavista d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, Command
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = "account.chart.template"

    @template("ba")
    def _get_ba_template_data(self):
        return {
            "code_digits": "6",
            "use_storno_accounting": True,
            "property_account_receivable_id": "ba_211000",
            "property_account_payable_id": "ba_432000",
            "property_account_expense_categ_id": "ba_511000",
            "property_account_income_categ_id": "ba_601000",
        }

    @template("ba", "res.company")
    def _get_ba_res_company(self):
        return {
            self.env.company.id: {
                "account_fiscal_country_id": "base.ba",
                "bank_account_code_prefix": "200",
                "cash_account_code_prefix": "205",
                "transfer_account_code_prefix": "2020",
                "account_default_pos_receivable_account_id": "ba_211000",
                "income_currency_exchange_account_id": "ba_662000",
                "expense_currency_exchange_account_id": "ba_562000",
                "account_sale_tax_id": "VAT_S_17",
                "account_purchase_tax_id": "VAT_P_17",
                "expense_account_id": "ba_550000",
                "income_account_id": "ba_601000",
                # FBiH practice: invoices include the total written out in words.
                "display_invoice_amount_total_words": True,
            },
        }

    @template("ba", "account.reconcile.model")
    def _get_ba_reconcile_model(self):
        return {
            "bank_commission_template": {
                "name": "Bankarska provizija",
                "line_ids": [
                    Command.create({
                        "account_id": "ba_553000",
                        "amount_type": "percentage",
                        "amount_string": "100",
                        "label": "Bankarska provizija",
                    }),
                ],
            },
            "interest_income_template": {
                "name": "Prihod od kamata",
                "line_ids": [
                    Command.create({
                        "account_id": "ba_661000",
                        "amount_type": "percentage",
                        "amount_string": "100",
                        "label": "Prihod od kamata",
                    }),
                ],
            },
            "interest_expense_template": {
                "name": "Rashod od kamata",
                "line_ids": [
                    Command.create({
                        "account_id": "ba_561000",
                        "amount_type": "percentage",
                        "amount_string": "100",
                        "label": "Rashod od kamata",
                    }),
                ],
            },
            "exchange_gain_template": {
                "name": "Pozitivne kursne razlike",
                "line_ids": [
                    Command.create({
                        "account_id": "ba_662000",
                        "amount_type": "percentage",
                        "amount_string": "100",
                        "label": "Pozitivne kursne razlike",
                    }),
                ],
            },
            "exchange_loss_template": {
                "name": "Negativne kursne razlike",
                "line_ids": [
                    Command.create({
                        "account_id": "ba_562000",
                        "amount_type": "percentage",
                        "amount_string": "100",
                        "label": "Negativne kursne razlike",
                    }),
                ],
            },
        }
