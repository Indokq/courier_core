from odoo import models, fields


class CourierCustomer(models.Model):
    _name = 'courier.customer'
    _description = 'Courier Customer'

    name = fields.Char(string='Name', required=True)
