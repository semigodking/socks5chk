# tcpchk.py - simple tool to test TCP support of SOCKS5 proxy.
# Copyright (C) 2016-2017 Zhuofei Wang <semigodking@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy
# of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import print_function
import sys

if sys.platform == 'win32' and (
    sys.version_info.major < 3
    or (sys.version_info.major == 3 and sys.version_info.minor < 4)
):
    # inet_pton is only supported on Windows since Python 3.4
    import win_inet_pton
import socket
import socks


def verify_by_http(s):
    # Raw HTTP request
    host = "www.baidu.com"
    req = "GET / HTTP/1.0\r\nHost: %s\r\n\r\n" % host
    s.connect((host, 80))
    s.send(req.encode("utf-8"))
    rsp = s.recv(4096)
    decoded = rsp.decode("utf-8", errors="ignore")
    return decoded.startswith("HTTP/1.0 200 OK") or decoded.startswith(
        "HTTP/1.1 200 OK"
    )


def verify_by_dns(s):
    req = b"\x00\x1b\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x05\x62\x61\x69\x64\x75\x03\x63\x6f\x6d\x00\x00\x01\x00\x01"
    s.connect(("8.8.8.8", 53))
    s.send(req)
    rsp = s.recv(4096)
    return rsp[2] == req[2] and rsp[3] == req[3]


_methods = {
    "http": verify_by_http,
    "dns": verify_by_dns,
}


def test_tcp(typ, addr, port, user=None, pwd=None, method="http"):
    s = socks.socksocket(
        socket.AF_INET, socket.SOCK_STREAM
    )  # Same API as socket.socket in the standard lib
    try:
        s.set_proxy(
            socks.SOCKS5, addr, port, False, user, pwd
        )  # SOCKS4 and SOCKS5 use port 1080 by default
        # Can be treated identical to a regular socket object
        func = _methods.get(method)
        if not func:
            print("Bad method: ", method)
            return
        if func(s):
            print("TCP check passed")
        else:
            print("Invalid response")
        s.close()
    except socks.ProxyError as e:
        print(e.msg)
    except socket.error as e:
        print(repr(e))


def main():
    import os
    import argparse

    def ip_port(string):
        value = int(string)
        if value <= 0 or value > 65535:
            msg = "%r is not valid port number" % string
            raise argparse.ArgumentTypeError(msg)
        return value

    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description='Test SOCKS5 TCP support by sending HTTP request to www.baidu.com and receive response.',
    )
    parser.add_argument(
        '--proxy',
        "-p",
        metavar="PROXY",
        dest='proxy',
        required=True,
        help='IP or domain name of proxy to be tested.',
    )
    parser.add_argument(
        '--port',
        "-P",
        metavar="PORT",
        dest='port',
        type=ip_port,
        default=1080,
        help='Port of proxy to be tested.',
    )
    parser.add_argument(
        '--user',
        "-u",
        metavar="username",
        dest="user",
        default=None,
        help='Specify username to be used for proxy authentication.',
    )
    parser.add_argument(
        '--pwd',
        "-k",
        metavar="password",
        dest="pwd",
        default=None,
        help='Specify password to be used for proxy authentication.',
    )
    parser.add_argument(
        '--method',
        "-m",
        metavar="method",
        dest="method",
        default="http",
        choices=["http", "dns"],
        help='Test method.',
    )
    args = parser.parse_args()
    test_tcp(None, args.proxy, args.port, args.user, args.pwd, args.method)


if __name__ == "__main__":
    main()
