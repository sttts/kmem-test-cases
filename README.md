# Kernel Memory Accounting Test Case

## System V Message Queue example of missing kmem accounting

With Docker 1.11+ do this:

```shell
$ docker build -t msg .
$ docker run -it --sysctl=kernel.msgmni=32768 --kernel-memory=100M --memory=100M --rm --name msg msg \
    /bin/bash -c "python /msg.py; cat /sys/fs/cgroup/memory/memory.kmem.usage_in_bytes; tail -f /dev/null"
```

Because the created message queues need 512 MB of kernel memory, this command should never finish. 

### Kernels < 4.5

The command actually terminates early:

```
...
Message queue 5959
Message queue 5960
Message queue 5961
/bin/bash: line 1:     6 Killed                  python /msg.py
101056512
```

### Kernel >= 4.5

With later kernels kmem acconting was turned into opt-in (compare https://github.com/torvalds/linux/commit/a9bb7e620efdfd29b6d1c238041173e411670996) such that there is no kmem accounting for ipc message queues anymore and the upper example just works.

## TCP Memory Pressure

Prepare the system:

```shell
sysctl net.ipv4.tcp_syncookies=0
sysctl net.core.rmem_max=1000000
sysctl net.core.wmem_max=1000000
sysctl net.ipv4.tcp_rmem="1000000 1000000 6000000"
sysctl net.ipv4.tcp_wmem="1000000 1000000 6000000"
```

With Docker 1.11+ do this:

```shell
$ docker run --privileged -it --memory 50M --kernel-memory 10M \
    -p 10080:10080 --sysctl=net.core.somaxconn=512 --name somaxconn --rm \
    sttts/ipc-test /bin/bash -c \
    "echo 10000000 > /sys/fs/cgroup/memory/memory.kmem.tcp.limit_in_bytes; python /somaxconn.py 500 1 & while sleep 1; do echo $(cat /sys/fs/cgroup/memory/memory.kmem.usage_in_bytes) $(cat /sys/fs/cgroup/memory/memory.kmem.tcp.usage_in_bytes); done"
```

In a second shell call the client:

```shell
$ go run ./connect.go $(docker inspect --format '{{ .NetworkSettings.IPAddress }}' somaxconn):10080 1000
```

The client will be able to create around 500 connection, the others a blocking.

In the server container, the two numbers printed each second are normal kmem memory and the tcp kmem value.

Depending on the kernel you can observe a different behavior:

- **kernel 4.6.3** (Fedora 24): `47702016 0` - tcp memory are not counted at all, kmem is pretty high.
- **kernel  4.4.0-31** (Ubuntu 16.04LTS): only values from the root-cg are copied into the counters of the container memcg initially, but do not change anymore during runtime.

Overall, tcp kmem accounting feels pretty broken.
