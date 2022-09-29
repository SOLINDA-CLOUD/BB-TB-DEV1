from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        store=True,
        string='Analytic Account',
        readonly=False)
