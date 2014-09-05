#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests

ENDPOINTS = {
        'connections': {'name': '/connections', 'method': 'get'},
        'completion': {'name': '/completion', 'method': 'get'},
        'config':
        {
            'get': {'name': '/config', 'method': 'get'},
            'sync': {'name': '/config/sync', 'method': 'get'},
            'new': {'name': '/config', 'method': 'post'},
        },
        'errors':
        {
            'get': {'name': '/errors', 'method': 'get'},
            'new': {'name': '/error', 'method': 'post'},
            'clear': {'name': '/error/clear', 'method': 'post'},
        },
        'events': {'name': '/events', 'method': 'get'},
        'discovery':
        {
            'get': {'name': '/discovery', 'method': 'get'},
            'new': {'name': '/discovery/hint', 'method': 'post'},
        },
        'lang': {'name': '/lang', 'method': 'get'},
        'need': {'name': '/need', 'method': 'get'},
        'nodeid': {'name': '/nodeid', 'method': 'get'},
        'repo':
        {
            'get': {'name': '/model', 'method': 'get'},
            'version': {'name': '/model/version', 'method': 'get'},
            'override': {'name': '/model/override', 'method': 'post'},
        },
        'report': {'name': '/report', 'method': 'get'},
        'stats': {'name': '/stats/node', 'method': 'get'},
        'system':
        {
            'get': {'name': '/system', 'method': 'get'},
            'reset': {'name': '/reset', 'method': 'post'},
            'restart': {'name': '/restart', 'method': 'post'},
            'shutdown': {'name': '/shutdown', 'method': 'post'},
            'upgrade': {'name': '/upgrade', 'method': 'get'},
            'version': {'name': '/version', 'method': 'get'},
        }, 
    }

class SyncthingClient:

    def __init__(self, apikey='', url='http://localhost:8080'):
        self.syncthing_url = '%s/rest' % (url)
        self.syncthing_apikey = apikey
        self.syncthing_config = self.get_config()
        self.syncthing_apikey = self.get_api_key()

    def get_api_key(self):
        return self.get_config()['GUI'].get('APIKey', '')

    def get_connections(self):
        return self.api_call(ENDPOINTS['connections'], False, False)

    def get_completion(self, node, repo):
        return self.api_call(ENDPOINTS['completion'], {'node': node, 'repo': repo}, False)

    def get_config(self):
        return self.api_call(ENDPOINTS['config']['get'], False, False)

    def get_errors(self):
        return self.api_call(ENDPOINTS['errors']['get'], False, False)

    def get_events(self):
        return self.api_call(ENDPOINTS['events'], False, False)
        
    def get_dir_path(self, repo_id):
        repos = self.syncthing_config['Repositories']
        path = [repo['Directory'] for repo in repos if repo['ID'] == repo_id]
        return path[0] if path else ''

    def get_discovery(self):
        return self.api_call(ENDPOINTS['discovery']['get'], False, False)

    def get_lang(self):
        return self.api_call(ENDPOINTS['lang'], False, False)

    def get_need(self):
        return self.api_call(ENDPOINTS['need'], False, False)
        
    def get_node_name(self, node_id):
        nodes = self.syncthing_config['Nodes']
        name = [node['Name'] for node in nodes if node['NodeID'] == node_id]
        return name[0] if name else ''
        
    def get_node_id(self, node_name):
        nodes = self.syncthing_config['Nodes']
        id = [node['NodeID'] for node in nodes if node['Name'] == node_name]
        return id[0] if id else ''

    def get_node_stats(self):
        return self.api_call(ENDPOINTS['stats'], False, False)

    def get_repo(self, repository=False):
        repo = {'repo': repository if repository else 'default'}
        return self.api_call(ENDPOINTS['repo']['get'], repo, False)

    def get_repositories(self):
        return self.get_config()['Repositories']

    def get_repo_version(self, repository=False):
        repo = {'repo': repository if repository else 'default'}
        return self.api_call(ENDPOINTS['repo']['version'], repo, False)

    def get_report(self):
        return self.api_call(ENDPOINTS['report'], False, False)

    def get_self_id(self):
        return self.get_system()['myID']

    def get_sync(self):
        return self.api_call(ENDPOINTS['config']['sync'], False, False)

    def get_system(self):
        return self.api_call(ENDPOINTS['system']['get'], False, False)

    def get_upgrade(self):
        return self.api_call(ENDPOINTS['system']['upgrade'], False, False)

    def get_version(self):
        return self.api_call(ENDPOINTS['system']['version'], False, False)

    def new_error(self, error_body):
        return self.api_call(ENDPOINTS['errors']['new'], {'error': error_body}, False)

    def clear_errors(self):
        return self.api_call(ENDPOINTS['errors']['clear'], False, False)

    def new_discovery_hint(self, node, addr):
        return self.api_call(ENDPOINTS['discovery']['new'], {'node': node, 'addr': addr}, False)

    def new_config(self, config):
        return self.api_call(ENDPOINTS['config']['new'], config, False)

    def new_repo_version(self, repo, version):
        return self.api_call(ENDPOINTS['repo']['override'], {'repo': repo, 'version': version}, False)

    def restart(self):
        return self.api_call(ENDPOINTS['system']['restart'], False, False)

    def reset(self):
        return self.api_call(ENDPOINTS['system']['reset'], False, False)

    def shutdown(self):
        return self.api_call(ENDPOINTS['system']['shutdown'], False, False)

    def api_call(self, endpoint, request_body=False, params=False):
        url = '%s%s' % (self.syncthing_url, endpoint['name'])

        method = endpoint['method']
        headers = {'Content-Type': 'application/json', 'User-Agent': 'Syncthing Python client', 'X-API-Key': self.syncthing_apikey}

        if request_body:
            keys = request_body.keys()

            key = keys[0]
            keys.remove(key)

            url += '?%s=%s' % (key, request_body[key])

            for key in keys:
                url += '&%s=%s' % (key, request_body[key])

        if method is 'get':
            try:
                r = requests.get(url, headers=headers)
            except requests.packages.urllib3.exceptions.ProtocolError:
                print('Syncthing is not responding. Exiting.')
                sys.exit()

        elif method is 'post':
            try:
                r = requests.post(url, headers=headers)
            except requests.packages.urllib3.exceptions.ProtocolError:
                print('Syncthing is not responding. Exiting.')
                sys.exit()
        else:
            raise 'Unknown call method: %s' % method

        if method == 'get' and endpoint['name'] != '/version':
            return r.json()

        if endpoint['name'] == '/version':
            return r.content
