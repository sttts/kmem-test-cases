# System V Message Queue example of missing kmem accounting

With Docker 1.11+ do this:

```shell
$ docker build -t msg .
$ docker run -it --kernel-memory=100M --memory=100M --rm --name msg msg \
    /bin/bash -c "python /msg.py; cat /sys/fs/cgroup/memory/memory.kmem.usage_in_bytes; tail -f /dev/null"
```

Because the created message queues need 512 MB of kernel memory, this command should never finish. But as there is no kmem accounting for ipc message queues in kernel <=4.7 this just works.
