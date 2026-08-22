"""
Dayflow HR Intelligence Rules Engine

This module contains deterministic HR rules.
It does not call Gemini or access the Odoo database directly.

The rules accept simple Python data structures so they can be
connected to the actual Odoo models later.
"""


def detect_attendance_anomalies(attendance_records, late_threshold=3):
    """
    Detect employees with repeated late check-ins.

    Expected input:
    [
        {
            "employee_id": 104,
            "employee_name": "Employee 104",
            "late": True
        },
        ...
    ]
    """

    late_counts = {}

    for record in attendance_records:
        employee_id = record.get("employee_id")

        if not employee_id:
            continue

        if record.get("late"):
            late_counts[employee_id] = late_counts.get(employee_id, 0) + 1

    alerts = []

    for employee_id, count in late_counts.items():
        if count >= late_threshold:
            alerts.append({
                "type": "attendance",
                "severity": "high",
                "employee_id": employee_id,
                "title": "Repeated late check-ins",
                "message": (
                    f"Employee {employee_id} has "
                    f"{count} late check-ins."
                ),
            })

    return alerts


def detect_leave_conflicts(leave_records, conflict_threshold=3):
    """
    Detect departments where too many employees request leave
    on the same date.

    Expected input:
    [
        {
            "employee_id": 101,
            "department": "Engineering",
            "date": "2026-08-25",
            "status": "pending"
        },
        ...
    ]
    """

    leave_counts = {}

    for record in leave_records:
        department = record.get("department")
        date = record.get("date")
        status = record.get("status")

        if not department or not date:
            continue

        if status not in ("pending", "approved"):
            continue

        key = (department, date)

        leave_counts[key] = leave_counts.get(key, 0) + 1

    alerts = []

    for (department, date), count in leave_counts.items():
        if count >= conflict_threshold:
            alerts.append({
                "type": "leave",
                "severity": "medium",
                "title": "Leave concentration detected",
                "message": (
                    f"{count} employees from {department} "
                    f"have leave on {date}."
                ),
                "department": department,
                "date": date,
            })

    return alerts


def detect_payroll_risks(payroll_records):
    """
    Detect payroll records that contain attendance or leave
    discrepancies.

    Expected input:
    [
        {
            "employee_id": 104,
            "attendance_discrepancy": True,
            "leave_discrepancy": False
        },
        ...
    ]
    """

    alerts = []

    for record in payroll_records:
        employee_id = record.get("employee_id")

        if not employee_id:
            continue

        attendance_issue = record.get(
            "attendance_discrepancy",
            False
        )

        leave_issue = record.get(
            "leave_discrepancy",
            False
        )

        if attendance_issue or leave_issue:
            alerts.append({
                "type": "payroll",
                "severity": "high",
                "employee_id": employee_id,
                "title": "Payroll discrepancy",
                "message": (
                    f"Employee {employee_id} has a "
                    "record discrepancy that may affect payroll."
                ),
            })

    return alerts


def generate_all_insights(
    attendance_records=None,
    leave_records=None,
    payroll_records=None,
):
    """
    Run all Dayflow HR intelligence rules.
    """

    attendance_records = attendance_records or []
    leave_records = leave_records or []
    payroll_records = payroll_records or []

    insights = []

    insights.extend(
        detect_attendance_anomalies(attendance_records)
    )

    insights.extend(
        detect_leave_conflicts(leave_records)
    )

    insights.extend(
        detect_payroll_risks(payroll_records)
    )

    return insights