package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"sync"
	"sync/atomic"
)

func main() {
	tcpAddr, err := net.ResolveTCPAddr("tcp", os.Args[1])
	if err != nil {
		println(err.Error())
		os.Exit(1)
	}

	n, err := strconv.Atoi(os.Args[2])
	if err != nil {
		println(err)
		os.Exit(1)
	}
	c := make(chan string, 100)
	var wg sync.WaitGroup
	wg.Add(n)
	var conns int64
	for i := 0; i < n; i++ {
		go func(i int) {
			defer wg.Done()
			c <- fmt.Sprintf("dialing #%d", i)
			_, err := net.DialTCP("tcp", nil, tcpAddr)
			if err != nil {
				c <- fmt.Sprintf("dial failed #%d: %v", i, err)
				return
			}
			atomic.AddInt64(&conns, 1)
			c <- fmt.Sprintf("accepted #%d, %d connected", i, atomic.LoadInt64(&conns))

			<- make(chan struct{})
		}(i)
	}

	go func() {
		for s := range c {
			println(s)
		}
	}()

	wg.Wait()
}
