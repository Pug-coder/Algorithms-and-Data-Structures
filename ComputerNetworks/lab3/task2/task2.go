package main

import (
	"fmt"
	"github.com/sparrc/go-ping"
	"os"
	"os/signal"
)

func f(addr string) {

	pinger, err := ping.NewPinger(addr)
	if err != nil {
		fmt.Printf("ERROR: %s\n", err.Error())
		return
	}
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)
	go func() {
		for _ = range c {
			pinger.Stop()
		}
	}()
	pinger.Count = 3
	pinger.OnRecv = func(pkt *ping.Packet) {
		fmt.Printf("%d bytes from %s: icmp_seq=%d time=%v\n",
			pkt.Nbytes, pkt.IPAddr, pkt.Seq, pkt.Rtt)

	}
	pinger.OnFinish = func(stats *ping.Statistics) {

		fmt.Printf("\n--- %s ping statistics ---\n", stats.Addr)

		fmt.Printf("%d packets transmitted, %d packets received, %v%% packet loss\n",

			stats.PacketsSent, stats.PacketsRecv, stats.PacketLoss)

		fmt.Printf("round-trip min/avg/max/stddev = %v/%v/%v/%v\n",

			stats.MinRtt, stats.AvgRtt, stats.MaxRtt, stats.StdDevRtt)

	}
	pinger.Run()
}
func main() {
	var addr string
	fmt.Println("Введите адрес хоста:")
	fmt.Scan(&addr)
	for i := 0; i < 10; i++  {
		go f(addr)
	}
	var input string
	fmt.Scanln(&input)
}

