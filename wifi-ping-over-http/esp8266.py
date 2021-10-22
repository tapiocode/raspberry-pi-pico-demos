# Copyright (c) 2021 tapiocode
# https://github.com/tapiocode
# MIT License

import time
from machine import UART, Pin

STATUS_OK = b'OK\r\n'
STATUS_ERROR = b'ERROR\r\n'
STATUS_WIFI_GOT_IP = b'WIFI GOT IP\r\n'

CONNECTION_ATTEMPTS_MAX = 6 # Attempts before aborting

UART_TXBUF_LENGTH = 1024
UART_RXBUF_LENGTH = 1024 * 2

class esp8266:

    _debug: bool = True
    _rx_data: bytes
    _uart_obj: UART

    def __init__(
        self,
        uart_port: int = 0,
        baudrate: int = 115200,
        tx_pin: int = 0,
        rx_pin: int = 1
    ):
        self._uart_obj = UART(
            uart_port,
            baudrate = baudrate,
            tx = Pin(tx_pin),
            rx = Pin(rx_pin),
            txbuf = UART_TXBUF_LENGTH,
            rxbuf = UART_RXBUF_LENGTH
        )

    # Setting _debug to False disables log printing
    def set_debug(self, debug: bool) -> None:
        self._debug = debug

    def connect(self, ssid: str, password: str, max_attempts: int = CONNECTION_ATTEMPTS_MAX) -> bool:
        self._log('Trying to join WiFi access point')
        self._set_wifi_mode()
        while max_attempts > 0:
            self._send_at_command(f'AT+CWJAP_CUR="{ssid}","{password}"', print_log = False)
            if STATUS_WIFI_GOT_IP in self._read_rx_data():
                self._log('Got IP, waiting...')
                # Apparently at this point a delay is needed
                i = 0
                while i < 10:
                    i += 1
                    self._wait()
                return True
            else:
                self._log('Trying...')
                max_attempts -= 1
            time.sleep(5)

        self._log('Maximum attempts reached, aborting')
        return False

    def disconnect(self) -> bool:
        self._log('Disconnecting')
        self._send_at_command('AT+CWQAP')

    def do_http_request(
        self,
        method: str,
        host: str,
        path: str,
        user_agent: str = 'esp8266.py/0.1',
        port: int = 80
    ) -> tuple[str, list[str], str]:
        self._log('Doing an HTTP request')
        header_str = ''.join([
            f'{method} {path} HTTP/1.1\r\n',
            f'Host: {host}\r\n',
            f'User-Agent: {user_agent}\r\n',
            '\r\n'
        ])
        self._log(header_str)
        self._open_tcp_connection(host, port)
        self._send_at_command(f'AT+CIPSEND={len(header_str)}', 1)
        self._send_at_command(header_str, 1)
        response = self._read_rx_data()
        self._send_at_command('AT+CIPCLOSE')

        if response != None:
            return self._parse_http_response(response)
        else:
            self._log('Did not get response')
            return None

    def _open_tcp_connection(self, host: str, port: int) -> bool:
        self._log('Opening TCP')
        self._send_at_command(f'AT+CIPSTART="TCP","{host}",{str(port)}', 3)
        while True:
            result = self._read_rx_data()
            if STATUS_OK in result:
                self._log('Opened TCP')
                return True
            self._wait()

    def _parse_http_response(self, response) -> tuple[str, list[str], str]:
        parts = str(response).partition('+IPD,')
        if parts[1] == '+IPD,':
            headers_raw, response_body = parts[2].split(r'\r\n\r\n', 1)
            response_headers = headers_raw.split(r'\r\n')
            response_code = response_headers[0].split(' ', 1)[1]
            del response_headers[0]
            return response_code, response_headers, response_body
        else:
            self._log('Could not parse response')
            return None

    def _read_rx_data(self) -> bytes:
        while self._uart_obj.any() > 0:
            self._rx_data += self._uart_obj.read(UART_RXBUF_LENGTH)
        return self._rx_data

    def _send_at_command(self, atCommand: str, delay = 0, print_log = True) -> None:
        if print_log:
            self._log(f'Command: {atCommand}')
        self._uart_obj.write(b'{}\r\n'.format(atCommand))
        self._rx_data = bytes()
        time.sleep(delay)

    def _set_wifi_mode(self, mode: int = 3) -> bool:
        self._send_at_command(f'AT+CWMODE_CUR={mode}')
        return STATUS_OK in self._read_rx_data()

    def _wait(self) -> None:
        self._log('.')
        time.sleep(1)

    def _log(self, message: str) -> None:
        if self._debug:
            print('ESP8266: ' + message)
