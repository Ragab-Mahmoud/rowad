# -*- coding: utf-8 -*-
# from odoo import http


# class PosMarginSale(http.Controller):
#     @http.route('/pos_margin_sale/pos_margin_sale', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_margin_sale/pos_margin_sale/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_margin_sale.listing', {
#             'root': '/pos_margin_sale/pos_margin_sale',
#             'objects': http.request.env['pos_margin_sale.pos_margin_sale'].search([]),
#         })

#     @http.route('/pos_margin_sale/pos_margin_sale/objects/<model("pos_margin_sale.pos_margin_sale"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_margin_sale.object', {
#             'object': obj
#         })

