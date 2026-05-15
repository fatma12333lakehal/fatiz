# models/viewing_project.py

from odoo import models, fields


class ViewingProject(models.Model):
    _name = 'viewing.project'
    _description = 'Viewing Project'

    name = fields.Char(required=True)

    appointment_id = fields.Many2one('website.appointment')
    partner_id = fields.Many2one('res.partner')
    employee_id = fields.Many2one('hr.employee')

    location = fields.Char()

    stage = fields.Selection([
        ('draft', 'Draft'),
        ('visit', 'Site Visit'),
        ('negotiation', 'Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ], default='draft')

    note = fields.Text()