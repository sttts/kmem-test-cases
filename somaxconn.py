#!/usr/bin/env python

import socket
import sys
import subprocess

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 10080))
s.listen(int(sys.argv[1]))
s.accept()
subprocess.call(["tail", "-f", "/dev/null"])
