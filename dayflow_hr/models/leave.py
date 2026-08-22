from odoo import models, fields


class DayflowLeave(models.Model):
    _name = "dayflow.leave"
    _description = "Dayflow Employee Leave"
    _order = "date_from desc"

    employee_id = fields.Many2one(
        "dayflow.employee",
        string="Employee",
        required=True
    )

    leave_type = fields.Selection(
        [
            ("paid", "Paid Leave"),
            ("sick", "Sick Leave"),
            ("unpaid", "Unpaid Leave"),
        ],
        string="Leave Type",
        required=True,
        default="paid"
    )

    date_from = fields.Date(
        string="From Date",
        required=True
    )

    date_to = fields.Date(
        string="To Date",
        required=True
    )

    remarks = fields.Text(
        string="Remarks"
    )

    status = fields.Selection(
        [
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        string="Status",
        required=True,
        default="pending"
    )

    admin_comment = fields.Text(
        string="HR/Admin Comment"
    )