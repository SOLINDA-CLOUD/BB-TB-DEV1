from odoo import fields, models, api, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    class_product = fields.Selection([('normal', 'Normal'),('sale','Sale')], string='Class')
    brand = fields.Many2one('product.brand', string='Brand')
    stock_type = fields.Many2one('stock.type', string='Stock Type')

class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product Brand'

    name = fields.Char(string='Name')

class StockType(models.Model):
    _name = 'stock.type'
    _description = 'Stock Type'

    name = fields.Char(string='Name')