# Copyright (c) 2021 tapiocode
# https://github.com/tapiocode
# MIT License

from esp8266 import esp8266

SSID = ''
PASSWORD = ''

if SSID == '' or PASSWORD == '':
    print('Please set network name (SSID) and password')
else:
    print('Starting')
    esp = esp8266(tx_pin = 0, rx_pin = 1)
    # esp.set_debug(False)

    is_connected = esp.connect(ssid = SSID, password = PASSWORD)

    if is_connected:
        print('Doing HTTP GET')
        response = esp.do_http_request(
            method = 'GET',
            host = 'httpbin.org',
            path = '/get'
        )
        esp.disconnect()

        print('Done')
        if response:
            code, headers, body = response
            print('--------------')
            print('Response code:')
            print(code)
            print('--------------')
            print('Response headers:')
            print(headers)
            print('--------------')
            print('Response body:')
            print(body)
            print('--------------')
        else:
            print('Did not get response')
