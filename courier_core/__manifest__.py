{
    'name': 'Courier Core',
    'version': '18.0.1.0.0',
    'category': 'Operations',
    'summary': 'Incident Log System for BeraniExpress',
    'description': '''
        Courier Core - Incident Log System
        ===================================

        This module provides incident tracking and management for
        BeraniExpress courier services.

        Features:
        - Incident logging with severity levels
        - Workflow-based incident resolution (Draft -> Follow-up -> Done)
        - Customer and shipment tracking
    ''',
    'author': 'BeraniExpress',
    'website': 'https://github.com/yourusername/courier_core',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/courier_incident_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
