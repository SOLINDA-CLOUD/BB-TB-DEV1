# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'

    image = fields.Image(string='Fabric Swatch')

    @api.onchange('product_id')
    def _onchange_image(self):
        if self.product_id:
            self.image = ''
            if self.product_id.image_1920:
                self.image = self.product_id.image_1920
            self.image = self.image

class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    style_name = fields.Char(string='Style Name')
    department = fields.Char(string='Department')
    sub_department = fields.Char(string='Sub Department')
    request_detail_id = fields.Many2one(string='Original Sample', comodel_name='request.detail', ondelete='cascade')
    notes = fields.Html(string='Fit Notes')
    date_start = fields.Date(string='Transaction Date')

    @api.model
    def create(self, vals):
        res = super(PurchaseRequest, self).create(vals)
        res.name = self.env["ir.sequence"].next_by_code("purchase.request.seq")
        return res

class RequestDetail(models.Model):
    _name = 'request.detail'
    _description = 'Request Detail'

    name = fields.Char(string='Original Sample')
    sample_size = fields.Char(string='Sample Size')
    approved_size = fields.Char(string='Sample In Approved Size')
    sample_in_size = fields.Char(string='Please Make Sample In Size')
    fabric = fields.Char(string='Fabric')
    lining = fields.Char(string='Lining')
    
