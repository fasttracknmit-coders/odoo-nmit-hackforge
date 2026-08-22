{
<<<<<<< HEAD
    'name': 'Dayflow HR',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'HR Payroll and Leave Management',
    'depends': ['base'],
    'data': [
        'views/payroll_views.xml',
    ],
    'installable': True,
    'application': True,
=======
    "name": "Dayflow HR",
    "version": "19.0.1.0.0",
    "summary": "Human Resource Management System",
    "description": """
        Dayflow - Human Resource Management System
    """,
    "category": "Human Resources",
    "author": "FastTrack NMIT",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/employee_views.xml",
    ],
    "installable": True,
    "application": True,
>>>>>>> ec9e89a38d1184d5790d5284a1b16a1daafc9be8
}
'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/employee_views.xml',
        'views/payroll_views.xml',
        'reports/payroll_report.xml',  # <--- Add this line here
    ],