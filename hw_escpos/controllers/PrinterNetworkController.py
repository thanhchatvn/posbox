# -*- coding: utf-8 -*-
from odoo import http
import logging
import json
from odoo.addons.hw_escpos.escpos.printer import Network
from odoo.addons.hw_drivers.controllers import proxy

import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import time

_logger = logging.getLogger(__name__)



# class EscposNetworkDriver(EscposDriver):
#
#     def print_network(self, receipt, proxy, name=None):
#         time.sleep(1)
#         printer_object = Network(proxy)
#         printer_object.open()
#         if printer_object:
#             printer_object.receipt(receipt)
#             printer_object.__del__()
#             return True
#         return False
#
#
# network_driver = EscposNetworkDriver()

class NetworkEscposProxy(proxy.ProxyController):

    @http.route('/hw_proxy/print_network', type='json', auth='none', cors='*')
    def epson_printing(self, receipt, proxy):
        time.sleep(3)
        _logger.info('[epson_printing] Begin')
        _logger.info('[epson_printing] proxy ip: %s' % proxy)
        printer_object = Network(proxy)
        printer_object.open()
        printResult = None
        if printer_object:
            printResult= printer_object.receipt(receipt)
            printer_object.__del__()
        _logger.info('[epson_printing] Result of Printer Network: %s' % printResult)
        return json.dumps({'state': 'succeed', 'values': printResult})

    def ping(self, host):
        param = '-n' if platform.system().lower()=='windows' else '-c'
        command = ['ping', param, '1', host]
        return subprocess.call(command) == 0

    @http.route('/hw_proxy/get_printers_status', type='json', auth='none', cors='*')
    def ping_printer(self, printer_ips=[]):
        _logger.info('ESCPOS: ping proxy %s' % printer_ips)
        values = {}
        for printer_ip in printer_ips:
            result = self.ping(printer_ip)
            _logger.info(result)
            if printer_ip:
                values[printer_ip] = 'Online'
            else:
                values[printer_ip] = 'Offline'
        return json.dumps({'state': 'succeed', 'values': values})
