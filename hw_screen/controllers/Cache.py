# -*- coding: utf-8 -*-
##############################################################################
#
#    TL Technology
#    Copyright (C) 2019 ­TODAY TL Technology (<https://www.posodoo.com>).
#    Odoo Proprietary License v1.0 along with this program.
#
##############################################################################

from odoo import http, _

try:
    from xmlrpc import client as xmlrpclib
except ImportError:
    import xmlrpclib

try:
    from queue import Queue
except ImportError:
    from Queue import Queue  # pylint: disable=deprecated-module

# TODO: chef screens
from odoo.addons.web.controllers import main as web


import json
import logging

_logger = logging.getLogger(__name__)

class CacheController(web.Home):

    def __init__(self):
        self.keys = {}

    @http.route('/hw_cache/save', type="json", auth='none', cors='*')
    def saveIotCache(self, key, value):
        _logger.info('[saveIotCache] key %s' % key)
        self.keys[key] = value
        return json.dumps({'state': 'succeed', 'values': {}})

    @http.route('/hw_cache/get', type="json", auth='none', cors='*')
    def getIotCache(self, key):
        _logger.info('[getIotCache] key %s' % key)
        if (self.keys.get(key, None)):
            return self.keys[key]
        else:
            return None

    @http.route('/hw_cache/reset', type="json", auth='none', cors='*')
    def resetIotCache(self):
        _logger.info('[resetIotCache] reset')
        self.keys = {}
        return True


