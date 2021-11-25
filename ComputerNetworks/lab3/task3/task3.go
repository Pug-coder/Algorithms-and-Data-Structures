package main

import (
	"fmt"
	"golang.org/x/net/trace"
	"net/http"
)

type Fetcher struct {
	domain string
	events trace.EventLog
}

func NewFetcher(domain string) *Fetcher {
	return &Fetcher{
		domain,
		trace.NewEventLog("mypkg.Fetcher", domain),
	}
}
func (f *Fetcher) Fetch(path string) (string, error) {
	resp, err := http.Get("http://" + f.domain + "/" + path)
	if err != nil {
		f.events.Errorf("Get(%q) = %v", path, err)
		return "", err
	}
	f.events.Printf("Get(%q) = %s", path, resp.Status)
	return resp.Status, err
}

func (f *Fetcher) Close() error {
	f.events.Finish()
	return nil
}
func main(){
	var domain string
	fmt.Scan(&domain)
	fetch := NewFetcher(domain)
	fetch.Fetch(fetch.domain)
	fetch.Close()
}