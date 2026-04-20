from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestProductBrand(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Brand = cls.env['product.brand']
        cls.Template = cls.env['product.template']
        cls.brand_a = cls.Brand.create({'name': 'Brand A'})
        cls.brand_b = cls.Brand.create({'name': 'Brand B'})

    def test_product_count_zero_for_empty_brand(self):
        self.assertEqual(self.brand_a.product_count, 0)

    def test_product_count_matches_linked_templates(self):
        self.Template.create({'name': 'P1', 'brand_id': self.brand_a.id})
        self.Template.create({'name': 'P2', 'brand_id': self.brand_a.id})
        self.Template.create({'name': 'P3', 'brand_id': self.brand_b.id})
        self.brand_a.invalidate_recordset(['product_count'])
        self.brand_b.invalidate_recordset(['product_count'])
        self.assertEqual(self.brand_a.product_count, 2)
        self.assertEqual(self.brand_b.product_count, 1)

    def test_variant_brand_follows_template(self):
        template = self.Template.create({'name': 'Variant P', 'brand_id': self.brand_a.id})
        variant = template.product_variant_ids[:1]
        self.assertEqual(variant.brand_id, self.brand_a)
        template.brand_id = self.brand_b
        self.assertEqual(variant.brand_id, self.brand_b)

    def test_archive_hides_brand_from_default_search(self):
        self.brand_a.action_archive()
        self.assertFalse(self.brand_a.active)
        self.assertNotIn(self.brand_a, self.Brand.search([]))
        self.assertIn(self.brand_a, self.Brand.with_context(active_test=False).search([]))

    def test_action_view_products_returns_filtered_domain(self):
        self.Template.create({'name': 'P1', 'brand_id': self.brand_a.id})
        action = self.brand_a.action_view_products()
        self.assertEqual(action['res_model'], 'product.template')
        self.assertIn(('brand_id', '=', self.brand_a.id), action['domain'])
        self.assertEqual(action['context']['default_brand_id'], self.brand_a.id)

    def test_order_by_sequence_then_name(self):
        self.brand_a.sequence = 20
        self.brand_b.sequence = 10
        brands = self.Brand.search([('id', 'in', (self.brand_a + self.brand_b).ids)])
        self.assertEqual(brands[0], self.brand_b)
        self.assertEqual(brands[1], self.brand_a)


@tagged('post_install', '-at_install')
class TestBrandDisplayName(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Param = cls.env['ir.config_parameter'].sudo()
        cls.brand = cls.env['product.brand'].create({'name': 'Acme'})
        cls.template = cls.env['product.template'].create({
            'name': 'Laptop',
            'brand_id': cls.brand.id,
        })
        cls.variant = cls.template.product_variant_ids[:1]

    def _set_format(self, fmt):
        self.Param.set_param('viavista_product_brand.sale_format', fmt)
        self.template.invalidate_recordset(['display_name'])
        self.variant.invalidate_recordset(['display_name'])

    def test_format_no_uses_plain_name(self):
        self._set_format('no')
        self.assertEqual(self.template.display_name, 'Laptop')
        self.assertEqual(self.variant.display_name, 'Laptop')

    def test_format_bracket_on_template(self):
        self._set_format('bracket')
        self.assertEqual(self.template.display_name, '[Acme] Laptop')

    def test_format_dash_on_variant(self):
        self._set_format('dash')
        self.assertEqual(self.variant.display_name, 'Acme - Laptop')

    def test_format_space(self):
        self._set_format('space')
        self.assertEqual(self.template.display_name, 'Acme Laptop')
        self.assertEqual(self.variant.display_name, 'Acme Laptop')

    def test_product_without_brand_unaffected(self):
        self._set_format('bracket')
        plain = self.env['product.template'].create({'name': 'Mouse'})
        self.assertEqual(plain.display_name, 'Mouse')

    def test_brand_prefixes_sale_order_line_name(self):
        self._set_format('dash')
        partner = self.env['res.partner'].create({'name': 'Customer X'})
        order = self.env['sale.order'].create({'partner_id': partner.id})
        line = self.env['sale.order.line'].create({
            'order_id': order.id,
            'product_id': self.variant.id,
        })
        self.assertTrue(line.name.startswith('Acme - Laptop'))

    def test_existing_draft_line_refreshed_on_setting_change(self):
        self._set_format('no')
        partner = self.env['res.partner'].create({'name': 'Customer X'})
        order = self.env['sale.order'].create({'partner_id': partner.id})
        line = self.env['sale.order.line'].create({
            'order_id': order.id,
            'product_id': self.variant.id,
        })
        self.assertEqual(line.name, 'Laptop')
        settings = self.env['res.config.settings'].create({
            'product_brand_sale_format': 'dash',
        })
        settings.set_values()
        self.assertTrue(line.name.startswith('Acme - Laptop'))
