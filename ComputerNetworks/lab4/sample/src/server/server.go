package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"github.com/mgutz/logxi/v1"
	"io/ioutil"
	"net"
	"os"
)

func listDirByReadDir(path string) []string {
	var files []string
	lst, err := ioutil.ReadDir(path)
	if err != nil {
		panic(err)
	}
	for _, val := range lst {
		if val.IsDir() {
			//files = append(files, val.Name())
			//	fmt.Printf("[%s]\n", val.Name())
		} else {
			files = append(files, val.Name())
			//fmt.Println(val.Name())
		}
	}
	return files
}

type File struct {
	Id    int      `json:"id"`
	Path  string   `json:"path"`
	Value []string `json:"value"`
}

func main() {
	var (
		serverAddrStr string
		helpFlag      bool
	)
	flag.StringVar(&serverAddrStr, "addr", "127.0.0.1:6000", "set server IP address and port")
	flag.BoolVar(&helpFlag, "help", false, "print options list")

	if flag.Parse(); helpFlag {
		fmt.Fprint(os.Stderr, "server [options]\n\nAvailable options:\n")
		flag.PrintDefaults()
	} else if serverAddr, err := net.ResolveUDPAddr("udp", serverAddrStr); err != nil {
		log.Error("resolving server address", "error", err)
	} else if conn, err := net.ListenUDP("udp", serverAddr); err != nil {
		log.Error("creating listening connection", "error", err)
	} else {
		log.Info("server listens incoming messages from clients")
		buf := make([]byte, 1024*1024)
		var f File
		for {
			if bytesRead, addr, err := conn.ReadFromUDP(buf); err != nil {
				log.Error("receiving message from client", "error", err)
			} else {
				if err := json.Unmarshal(buf[:bytesRead], &f); err != nil {
					log.Error("convert to struct", "error", err)
				} else {
					f.Value = listDirByReadDir(f.Path)

					if responseBytes, err := json.Marshal(f); err != nil {
						log.Error("convert to JSON", "error", err)
					} else if _, err = conn.WriteToUDP(responseBytes, addr); err != nil {
						log.Error("sending message to client", "error", err, "client", addr.String())
					} else {
						log.Info("successful interaction with client", "path", f.Path, "result", f.Value, "client", addr.String())
					}
				}
			}
		}
	}
}
