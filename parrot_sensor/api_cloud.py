#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GNU AFFERO GENERAL PUBLIC LICENSE
    Version 3, 19 November 2007
"""
import requests


class ApiCloud(object):
    """ Flower Power API Cloud """
    url = 'https://api-flower-power-pot.parrot.com'
    SUCCESS = 200

    def __init__(self, api_key, api_secret):
        self._credentials = {'client_id': api_key, 'client_secret': api_secret}
        self.__logged = False
        self.__token = {}

    def login(self, username, password):
        self._credentials['username'] = username
        self._credentials['password'] = password
        options = self._credentials
        options['grant_type'] = 'password'

        req = requests.post(ApiCloud.url + '/user/v1/authenticate', data=options)

        if req.status_code == ApiCloud.SUCCESS:
            self.__logged = True
            self.__token = req.json()
            print "Login successful!"
            return True
        else:
            self.__logged = False
            print "Login Failure: " + req.json()['error']
            return False

    def get_sensor_data_sync(self):
        if not self.__logged:
            return False

        path = '/garden/v2/configuration'
        req = requests.get(ApiCloud.url + path,
                           headers={'Authorization': 'Bearer ' + self.__token['access_token']},
                           params={'include_s3_urls': 1})
        return ApiCloud.__return_result(path, req)

    def get_samples_location(self, identifier, form_date_time, to_date_time):
        if not self.__logged:
            return False

        path = '/sensor_data/v6/sample/location/' + identifier
        req = requests.get(ApiCloud.url + path,
                           headers={'Authorization': 'Bearer ' + self.__token['access_token']},
                           params={'from_datetime_utc': form_date_time, 'to_datetime_utc': to_date_time})
        return ApiCloud.__return_result(path, req)

    @staticmethod
    def __return_result(path, req):
        if req.status_code == ApiCloud.SUCCESS:
            return req.json()
        else:
            return req.status_code, "Error: " + path

    def __str__(self):
        dest = "User: " + self._credentials['username'] + "\n"
        dest += "Logged: " + str(self.__logged)
        return dest
