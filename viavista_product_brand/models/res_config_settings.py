from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_brand_sale_format = fields.Selection(
        selection=[
            ('no', 'No'),
            ('bracket', 'Yes — [Brand] Product name'),
            ('dash', 'Yes — Brand - Product name'),
            ('space', 'Yes — Brand Product name'),
        ],
        string='Show Product Brand in Product Name',
        default='no',
        config_parameter='viavista_product_brand.sale_format',
        help='Prepends the brand name to the product display name throughout '
             'the interface (sale orders, invoices, inventory, reports, etc.). '
             'Existing draft quotations are refreshed to match; confirmed '
             'orders are not modified.',
    )

    def set_values(self):
        IrConfig = self.env['ir.config_parameter'].sudo()
        old_format = IrConfig.get_param('viavista_product_brand.sale_format', 'no')
        super().set_values()
        new_format = IrConfig.get_param('viavista_product_brand.sale_format', 'no')
        if old_format != new_format:
            self._refresh_draft_sale_order_lines()

    def _refresh_draft_sale_order_lines(self):
        lines = self.env['sale.order.line'].search([
            ('order_id.state', 'in', ('draft', 'sent')),
            ('product_id', '!=', False),
            ('product_id.brand_id', '!=', False),
        ])
        for line in lines:
            line.name = line._get_sale_order_line_multiline_description_sale()
