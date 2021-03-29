#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

#params = {'account': 'zumlic92476@chacuo.net', 'password': 'zumlic92476'}

def getCookie():

    try:
        r = requests.post("http://www.zimuzu.tv/User/Login/ajaxLogin", params)
    except requests.exceptions.RequestException as err:
        print(err)
        return False

    return r.cookies

if __name__=='__main__':
    print(getCookie().get_dict())
