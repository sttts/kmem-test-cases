#!/usr/bin/env python

import sysv_ipc
import sys

# store queues here to avoid garbage collection
qs = []

# 8kb messages
msg = ("A" * 8192).encode('utf-8')
print("message length " + str(len(msg)))

# create 32000 queues with 16kb messages each => 512MB of data
for i in range(32000):
	print("Message queue " + str(i))
	q = sysv_ipc.MessageQueue(None, flags=sysv_ipc.IPC_CREX, max_message_size=8192)
	qs.append(q)
	q.send(msg, block=False)
	q.send(msg, block=False)
