# -*- coding: utf-8 -*
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
from odoo.addons.hw_drivers.controllers import proxy

import json
import logging

_logger = logging.getLogger(__name__)


class SyncDrive(Thread):

    """
    Any datas sync between session stored to Queue and by config_id
    period 2 seconds, pos sessions auto call to this controller and get new updates datas
    Key point of queue is Database
    Each Database have config ID and Arrays Datas
    Example:
        Queue = {
            'db1': {
                'config_1': [data1, data2 ....etc],
                'config_2': [data1, data2 ....etc],
            },
            'db2': {
                'config_1': [data1, data2 ....etc],
                'config_2': [data1, data2 ....etc],
            }
        }
    Each POS Config save total maximum 2000 datas, if bigger than or equal 2000, we remove datas for reduce RAM
    TODO: If Odoo-Server restart: all datas sync will lose (*****)
    """

    def __init__(self):
        Thread.__init__(self)
        self.chef_login = {}
        self.lock = Lock()
        self.sync_datas = {}
        self.total_notification_by_config_id = {}

    def register_point(self, database, config_ids):
        if not self.sync_datas.get(database, None):
            self.sync_datas[database] = {}
            self.total_notification_by_config_id[database] = {}
            for config_id in config_ids:
                if not self.sync_datas[database].get(config_id, None):
                    self.sync_datas[database][config_id] = Queue()
                    self.total_notification_by_config_id[database][config_id] = 0
        return True

    def save_notification(self, database, send_from_config_id, config_ids, message):
        database_datas = self.sync_datas.get(database)
        if not database_datas:
            self.register_point(database, config_ids)
        databases = self.sync_datas.get(database)
        for config_id, values in databases.items():
            if config_id != send_from_config_id and config_id in config_ids:
                databases[config_id].put((time.time(), config_id, message))
                _logger.info('{sync} save notification to config_id %s' % config_id)
                if not self.total_notification_by_config_id.get(database, None):
                    self.total_notification_by_config_id[database] = {}
                if not self.total_notification_by_config_id[database].get(config_id, None):
                    self.total_notification_by_config_id[database][config_id] = 0
                self.total_notification_by_config_id[database][config_id] += 1
                # TODO: if total notifications of config_id bigger than 2000, we clear data for reduce RAM of system
                if self.total_notification_by_config_id[database][config_id] >= 2000:
                    self.sync_datas[database][config_id].get()
        return True

    def get_notifications(self, database, config_id):
        result_list = []
        if not self.sync_datas.get(database, None):
            self.sync_datas[database] = {}
            self.sync_datas[database][config_id] = Queue()
            return []
        else:
            if not self.sync_datas[database].get(config_id):
                self.sync_datas[database][config_id] = Queue()
            while not self.sync_datas[database][config_id].empty():
                result_list.append(self.sync_datas[database][config_id].get())
            if not self.total_notification_by_config_id.get(database, None):
                self.total_notification_by_config_id[database] = {}
            if not self.total_notification_by_config_id[database].get(config_id, None):
                self.total_notification_by_config_id[database][config_id] = 0
            self.total_notification_by_config_id[database][config_id] -= len(result_list)
        return result_list

driver = SyncDrive()


class SyncController(proxy.ProxyController):

    @http.route('/pos/register/sync', type="json", auth='none', cors='*')
    def register_sync(self, database, config_id, config_ids):
        driver.register_point(database, config_ids)
        values = driver.get_notifications(database, config_id)
        return json.dumps({'state': 'succeed', 'values': values})

    @http.route('/pos/save/sync', type="json", auth='none', cors='*')
    def save_sync(self, database, send_from_config_id, config_ids, message):
        driver.save_notification(database, send_from_config_id, config_ids, message)
        return json.dumps({'state': 'succeed', 'values': {}})

    @http.route('/pos/passing/login', type='json', auth='none', cors='*')
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
