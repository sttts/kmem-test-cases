#!/usr/bin/env python

import socket
import sys
import subprocess

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 10080))
s.listen(int(sys.argv[1]))

if len(sys.argv) > 2:
	while True:
		print(".")
		s.accept()
else:
	subprocess.call(["tail", "-f", "/dev/null"])
