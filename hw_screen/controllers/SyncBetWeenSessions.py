# -*- coding: utf-8 -*-
##############################################################################
#
#    TL Technology
#    Copyright (C) 2019 ­TODAY TL Technology (<https://www.posodoo.com>).
#    Odoo Proprietary License v1.0 along with this program.
#
##############################################################################
import time
from threading import Thread, Lock
from odoo import http, _
import os
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


class SyncDrive(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.chef_login = {}
        self.lock = Lock()
        self.sync_datas = {}

    def register_point(self, database, bus_id, user_id):
        if not self.sync_datas.get(database, None):
            self.sync_datas[database] = {}
            self.sync_datas[database][bus_id] = {}
            self.sync_datas[database][bus_id][user_id] = Queue()
        else:
            if not self.sync_datas[database].get(bus_id, None):
                self.sync_datas[database][bus_id] = {}
                self.sync_datas[database][bus_id][user_id] = Queue()
            else:
                if not self.sync_datas[database][bus_id].get(user_id, None):
                    self.sync_datas[database][bus_id][user_id] = Queue()
        return True

    def save_notification(self, database, bus_id, user_id, message):
        database_datas = self.sync_datas[database]
        bus_point = database_datas[bus_id]
        for cache_user_id, values in bus_point.items():
            if user_id != cache_user_id:
                bus_point[cache_user_id].put((time.time(), user_id, message))
        return True

    def get_notifications(self, database, bus_id, user_id):
        result_list = []
        if not self.sync_datas.get(database, None):
            self.register_point(database, bus_id, user_id)
            return []
        else:
            while not self.sync_datas[database][bus_id][user_id].empty():
                result_list.append(self.sync_datas[database][bus_id][user_id].get())
        return result_list


driver = SyncDrive()

class SyncController(web.Home):

    @http.route('/pos/register/sync', type="json", auth='none', cors='*')
    def register_sync(self, database, bus_id, user_id):
        # TODO: each bus_id we stores all event of pos sessions
        driver.register_point(database, bus_id, user_id)
        return json.dumps({'state': 'succeed', 'values': {}})

    @http.route('/pos/save/sync', type="json", auth='none', cors='*')
    def save_sync(self, database, bus_id, user_id, message):
        # TODO: save all transactions event from pos sessions
        driver.save_notification(database, bus_id, user_id, message)
        return json.dumps({'state': 'succeed', 'values': {}})

    @http.route('/pos/get/sync', type="json", auth='none', cors='*')
    def get_sync(self, database, bus_id, user_id):
        # TODO: get any events change from another pos sessions
        values = driver.get_notifications(database, bus_id, user_id)
        return json.dumps({'state': 'succeed', 'values': values})

    @http.route('/pos/passing/login', type='http', auth='none', cors='*')
    def pos_login(self):
        return "ping"

    @http.route('/pos/display-chef-screen', type="json", auth='none', cors='*')
    def display_chef_screen(self, link, database, login, password):
        try:
            driver.xmlrpc_url = url_8 = '%s/xmlrpc/2/' % link
            driver.xmlrpc_common = xmlrpclib.ServerProxy(url_8 + 'common')
            driver.xmlrpc_object = xmlrpclib.ServerProxy(url_8 + 'object')
            driver.uid = driver.xmlrpc_common.login(database, login, password)
            if driver.uid:
                driver.chef_login['link'] = link
                driver.chef_login['database'] = database
                driver.chef_login['login'] = login
                driver.chef_login['password'] = password
                return json.dumps({'state': 'succeed', 'values': driver.uid})
            else:
                return json.dumps({'state': 'fail', 'values': 'login fail'})
        except:
            return json.dumps({'state': 'fail', 'values': 'login fail'})

    @http.route('/pos/get-login-chef', type='json', auth='none')
    def get_login_chef_screen(self):
        return driver.chef_login

    @http.route('/pos/reboot', type='json', auth='none', cors='*')
    def reboot(self):
        os.system('sudo reboot now')
        return json.dumps({'state': 'succeed', 'values': 'OK'})
