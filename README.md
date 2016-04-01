udpchk - UDP Checker
--------------------
A simple script used for checking if SOCKS5 proxy support UDP transport.

Prerequisites
-------------
* Python 2.6+ or Python 3.x
* [PySocks](https://github.com/Anorov/PySocks)
* [argparse](https://pypi.python.org/pypi/argparse) (required for Python 2.6)

Usage
-----
Run command like this and check output.
```shell
python udpchk.py -p 192.168.1.1 -P 1080 -u user1 -k password1
```
