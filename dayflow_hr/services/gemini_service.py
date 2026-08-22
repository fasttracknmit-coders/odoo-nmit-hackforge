import os

try:
    from google import genai
except ImportError:
    genai = None


MODEL_NAME = "gemini-3.5-flash-lite"


def generate_hr_explanation(prompt):
    """
    Generate an HR explanation using Gemini.

    If Gemini is unavailable, return a deterministic fallback so
    the HR module continues to work during development/demo.
    """

    api_key = os.environ.get("GEMINI_API_KEY")

    # Gemini available
    if api_key and genai:
        try:
            client = genai.Client(api_key=api_key)

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )

            if response and response.text:
                return response.text.strip()

        except Exception as error:
            # Keep Odoo working even if Gemini is unavailable.
            print("Gemini unavailable:", error)

    # Development/demo fallback
    return (
        "HR Insight: Repeated late check-ins may indicate "
        "scheduling, workload, transportation, or employee "
        "engagement issues. HR should review the attendance "
        "pattern and discuss the situation with the employee."
    )


def generate_attendance_insight(employee_name, late_count):
    prompt = (
        f"Employee {employee_name} has {late_count} late check-ins. "
        "Provide one short, professional HR insight and one "
        "recommended action."
    )

    return generate_hr_explanation(prompt)


def generate_leave_insight(department, date, employee_count):
    prompt = (
        f"{employee_count} employees from {department} have leave "
        f"on {date}. Provide one short HR risk insight and one "
        "recommended action."
    )

    return generate_hr_explanation(prompt)


def generate_payroll_insight(employee_name):
    prompt = (
        f"Employee {employee_name} has a payroll-related "
        "attendance or leave discrepancy. Provide one short "
        "HR insight and one recommended action."
    )

    return generate_hr_explanation(prompt)