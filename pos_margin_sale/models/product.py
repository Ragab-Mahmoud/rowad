from odoo import _, api, fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'


    margin_sale = fields.Float('Margin')
    


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    margin_sale = fields.Float(string="Margin", tracking=True, compute="_compute_margin_sale", store=True, readonly=False)
    minimum_sale_price = fields.Float(string="Minimum sale price", compute='_compute_minimum_sale_price', 
                                      inverse='_inverse_minimum_sale_price', store=True, readonly=False)
    minimum_sale_price_with_tax = fields.Float(string="Minimum sale price (Tax include)", compute='_compute_minimum_sale_price_with_tax', store=True)
    
    @api.depends('categ_id.margin_sale')
    def _compute_margin_sale(self):
        for rec in self:
            rec.margin_sale = rec.categ_id.margin_sale

    @api.depends('margin_sale', 'minimum_sale_price', 'taxes_id')
    def _compute_minimum_sale_price_with_tax(self):
        for rec in self:
            tax_amount = sum(tax.amount for tax in rec.taxes_id)
            rec.minimum_sale_price_with_tax = rec.minimum_sale_price * (1 + tax_amount / 100)

    @api.depends('margin_sale', 'standard_price')
    def _compute_minimum_sale_price(self):
        for rec in self:
            rec.minimum_sale_price = rec.standard_price * (1 + rec.margin_sale/100)
          
    def _inverse_minimum_sale_price(self):
        for rec in self:
            if rec.standard_price:
                rec.margin_sale = ((rec.minimum_sale_price / rec.standard_price) - 1) * 100
            else:
                rec.margin_sale = 0.0

    def action_assign_margin(self):
        wizard = self.env['wizard.margin.product'].create({
            'product_template_ids': [(6, 0, self.ids)]
        })
        return {
            'type': 'ir.actions.act_window',
            'name': _('Update margin sale'),
            'view_mode': 'form',
            'res_model': 'wizard.margin.product',
            'target': 'new',
            'res_id': wizard.id,
        }


class ProductProduct(models.Model):
    _inherit = 'product.product'

    margin_sale = fields.Float(string="Margin", tracking=True, compute="_compute_margin_sale", inverse="_set_product_margin_sale", store=True, readonly=False)
    minimum_sale_price = fields.Float(string="Minimum sale price", compute="_compute_minimum_sale_price", inverse='_inverse_minimum_sale_price', store=True, readonly=False)
    is_less_minimum_sale = fields.Boolean(string="Less minimum price", compute="_compute_warning")

    @api.onchange('margin_sale')
    def _set_product_margin_sale(self):
        for rec in self:
            rec.product_tmpl_id.write({'margin_sale': rec.margin_sale})

    def _compute_warning(self):
        for rec in self:
            rec.is_less_minimum_sale = rec.lst_price < rec.minimum_sale_price

    @api.depends('categ_id.margin_sale', 'product_tmpl_id.margin_sale')
    def _compute_margin_sale(self):
        for record in self:
            record.margin_sale = record.product_tmpl_id.margin_sale
    
    @api.depends('margin_sale', 'standard_price')
    def _compute_minimum_sale_price(self):
        for rec in self:
            rec.minimum_sale_price = rec.standard_price * (1 + rec.margin_sale/100)

    def _inverse_minimum_sale_price(self):
        for rec in self:
            if rec.standard_price:
                rec.margin_sale = ((rec.minimum_sale_price / rec.standard_price) - 1) * 100
            else:
                rec.margin_sale = 0.0

    def action_assign_margin(self):
        wizard = self.env['wizard.margin.product'].create({
            'product_ids': [(6, 0, self.ids)]
        })
        return {
            'type': 'ir.actions.act_window',
            'name': _('Update margin sale'),
            'view_mode': 'form',
            'res_model': 'wizard.margin.product',
            'target': 'new',
            'res_id': wizard.id,
        }