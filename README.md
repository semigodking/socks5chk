udpchk - UDP Checker
--------------------
Simple scripts used for checking SOCKS5 proxy's support of TCP or UDP.

Prerequisites
-------------
* Python 2.6+ or Python 3.x
* [PySocks](https://github.com/Anorov/PySocks)
* [argparse](https://pypi.python.org/pypi/argparse) (required for Python 2.6)
* [win_inet_pton](https://pypi.python.org/pypi/win_inet_pton) (required for running Python 2.6-3.3 on Windows)

Usage
-----
Run command like this and check output.
```shell
python tcpchk.py -p 192.168.1.1 -P 1080
python tcpchk.py -p 192.168.1.1 -P 1080 -u user1 -k password1
python udpchk.py -p 192.168.1.1 -P 1080
python udpchk.py -p 192.168.1.1 -P 1080 -u user1 -k password1
```
