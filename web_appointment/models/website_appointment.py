# models/website_appointment.py

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class WebsiteAppointment(models.Model):
    _name = 'website.appointment'
    _description = 'Website Appointment'
    _rec_name = 'name'

    name = fields.Char(required=True)

    partner_id = fields.Many2one('res.partner', required=True)
    employee_id = fields.Many2one('hr.employee', required=True)

    project_id = fields.Many2one('project.project')
    duration = fields.Float(
        string="Duration (Hours)",
        default=1.0,
        help="Duration of the appointment in hours"
    )

    date = fields.Date(required=True)
    time = fields.Float(required=True)

    location = fields.Char()

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], default='draft')

    _sql_constraints = [
        ('unique_slot', 'unique(employee_id, date, time)',
         'This slot is already booked.')
    ]

    @api.constrains('time')
    def _check_time(self):
        for rec in self:
            if rec.time < 0 or rec.time > 24:
                raise ValidationError("Time must be between 0 and 24")

    # ACTIONS
    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})