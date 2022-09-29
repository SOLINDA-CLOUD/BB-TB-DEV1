import datetime

from odoo import fields, api, models
from odoo.tools import float_compare, float_round, float_is_zero, format_datetime

class ProductionDetail(models.Model):
    _name = 'production.detail'
    _description = 'Production Detail'
    _date_name = 'date_planned_start'

    @api.model
    def _get_default_date_planned_start(self):
        if self.env.context.get('default_date_deadline'):
            return fields.Datetime.to_datetime(self.env.context.get('default_date_deadline'))
        return datetime.datetime.now()

    # @api.depends(
    #     'move_raw_ids.state', 'move_raw_ids.quantity_done', 'move_finished_ids.state',
    #     'workorder_ids.state', 'product_qty', 'qty_producing')
    # def _compute_state(self):
    #     for production in self:
    #             if not production.state or not production.product_uom_id:
    #                 production.state = 'draft'
    #             elif production.state == 'cancel' or (production.move_finished_ids and all(move.state == 'cancel' for move in production.move_finished_ids)):
    #                 production.state = 'cancel'
    #             elif production.state == 'done' or (production.move_raw_ids and all(move.state in ('cancel', 'done') for move in production.move_raw_ids)):
    #                 production.state = 'done'
    #             elif any(wo_state in ('progress', 'done') for wo_state in production.workorder_ids.mapped('state')):
    #                 production.state = 'progress'
    #             elif production.product_uom_id and not float_is_zero(production.qty_producing, precision_rounding=production.product_uom_id.rounding):
    #                 production.state = 'progress'
    #             elif any(not float_is_zero(move.quantity_done, precision_rounding=move.product_uom.rounding or move.product_id.uom_id.rounding) for move in production.move_raw_ids):
    #                 production.state = 'progress'
    
    # state = fields.Selection([
    #     ('draft', 'Draft'),
    #     ('confirmed', 'Confirmed'),
    #     ('progress', 'In Progress'),
    #     ('done', 'Done')],
    #     string='State',
    #     compute='_compute_state', copy=False, index=True, readonly=True,
    #     store=True, tracking=True,
    #     help=" * Draft: The MO is not confirmed yet.\n"
    #          " * Confirmed: The MO is confirmed, the stock rules and the reordering of the components are trigerred.\n"
    #          " * In Progress: The production has started (on the MO or on the WO).\n"
    #          " * To Close: The production is done, the MO has to be closed.\n"
    #          " * Done: The MO is closed, the stock moves are posted. \n"
    #          " * Cancelled: The MO has been cancelled, can't be confirmed anymore.")

    name = fields.Char(
        required=True,
        default='New',
        index=True,
        readonly=True,
        string='Trans No.'
    )

    trans_date = fields.Datetime(
        string='Transaction Date',
        default=fields.Datetime.now,
        index=True,
        required=True,
        readonly=True,
        )
    bom_id = fields.Many2one(
        comodel_name="mrp.bom",
        string="Bill of Materials",
        required=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        required=True,
        track_visibility="onchange",
        readonly=True,
    )
    date_planned_start = fields.Datetime(
        'Scheduled Date', copy=False, default=_get_default_date_planned_start,
        help="Date at which you plan to start the production.",
        index=True, required=True)
    product_tmpl_id = fields.Many2one('product.template', string='Product')
    image = fields.Image(string='Fabric Swatch')
    product_qty = fields.Float('Quantity')
    customer = fields.Many2one(related='bom_id.customer', string='Customer', store=True)
    retail_price = fields.Float(related='bom_id.retail_price', string='Retail Price', store=True)
    sales_order_id = fields.Many2one(comodel_name='sale.order', string='SO No.')
    po_no = fields.Char(string='PO No.')
    production_detail_ids = fields.One2many('production.detail.line', 'product_id', string='Production Detail Line')
    fit_notes = fields.Text(string='Fit Notes')

class ProductionDetailLine(models.Model):
    _name = 'production.detail.line'
    _description = 'Production Detail Line'

    production_id = fields.Many2one('mrp.production', string='MO')
    product_id = fields.Many2one('product.product', string='Variant')
    variant_qty = fields.Float(string='Quantity')
