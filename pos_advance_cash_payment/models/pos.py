# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import date, datetime

class ResPartner(models.Model):
    _inherit = 'res.partner'

    ledger_balance = fields.Float(string='Partner Ledger Balance', compute='_compute_ledger_balance', store=True)
    amount_note = fields.Float(string='amount_note')
    
    def action_view_balance_ledger(self):
        return

    def btn_refresh(self):
        self._compute_ledger_balance()
        
    @api.depends('invoice_ids.amount_total', 'invoice_ids.state', 'credit', 'debit', 'write_date', 'payment_amount_due', 'last_time_entries_checked', 'payment_amount_overdue')
    @api.onchange('invoice_ids.amount_total', 'invoice_ids.state', 'credit', 'debit', 'write_date', 'payment_amount_due', 'last_time_entries_checked', 'payment_amount_overdue')
    def _compute_ledger_balance(self):
            for partner in self:
                partner.ledger_balance = partner.credit - partner.debit 
            
    @api.depends('pos_order_ids', 'pos_order_ids.state', 'pos_order_ids.amount_paid')
    def _compute_pos_credit(self):
        for rec in self:
            orders = rec.pos_order_ids.filtered(lambda odr: odr.state == 'draft')
            pos_credit = sum(odr.amount_total - odr.amount_paid for odr in rec.pos_order_ids)
            rec.custom_credit = pos_credit

class POSOrder(models.Model):
	_inherit = 'pos.order'

	def create_customer_payment(self, partner_id, journal, amount):
		payment_object = self.env['account.payment']
		partner_object = self.env['res.partner']
		journal_id = self.env['account.journal'].browse(int(journal))
		if journal_id:					
			vals = {
				'payment_type':'inbound', 
				'partner_type':'customer', 
				'partner_id':partner_id, 
				'journal_id':journal_id.id, 
				'amount':amount, 
				'create_date': datetime.today(), 
				'payment_method_id':1 
			}
			payment = payment_object.create(vals)
			payment.action_post()
			this_partner = partner_object.search([('id', '=', partner_id)], limit=1)
			this_partner._compute_ledger_balance()
			this_partner.write({'amount_note': amount})
		return True
	
class PosSession(models.Model):
	_inherit = 'pos.session'

	def _pos_ui_models_to_load(self):
		result = super()._pos_ui_models_to_load()
		new_model = 'account.journal'
		if new_model not in result:
			result.append(new_model)
		return result


	def _loader_params_account_journal(self):
		return {
			'search_params': {
				'domain': [('type', 'in', ["cash","bank"])],
				'fields': ['name','type'],
			}
		}

	def _get_pos_ui_account_journal(self, params):
		return self.env['account.journal'].search_read(**params['search_params'])
