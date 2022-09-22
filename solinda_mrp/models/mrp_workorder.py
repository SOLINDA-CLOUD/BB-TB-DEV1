from odoo import api, fields, models

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    order_id = fields.Many2one(comodel_name='purchase.order', string='PO')
    supplier = fields.Many2one(comodel_name='res.partner', string='Supplier', related='order_id.partner_id')
    fabric_id = fields.Many2one(comodel_name='mrp.bom.line',string='Fabric', related='production_bom_id.operation_ids.fabric_id')
    hk = fields.Float(string='HK', related='production_bom_id.operation_ids.hk')
    color_id = fields.Many2one(comodel_name='dpt.color', string='Color', related='production_bom_id.operation_ids.color_id')
    shrinkage = fields.Float(string='Shkg(%)', default=0.0)

    duration_expected = fields.Float(
        'Expected Duration',
        digits=(16, 2),
        default=1.0,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="Expected duration (in minutes)")
