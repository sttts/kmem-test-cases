# System V Message Queue example of missing kmem accounting

With Docker 1.11+ do this:

```shell
$ docker build -t msg .
$ docker run -it --kernel-memory=100M --memory=100M --rm --name msg msg \
    /bin/bash -c "python /msg.py; cat /sys/fs/cgroup/memory/memory.kmem.usage_in_bytes; tail -f /dev/null"
```

Because the created message queues need 512 MB of kernel memory, this command should never finish. 

## Kernels < 4.5

The command actually terminates early:

```
...
Message queue 5959
Message queue 5960
Message queue 5961
/bin/bash: line 1:     6 Killed                  python /msg.py
101056512
```

## Kernel >= 4.5

With later kernels accontings was turned into opt-in (compare https://github.com/torvalds/linux/commit/a9bb7e620efdfd29b6d1c238041173e411670996) such that there is no kmem accounting for ipc message queues anymore and the upper example just works.
