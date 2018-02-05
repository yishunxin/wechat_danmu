# -*- coding:utf-8 -*-

import requests
from gs.conf import wx
import json
import logging

logger = logging.getLogger('common')


def get_access_token():
    access_token = ''
    if access_token:
        return access_token
    access_token = refresh_access_token()
    return access_token


def refresh_access_token():
    url = "https://{}/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(wx.API_HOST, wx.APPID,
                                                                                            wx.APPSECRET)
    res = requests.get(url)
    data = json.loads(res.content)
    if 'errcode' in data and data['errcode'] > 0:
        logger.error("get weixin access token error, errcode[%s] errmsg[%s]", data['errcode'], data['errmsg'])
        return False
    access_token = data['access_token']
    expires_in = data['expires_in']
    return access_token


def create_menu():
    access_token = get_access_token()
    url = "https://{}/cgi-bin/menu/create?access_token={}".format(wx.API_HOST, access_token)
    print json.dumps(wx.MENU, ensure_ascii=False).encode('utf8', 'ignore')
    res = requests.post(url, data=json.dumps(wx.MENU, ensure_ascii=False).encode('utf8', 'ignore'),
                        headers={'content-type': 'application/json; charset=utf8'})
    print res.content
    return True


def delete_menu():
    access_token = get_access_token()
    url = "https://{}/cgi-bin/menu/delete?access_token={}".format(wx.API_HOST, access_token)
    res = requests.get(url)
    print res.content
    return True


def get_users():
    access_token = get_access_token()
    url = "https://{}/cgi-bin/user/get?access_token={}".format(wx.API_HOST, access_token)
    res = requests.get(url)
    data = json.loads(res.content)
    if 'errcode' in data and data['errcode'] > 0:
        logger.error("get users fail, errcode[%s], errmsg[%s]", data['errcode'], data['errmsg'])
        return False
    return data


def get_user_info(openid):
    access_token = get_access_token()
    url = "https://{}/cgi-bin/user/info?access_token={}&openid={}&lang=zh_CN".format(wx.API_HOST, access_token, openid)
    res = requests.get(url)
    return json.loads(res.content)


def send_template_message(msg):
    logger.info('----------msg------------------')
    logger.info(msg)
    access_token = get_access_token()
    url = "https://{}/cgi-bin/message/template/send?access_token={}".format(wx.API_HOST, access_token)
    res = requests.post(url, data=json.dumps(msg, ensure_ascii=False).encode('utf8', 'ignore'),
                        headers={'content-type': 'application/json; charset=utf8'})
    content = json.loads(res.content)
    if content["errcode"] == 40001:
        refresh_access_token()
        access_token = get_access_token()
        url = "https://{}/cgi-bin/message/template/send?access_token={}".format(wx.API_HOST, access_token)
        res = requests.post(url, data=json.dumps(msg, ensure_ascii=False).encode('utf8', 'ignore'),
                            headers={'content-type': 'application/json; charset=utf8'})
    logger.info(res.content)
    return True
