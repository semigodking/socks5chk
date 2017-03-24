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
if sys.platform == 'win32' and (sys.version_info.major < 3
                                or (sys.version_info.major == 3 and sys.version_info.minor < 4)):
    # inet_pton is only supported on Windows since Python 3.4
    import win_inet_pton
import socket
import socks

def test_tcp(typ, addr, port, user=None, pwd=None):
    s = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM) # Same API as socket.socket in the standard lib
    try:
        s.set_proxy(socks.SOCKS5, addr, port, False, user, pwd) # SOCKS4 and SOCKS5 use port 1080 by default
        # Can be treated identical to a regular socket object
        # Raw HTTP request
        host = "www.baidu.com"
        req = b"GET / HTTP/1.0\r\nHost: %s\r\n\r\n" % host
        s.connect((host, 80))
        s.send(req)
        rsp = s.recv(4096)
        if rsp.startswith("HTTP/1.1 200 OK"):
            print("UDP check passed")
        else:
            print("Invalid response")
        s.close()
    except socket.error as e:
        print(repr(e))
    except socks.ProxyError as e:
        print(e.msg)


def main():
    import os
    import argparse
    def ip_port(string):
        value = int(string)
        if value <= 0 or value > 65535:
            msg = "%r is not valid port number" % string
            raise argparse.ArgumentTypeError(msg)
        return value

    parser = argparse.ArgumentParser(prog=os.path.basename(__file__), 
        description='Test SOCKS5 TCP support by sending HTTP request to www.baidu.com and receive response.')
    parser.add_argument('--proxy', "-p",  metavar="PROXY", dest='proxy', required=True,
                       help='IP or domain name of proxy to be tested.')
    parser.add_argument('--port', "-P",  metavar="PORT", dest='port', type=ip_port, default=1080,
                       help='Port of proxy to be tested.')
    parser.add_argument('--user', "-u", metavar="username", dest="user", default=None,
                       help='Specify username to be used for proxy authentication.')
    parser.add_argument('--pwd', "-k", metavar="password", dest="pwd", default=None,
                       help='Specify password to be used for proxy authentication.')
    args = parser.parse_args()
    test_tcp(None, args.proxy, args.port, args.user, args.pwd)


if __name__ == "__main__":
    main()
