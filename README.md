socks5chk - Socks5 Ability Checker
----------------------------------
Simple scripts used for checking SOCKS5 proxy's support of TCP or UDP.
It could also check if SOCKS5 proxy allows sending DNS to TCP port 53.

Prerequisites
-------------
* Python 2.6+ or Python 3.x
* [PySocks](https://github.com/Anorov/PySocks)
* [argparse](https://pypi.python.org/pypi/argparse) (required for Python 2.6)
* [win\_inet\_pton](https://pypi.python.org/pypi/win_inet_pton) (required for running Python 2.6-3.3 on Windows)

Setup
-----
Run commands like below to setup environment for running script.
```shell
python3 -m venv venv
source venv/bin/activate
pip install pysocks
```

Usage
-----
Run command like this and check output.
```shell
python tcpchk.py -p 192.168.1.1 -P 1080
python tcpchk.py -p 192.168.1.1 -P 1080 -m dns
python tcpchk.py -p 192.168.1.1 -P 1080 -u user1 -k password1
python udpchk.py -p 192.168.1.1 -P 1080
python udpchk.py -p 192.168.1.1 -P 1080 -u user1 -k password1
```
