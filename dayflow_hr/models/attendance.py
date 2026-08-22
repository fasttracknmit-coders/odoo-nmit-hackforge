from odoo import models, fields, api


class DayflowAttendance(models.Model):
    _name = "dayflow.attendance"
    _description = "Dayflow Employee Attendance"
    _order = "date desc"

    employee_id = fields.Many2one(
        "dayflow.employee",
        string="Employee",
        required=True
    )

    date = fields.Date(
        string="Date",
        required=True,
        default=fields.Date.today
    )

    check_in = fields.Datetime(
        string="Check In"
    )

    check_out = fields.Datetime(
        string="Check Out"
    )

    status = fields.Selection(
        [
            ("present", "Present"),
            ("absent", "Absent"),
            ("half_day", "Half Day"),
            ("leave", "Leave"),
        ],
        string="Status",
        default="present",
        required=True
    )

    worked_hours = fields.Float(
        string="Worked Hours",
        compute="_compute_worked_hours",
        store=True
    )

    late_minutes = fields.Integer(
        string="Late Minutes",
        default=0
    )

    remarks = fields.Text(
        string="Remarks"
    )

    @api.depends("check_in", "check_out")
    def _compute_worked_hours(self):
        for record in self:
            if record.check_in and record.check_out:
                difference = record.check_out - record.check_in
                record.worked_hours = difference.total_seconds() / 3600
            else:
                record.worked_hours = 0.0