from odoo import api, fields, models

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    order_id = fields.Many2one(
        comodel_name='purchase.order',
        string='PO'
    )
    partner_id = fields.Many2one(
        string='Supplier', related='order_id.partner_id', default="Office")
    # price = fields.Float(string='Price', related='order_id.amount_total')
