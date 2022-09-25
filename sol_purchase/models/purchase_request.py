# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PatternAlteration(models.Model):
    _name = 'pattern.alteration'
    _description = 'Link Purchase Request and Pattern Alteration'

    parent_purchase_id = fields.Many2one('purchase.request', string='Request')
    pattern_id = fields.Many2one('purchase.request', string='Pattern Alteration')
    user_id = fields.Many2one('res.users', string='User Pattern Alteration')

class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'

    image = fields.Image(string='Fabric Swatch')
    department = fields.Char(string='Department')
    sub_department = fields.Char(string='Sub Department')

    @api.onchange('product_id')
    def _onchange_image(self):
        if self.product_id:
            self.image = ''
            if self.product_id.image_1920:
                self.image = self.product_id.image_1920
            self.image = self.image

class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    request_detail_id = fields.Many2one(string='Original Sample', comodel_name='request.detail', ondelete='cascade')
    notes = fields.Html(string='Fit Notes')
    date_start = fields.Date(string='Transaction Date')

    purchase_pattern_ids = fields.One2many('pattern.alteration', 'parent_purchase_id', string='Order History')
    revision_id = fields.Many2one('purchase.request', string='Purchase to Pattern Alteration')
    purchase_revision_id = fields.Many2one('purchase.request', string='Pattern Alteration')
    pattern_count = fields.Integer(string='Pattern', compute='_find_len')
    revisied = fields.Boolean(string='Revisied')
    rev = fields.Integer('Revision')

    @api.model
    def create(self, vals):
        res = super(PurchaseRequest, self).create(vals)
        res.name = self.env["ir.sequence"].next_by_code("purchase.request.seq")
        return res

    def _find_len(self):
        self.pattern_count = len(self.purchase_pattern_ids.ids)

    def create_pattern_alteration(self):
        # new_name = self.name[0: self.name.index(' - PTR ')] if self.revisied else self.name
        pattern = self.copy({
            # 'name': "%s - PTR %s"%(new_name,self.rev + 1),
            # 'rev': self.rev + 1,
            # 'revision_id' : self.id,
            # 'revisied': True
        })
        uid_id = self.env.user.id
        self.env['pattern.alteration'].create({
            'pattern_id': pattern.id,
            'user_id': uid_id,
            'parent_purchase_id': self.ids[0],
        })
        pattern.name = self.name + ' - PTR ' + str(len(self.purchase_pattern_ids.ids))
        
        action = self.env.ref('purchase_request.purchase_request_form_action').read()[0]
        if pattern:
            action['views'] = [(self.env.ref('purchase_request.view_purchase_request_form').id, 'form')]
            action['res_id'] = pattern.ids[0]
        else:
            action = {'type': 'ir.action.act_window_close'}
        return action
    
    def view_pattern_alteration(self):
        action = self.env.ref('purchase_request.purchase_request_form_action').read()[0]
        purchase_pattern_ids = self.mapped('purchase_pattern_ids.pattern_id')
        if len(purchase_pattern_ids) > 1: 
            action['domain'] = [('id', 'in', purchase_pattern_ids.ids)]
        elif purchase_pattern_ids:
            action['views'] = [
                (self.env.ref('purchase_request.view_purchase_request_form').id, 'form')
            ]
            action['res_id'] = purchase_pattern_ids.id
        return action

class RequestDetail(models.Model):
    _name = 'request.detail'
    _description = 'Request Detail'

    name = fields.Char(string='Original Sample')
    sample_size = fields.Char(string='Sample Size')
    approved_size = fields.Char(string='Sample In Approved Size')
    sample_in_size = fields.Char(string='Please Make Sample In Size')
    fabric = fields.Char(string='Fabric')
    lining = fields.Char(string='Lining')
    
