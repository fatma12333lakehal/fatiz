# models/website_appointment.py

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class WebsiteAppointment(models.Model):
    _name = 'website.appointment'
    _description = 'Website Appointment'
    _rec_name = 'name'
    _order = 'date desc, time desc'

    name = fields.Char(
        required=True
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string='Sales Engineer',
        required=True
    )

    project_id = fields.Many2one(
        'project.project',
        string='Viewing Project'
    )

    calendar_event_id = fields.Many2one(
        'calendar.event',
        string='Calendar Event'
    )

    date = fields.Date(
        required=True
    )

    time = fields.Float(
        required=True
    )

    duration = fields.Float(
        default=1.0
    )

    location = fields.Char()

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], default='draft')

    notes = fields.Text()

    _sql_constraints = [
        (
            'unique_booking',
            'unique(employee_id,date,time)',
            'This slot is already booked.'
        )
    ]

    @api.constrains('time')
    def _check_time(self):

        for rec in self:

            if rec.time < 0 or rec.time > 24:
                raise ValidationError(
                    'Time must be between 0 and 24'
                )

    def action_confirm(self):

        for rec in self:
            rec.state = 'confirmed'

    def action_done(self):

        for rec in self:
            rec.state = 'done'

    def action_cancel(self):

        for rec in self:
            rec.state = 'cancel'