from odoo import http
from odoo.http import request

from ..services.gemini_service import generate_hr_explanation


class DayflowAIController(http.Controller):

    @http.route(
        "/dayflow/ai/chat",
        type="json",
        auth="user",
        methods=["POST"],
    )
    def ai_chat(self, message=None, **kwargs):

        if not message:
            return {
                "success": False,
                "reply": "Please enter a question.",
            }

        message = message.lower().strip()

        Insight = request.env["dayflow.ai.insight"]

        # Attendance questions
        if any(word in message for word in [
            "attendance",
            "late",
            "check-in",
            "checkin",
        ]):
            records = Insight.search([
                ("insight_type", "=", "attendance"),
                ("status", "=", "open"),
            ], limit=10)

            if not records:
                return {
                    "success": True,
                    "reply": "No open attendance issues were found.",
                }

            lines = [
                f"Found {len(records)} attendance issue(s):"
            ]

            for record in records:
                employee = (
                    record.employee_id.name
                    if record.employee_id
                    else "Unknown employee"
                )

                lines.append(
                    f"- {record.name}: {employee} - "
                    f"{record.severity.upper()}"
                )

            raw_insight = "\n".join(lines)

            ai_reply = generate_hr_explanation(raw_insight)

            return {
                "success": True,
                "reply": ai_reply,
            }

        # Leave questions
        if "leave" in message or "holiday" in message:
            records = Insight.search([
                ("insight_type", "=", "leave"),
                ("status", "=", "open"),
            ], limit=10)

            if not records:
                return {
                    "success": True,
                    "reply": "No open leave conflicts were found.",
                }

            lines = [
                f"Found {len(records)} leave issue(s):"
            ]

            for record in records:
                lines.append(
                    f"- {record.name}: {record.message}"
                )

            raw_insight = "\n".join(lines)

            ai_reply = generate_hr_explanation(raw_insight)

            return {
                "success": True,
                "reply": ai_reply,
            }

        # Payroll questions
        if "payroll" in message or "salary" in message:
            records = Insight.search([
                ("insight_type", "=", "payroll"),
                ("status", "=", "open"),
            ], limit=10)

            if not records:
                return {
                    "success": True,
                    "reply": "No open payroll risks were found.",
                }

            lines = [
                f"Found {len(records)} payroll issue(s):"
            ]

            for record in records:
                employee = (
                    record.employee_id.name
                    if record.employee_id
                    else "Unknown employee"
                )

                lines.append(
                    f"- {record.name}: {employee} - "
                    f"{record.severity.upper()}"
                )

            raw_insight = "\n".join(lines)

            ai_reply = generate_hr_explanation(raw_insight)

            return {
                "success": True,
                "reply": ai_reply,
            }

        # General HR summary
        if any(word in message for word in [
            "summary",
            "problem",
            "issues",
            "insights",
            "report",
        ]):
            records = Insight.search([
                ("status", "=", "open"),
            ], limit=20)

            if not records:
                return {
                    "success": True,
                    "reply": "There are currently no open HR issues.",
                }

            attendance = sum(
                1 for r in records
                if r.insight_type == "attendance"
            )

            leave = sum(
                1 for r in records
                if r.insight_type == "leave"
            )

            payroll = sum(
                1 for r in records
                if r.insight_type == "payroll"
            )

            raw_insight = (
                "HR Action Center summary:\n"
                f"- Attendance issues: {attendance}\n"
                f"- Leave issues: {leave}\n"
                f"- Payroll issues: {payroll}\n"
                f"- Total open issues: {len(records)}"
            )

            ai_reply = generate_hr_explanation(raw_insight)

            return {
                "success": True,
                "reply": ai_reply,
            }

        return {
            "success": True,
            "reply": (
                "I can help with HR insights. "
                "Try asking about attendance, leave, "
                "payroll, or give me an HR summary."
            ),
        }