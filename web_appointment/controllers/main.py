# controllers/main.py

from odoo import http
from odoo.http import request


class AppointmentController(http.Controller):

    # ================= PAGE =================
    @http.route('/appointment', type='http', auth='public', website=True)
    def appointment_page(self, **kw):

        employee_id = kw.get('employee_id')

        employees = request.env['hr.employee'].sudo().search([])

        domain = []
        if employee_id:
            domain = [('employee_id', '=', int(employee_id))]

        availability = request.env['sales.engineer.availability'].sudo().search(domain)
        appointments = request.env['website.appointment'].sudo().search(domain)

        # ================= BOOKED EVENTS =================
        events = []

        for a in appointments:
            weekday = (a.date.weekday() + 1) % 7

            events.append({
                'employee_id': a.employee_id.id,
                'employee': a.employee_id.name,
                'weekday': weekday,
                'time': int(a.time),
                'duration': int(a.duration or 1),
                'partner': a.partner_id.name,
            })

        # ================= AVAILABLE SLOTS =================
        slots = []

        for av in availability:
            for h in range(int(av.hour_from), int(av.hour_to)):

                booked = False

                for e in events:
                    if (
                        e['employee_id'] == av.employee_id.id and
                        e['weekday'] == int(av.weekday) and
                        h >= e['time'] and
                        h < e['time'] + e['duration']
                    ):
                        booked = True
                        break

                slots.append({
                    'employee_id': av.employee_id.id,
                    'employee': av.employee_id.name,
                    'weekday': int(av.weekday),
                    'hour': h,
                    'booked': booked,
                })

        return request.render('web_appointment.appointment_template', {
            'employees': employees,
            'events': events,
            'slots': slots,
            'selected_employee': int(employee_id) if employee_id else False,
        })

    # ================= BOOK APPOINTMENT =================
    @http.route('/appointment/submit', type='json', auth='public', csrf=False, website=True)
    def appointment_submit(self, **kw):

        data = kw.get('params', kw)

        # ================= VALIDATION =================
        if not data:
            return {'success': False, 'message': 'No data received'}

        # ================= CREATE PARTNER =================
        partner = request.env['res.partner'].sudo().create({
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone'),
        })

        # ================= CREATE APPOINTMENT =================
        appointment = request.env['website.appointment'].sudo().create({
            'name': f"Appointment - {data.get('name')}",
            'partner_id': partner.id,
            'employee_id': int(data.get('employee_id')),
            'date': data.get('date'),
            'time': float(data.get('time')),
            'location': data.get('location'),
            'duration': float(data.get('duration', 1)),
        })

        # ================= CREATE VIEWING PROJECT =================
        project = request.env['project.project'].sudo().create({
            'name': f"Viewing - {data.get('name')}",
            'partner_id': partner.id,
        })

        appointment.project_id = project.id

        return {
            'success': True,
            'message': 'Booking successful',
            'appointment_id': appointment.id,
            'project_id': project.id,
        }