package main

import (
	"bytes"
	"fmt"
	"github.com/jlaffaye/ftp"
	"io/ioutil"
	"log"
	"time"
)
func makeDirectory(c *ftp.ServerConn) {
	var data string
	fmt.Println("Add new Directory")
	fmt.Scan(&data)
	err := c.MakeDir(data)
	if err != nil {
		fmt.Println(err)
	}
}

func removeDirectory(c *ftp.ServerConn) {
	var data string
	fmt.Println("Directory name to delete")
	fmt.Scan(&data)
	toDel := c.RemoveDir(data)
	if toDel != nil {
		fmt.Println(toDel)
	}
}
func addNewFile(c *ftp.ServerConn) {
	var (
		info string
		fileName string
	)
	fmt.Println("file text")
	fmt.Scan(&info)
	fmt.Println("file name")
	fmt.Scan(&fileName)
	data := bytes.NewBufferString(info)
	err := c.Stor(fileName, data)
	if err != nil {
		fmt.Println(err)
	}
}

func listDir(connection *ftp.ServerConn) {
	var directoryName string
	fmt.Print("Directory name: ")
	fmt.Scan(&directoryName)

	entries, err := connection.List(directoryName)

	if err != nil {
		fmt.Println("Reading error:", err)
	}
	fmt.Println("Directory content:", directoryName)
	for _, entry := range entries {
		fmt.Print("\t")
		switch entry.Type {
		case ftp.EntryTypeFile:
			fmt.Print("folder: ")
		case ftp.EntryTypeFolder:
			fmt.Print("Папка: ")
		default:
			fmt.Print("Object: ")
		}
		fmt.Println(entry.Name)
	}
}

func readFile(c *ftp.ServerConn) {
	var data string
	fmt.Println("fileName: ")
	fmt.Scan(&data)
	r, err := c.Retr(data)
	if err != nil {
		fmt.Println(err)
	}
	defer r.Close()

	buf, err := ioutil.ReadAll(r)
	println(string(buf))
}

func main() {
	c, err := ftp.Dial("students.yss.su:21", ftp.DialWithTimeout(5*time.Second))
	if err != nil {
		log.Fatal(err)
	}

	err = c.Login("ftpiu8", "3Ru7yOTA")
	if err != nil {
		log.Fatal(err)
	}

	//makeDirectory(c)
	//removeDirectory(c)
	//addNewFile(c)
	//readFile(c)
	//listDir(c)
	fmt.Print("Enter command: ")
	var command string
	fmt.Scanln(&command)
	switch command {
	case "makeDirectory":
		makeDirectory(c)
	case "removeDirectory":
		removeDirectory(c)
	case "addNewFile":
		addNewFile(c)
	case "readFile":
		readFile(c)
	case "listDirectory":
		listDir(c)
	default:
		fmt.Println("Unknown command:", command)
	}

	if err := c.Quit(); err != nil {
		log.Fatal(err)
	}
}