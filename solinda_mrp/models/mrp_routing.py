from email.policy import default
from odoo import api, fields, models

class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    qty = fields.Float(string='Qty', related='bom_id.product_qty')
    fabric_id = fields.Many2one(comodel_name='mrp.bom.line',string='Fabric')
    hk = fields.Float(string='HK', related='fabric_id.product_qty')
    time_cycle_manual = fields.Float(
        string='Qty', related='bom_id.product_qty')
    workcenter_id = fields.Many2one(
        'mrp.workcenter', 'Service', required=True, check_company=True)
