from odoo import models, fields


class DayflowAIInsight(models.Model):
    _name = "dayflow.ai.insight"
    _description = "Dayflow AI HR Insight"
    _order = "create_date desc"

    name = fields.Char(
        string="Title",
        required=True
    )

    insight_type = fields.Selection(
        [
            ("attendance", "Attendance"),
            ("leave", "Leave"),
            ("payroll", "Payroll"),
        ],
        string="Type",
        required=True
    )

    severity = fields.Selection(
        [
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        string="Severity",
        required=True
    )

    message = fields.Text(
        string="Message",
        required=True
    )

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee"
    )

    department = fields.Char(
        string="Department"
    )

    status = fields.Selection(
        [
            ("open", "Open"),
            ("reviewed", "Reviewed"),
            ("resolved", "Resolved"),
        ],
        string="Status",
        default="open",
        required=True
    )

    source = fields.Selection(
        [
            ("rules", "Rules Engine"),
            ("gemini", "Gemini AI"),
        ],
        string="Source",
        default="rules"
    )