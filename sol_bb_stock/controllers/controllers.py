# -*- coding: utf-8 -*-
# from odoo import http


# class SolBbStock(http.Controller):
#     @http.route('/sol_bb_stock/sol_bb_stock', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sol_bb_stock/sol_bb_stock/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sol_bb_stock.listing', {
#             'root': '/sol_bb_stock/sol_bb_stock',
#             'objects': http.request.env['sol_bb_stock.sol_bb_stock'].search([]),
#         })

#     @http.route('/sol_bb_stock/sol_bb_stock/objects/<model("sol_bb_stock.sol_bb_stock"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sol_bb_stock.object', {
#             'object': obj
#         })
