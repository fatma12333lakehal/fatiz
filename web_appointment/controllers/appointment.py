# controllers/main.py

from odoo import http
from odoo.http import request
from datetime import datetime


class AppointmentController(http.Controller):

    @http.route('/appointment', type='http', auth='public', website=True)
    def appointment_page(self, **kw):

        employees = request.env['hr.employee'].sudo().search([])

        appointments = request.env['website.appointment'].sudo().search([])

        events = []

        for rec in appointments:

            weekday = rec.date.weekday()

            # convert monday=0 to sunday=0
            weekday = (weekday + 1) % 7

            events.append({
                'employee': rec.employee_id.name,
                'date': str(rec.date),
                'time': int(rec.time),
                'partner': rec.partner_id.name,
                'weekday': weekday,
            })

        return request.render(
            'web_appointment.appointment_template',
            {
                'employees': employees,
                'events': events,
            }
        )

    @http.route('/appointment/submit', type='json', auth='public', csrf=False)
    def appointment_submit(
            self,
            name=None,
            email=None,
            phone=None,
            employee_id=None,
            date=None,
            time=None,
            location=None
    ):

        partner = request.env['res.partner'].sudo().create({
            'name': name,
            'email': email,
            'phone': phone,
        })

        request.env['website.appointment'].sudo().create({
            'name': f'Appointment - {name}',
            'partner_id': partner.id,
            'employee_id': int(employee_id),
            'date': date,
            'time': float(time),
            'location': location,
        })

        return {
            'success': True
        }