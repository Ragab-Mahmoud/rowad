from odoo import _, api, fields, models



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    blocking_transaction_order = fields.Boolean("Blocking Transaction Order", config_parameter="post_margin_sale.blocking_transaction_order")
    blocking_transaction_pos = fields.Boolean("Blocking Transaction POS", config_parameter="post_margin_sale.blocking_transaction_pos")
