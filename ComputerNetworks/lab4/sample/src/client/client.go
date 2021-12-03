package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"github.com/mgutz/logxi/v1"
	"net"
	"os"
	"time"
)

type File struct {
	Id int `json:"id"`
	Path    	string		`json:"path"`
	Value		[]string	`json:"value"`
}

var gen = (func() func() int {
	current := 0

	return func() int {
		current++
		return current
	}
})()

func main() {
	var (
		serverAddrStr string
		n             uint
		helpFlag      bool
	)

	flag.StringVar(&serverAddrStr, "server", "127.0.0.1:6000", "set server IP address and port")
	flag.UintVar(&n, "n", 10, "set the number of requests")
	flag.BoolVar(&helpFlag, "help", false, "print options list")

	if flag.Parse(); helpFlag {
		fmt.Fprint(os.Stderr, "client [options]\n\nAvailable options:\n")
		flag.PrintDefaults()
	} else if serverAddr, err := net.ResolveUDPAddr("udp", serverAddrStr); err != nil {
		log.Error("resolving server address", "error", err)
	} else if conn, err := net.DialUDP("udp", nil, serverAddr); err != nil {
		log.Error("creating connection to server", "error", err)
	} else {
		defer conn.Close()
		sent := make(map[int]bool)
		var f File
		buf := make([]byte, 1024*1014)
		for i := uint(0); i < n; i++ {
			var path string
			fmt.Println("Enter Path:")
			fmt.Scan(&path)
			f.Id = gen()
			f.Path = path
			sent[f.Id] = true
			if json_s, err := json.Marshal(f); err != nil {
				log.Error("convert to JSON", "error", err)
			} else if _, err := conn.Write(json_s); err != nil {
				log.Error("sending request to server", "error", err, "path", f)
				continue
			}
			for {
				conn.SetReadDeadline(time.Now().Add(time.Second * 2))
				if bytesRead, err := conn.Read(buf); err != nil {
					log.Error("receiving answer from server", "error", err)
					break
				} else {
					fmt.Println(string(buf[:bytesRead]))
					if err := json.Unmarshal(buf[:bytesRead], &f); err != nil {
						log.Error("convert to", "error", err)
						break
					} else {
						if _, ok := sent[f.Id]; !ok {
							log.Info("Duplicate")
						} else {
							delete(sent, f.Id)
							log.Info("successful interaction with server", "path", f.Path, "result", f.Value)
							break
						}
					}
				}
			}
		}
	}
}
