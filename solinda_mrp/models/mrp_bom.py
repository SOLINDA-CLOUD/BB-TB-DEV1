from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    over_packaging = fields.Float(string='Over & Packaging')

class DptColor(models.Model):
    _name = 'dpt.color'
    _description = 'DPT Color'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')

    @api.constrains('name')
    def _check_code_unique(self):
        if self.name:
            ref_counts = self.search_count(
                [('name', '=', self.name), ('id', '!=', self.id)])
            if ref_counts > 0:
                raise ValidationError("Color already exists!")
        else:
            return

    @api.constrains('code')
    def _check_code_unique(self):
        if self.code:
            ref_counts = self.search_count(
                [('code', '=', self.code), ('id', '!=', self.id)])
            if ref_counts > 0:
                raise ValidationError("Code already exists!")
        else:
            return
