{
    'name': 'Dayflow HRMS',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Dayflow Human Resource Management System',

    'description': """
        Dayflow - Human Resource Management System
        Employee Operations, Attendance, Leave and Payroll
    """,

    'author': 'Dayflow Team',
    'license': 'LGPL-3',

    'depends': [
        'base',
    ],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'views/employee_views.xml',
        'views/attendence_views.xml',
        'views/payroll_views.xml',
    ],

    'installable': True,
    'application': True,
}