# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'POS RETAIL SYNC POINT && ESC/POS Hardware Driver',
    'category': 'Sales/Point of Sale',
    'sequence': 6,
    'website': 'https://www.odoo.com/page/point-of-sale-hardware',
    'summary': 'Hardware Driver for ESC/POS Printers and Cashdrawers',
    'description': """
1) SYNC POINT CONTROLLER
=======================


2) ESC/POS Hardware Driver
=======================

This module allows Odoo to print with ESC/POS compatible printers and
to open ESC/POS controlled cashdrawers in the point of sale and other modules
that would need such functionality.

""",
    'external_dependencies': {
        'python' : ['pyusb','pyserial','qrcode'],
    },
    'installable': False,
}
