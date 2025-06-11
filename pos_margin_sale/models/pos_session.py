from odoo import _, api, fields, models



class PosSession(models.Model):
    _inherit = 'pos.session'


    def _loader_params_product_product(self):
        params = super(PosSession, self)._loader_params_product_product()
        params['search_params']['fields'].append('minimum_sale_price')
        params['search_params']['fields'].append('minimum_sale_price_with_tax')
        return params
