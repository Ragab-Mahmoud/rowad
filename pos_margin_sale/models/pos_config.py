from odoo import _, api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    is_blocked_warning = fields.Boolean(string="Blocked warning", compute='_compute_blocked_warning')


    def _compute_blocked_warning(self):
        for record in self:
            block_warning = self.env['ir.config_parameter'].sudo().get_param('post_margin_sale.blocking_transaction_pos')
            if block_warning:
                record.is_blocked_warning = True
            else:
                record.is_blocked_warning = False