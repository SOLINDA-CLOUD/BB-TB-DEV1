from odoo import api, fields, models
from odoo.tools import float_round

class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    def _get_operation_line(self, product, bom, qty, level):
        operations = []
        total = 0.0
        qty = bom.product_uom_id._compute_quantity(
            qty, bom.product_tmpl_id.uom_id)
        for operation in bom.operation_ids:
            if operation._skip_operation_line(product):
                continue
            operation_cycle = float_round(
                qty / operation.workcenter_id.capacity, precision_rounding=1, rounding_method='UP')
            duration_expected = (operation_cycle * operation.time_cycle * 100.0 / operation.workcenter_id.time_efficiency) + (
                operation.workcenter_id.time_stop + operation.workcenter_id.time_start)
            total = (operation.workcenter_id.costs_hour)
            operations.append({
                'level': level or 0,
                'operation': operation,
                'name': operation.name + ' - ' + operation.workcenter_id.name,
                'duration_expected': duration_expected,
                'total': self.env.company.currency_id.round(total),
            })
        return operations
