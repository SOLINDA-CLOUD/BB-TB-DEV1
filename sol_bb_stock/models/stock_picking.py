from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    @api.depends('partner_id', 'date')
    def _compute_analytic_account_id(self):
        for order in self:
            if not order.analytic_account_id:
                default_analytic_account = order.env['account.analytic.default'].sudo().account_get(
                    partner_id=order.partner_id.id,
                    user_id=order.env.uid,
                    date=order.date,
                    company_id=order.company_id.id,
                )
                order.analytic_account_id = default_analytic_account.analytic_id

    account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        store=True,
        string='Analytic Account',
        readonly=False,
        compute=_compute_analytic_account_id)
