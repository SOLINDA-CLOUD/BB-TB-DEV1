from odoo import api, fields, models, _
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

    def _get_sub_lines(self, bom, product_id, line_qty, line_id, level, child_bom_ids, unfolded):
        data = self._get_bom(bom_id=bom.id, product_id=product_id,
                             line_qty=line_qty, line_id=line_id, level=level)
        bom_lines = data['components']
        lines = []
        for bom_line in bom_lines:
            lines.append({
                'name': bom_line['prod_name'],
                'type': 'bom',
                'quantity': bom_line['prod_qty'],
                'uom': bom_line['prod_uom'],
                'prod_cost': bom_line['prod_cost'],
                'bom_cost': bom_line['total'],
                'level': bom_line['level'],
                'code': bom_line['code'],
                'child_bom': bom_line['child_bom'],
                'prod_id': bom_line['prod_id']
            })
            if bom_line['child_bom'] and (unfolded or bom_line['child_bom'] in child_bom_ids):
                line = self.env['mrp.bom.line'].browse(bom_line['line_id'])
                lines += (self._get_sub_lines(line.child_bom_id, line.product_id.id,
                          bom_line['prod_qty'], line, level + 1, child_bom_ids, unfolded))
        if data['operations']:
            lines.append({
                'name': _('Operations'),
                'type': 'operation',
                'quantity': data['operations_time'],
                'bom_cost': data['operations_cost'],
                'level': level,
            })
            for operation in data['operations']:
                if unfolded or 'operation-' + str(bom.id) in child_bom_ids:
                    lines.append({
                        'name': operation['name'],
                        'type': 'operation',
                        'quantity': operation['duration_expected'],
                        'bom_cost': operation['total'],
                        'level': level + 1,
                    })
        if data['byproducts']:
            lines.append({
                'name': _('Byproducts'),
                'type': 'byproduct',
                'uom': False,
                'quantity': data['byproducts_total'],
                'bom_cost': data['byproducts_cost'],
                'level': level,
            })
            for byproduct in data['byproducts']:
                if unfolded or 'byproduct-' + str(bom.id) in child_bom_ids:
                    lines.append({
                        'name': byproduct['product_name'],
                        'type': 'byproduct',
                        'quantity': byproduct['product_qty'],
                        'uom': byproduct['product_uom'],
                        'prod_cost': byproduct['product_cost'],
                        'bom_cost': byproduct['bom_cost'],
                        'level': level + 1,
                    })
        return lines
