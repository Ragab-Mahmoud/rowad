from odoo import _, api, fields, models # type: ignore


class WizardMarginProduct(models.TransientModel):
    _name = 'wizard.margin.product'
    _description = 'Set margin on every product'


    product_template_ids = fields.Many2many('product.template', string='Products')
    product_ids = fields.Many2many('product.product', string="Product variants")
    is_product = fields.Boolean(string="is product", compute="_compute_product_model")
    margin = fields.Float('Margin')


    def _compute_product_model(self):
        active_model = self._context.get('active_model')
        for rec in self:
            if active_model == 'product.template':
                rec.is_product = True
            else:
                rec.is_product = False

    def action_assing_margin(self):
        active_model = self._context.get('active_model')
        if active_model == 'product.template':
            for product in self.product_template_ids:
                product.margin_sale = self.margin
        elif active_model == 'product.product':
            for product in self.product_ids:
                product.margin_sale = self.margin
        return True
    