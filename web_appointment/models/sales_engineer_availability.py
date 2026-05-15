# models/availability.py

from odoo import models, fields


class SalesEngineerAvailability(models.Model):
    _name = 'sales.engineer.availability'
    _description = 'Sales Engineer Availability'

    employee_id = fields.Many2one('hr.employee', required=True)

    weekday = fields.Selection([
        ('0', 'Sunday'),
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
    ], required=True)

    hour_from = fields.Float(required=True)
    hour_to = fields.Float(required=True)

    location_id = fields.Many2one('res.partner')

    active = fields.Boolean(default=True)