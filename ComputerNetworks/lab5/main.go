package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"golang.org/x/net/html"
	"net"
	"net/http"
	url2 "net/url"
	"os"
	"strings"
	"sync"
	"time"
)

var (
	nextPeerNotConnErr = errors.New("next peer not connected")
	peerClosedErr      = errors.New("peer already closed")
)

const (
	ResultRequest       = "result"
	SearchInDocsRequest = "searchInDocs"
)

type Request struct {
	InitiatorAddr string          `json:"initiatorAddr"`
	Type          string          `json:"type"` // "result", "searchInDocs"
	Payload       json.RawMessage `json:"payload"`
}

type DocsToSearchIn struct {
	Substring string   `json:"substring"`
	Hrefs     []string `json:"hrefs"`
	Depth     int      `json:"depth"`
}

type SearchResults struct {
	Url       string `json:"url"`
	Substring string `json:"substring"`
	OccurrencesCount int    `json:"occurrencesCount"`
}

type downloadedDoc struct {
	Url, Doc string
}

func ProcessDocs(urls []string, substr string, results chan<- SearchResults, nextHrefs chan<- string) {
	fmt.Println("Processing urls:", urls)
	docs := make(chan downloadedDoc, len(urls))
	var wg sync.WaitGroup
	for _, url := range urls {
		wg.Add(1)
		go func(url string) {
			err := DownloadAndFindHTMLHrefs(url, docs, nextHrefs)
			if err != nil {
				fmt.Println("Error occurred during downloading html file", err)
			}
			wg.Done()
		}(url)
	}

	go func() {
		wg.Wait()
		close(docs)
	}()

	for doc := range docs {
		results <- SearchResults{
			Url:              doc.Url,
			OccurrencesCount: strings.Count(doc.Doc, substr),
			Substring:        substr,
		}
	}
}

func DownloadAndFindHTMLHrefs(url string, doc chan<- downloadedDoc, nextHrefs chan<- string) error {
	req, err := http.NewRequest("GET", url, nil)
	req.Header.Set("Accept", "text/html")
	client := http.DefaultClient
	resp, err := client.Do(req)
	if err != nil {

		return err
	}
	defer resp.Body.Close()

	bytesDoc := make([]byte, 1024*1024)
	n, _ := resp.Body.Read(bytesDoc)
	stringDoc := string(bytesDoc[:n])
	parsedDoc, err := html.Parse(bytes.NewReader(bytesDoc[:n]))
	if err != nil {
		return err
	}
	doc <- downloadedDoc{
		Url: url,
		Doc: stringDoc,
	}

	links := make(chan *html.Node, 32)
	go func() {
		FindByTag(parsedDoc, "a", links)
		close(links)
	}()

	for link := range links {
		href := GetAttribute(link, "href")
		if href != "" {
			nextHrefs <- href
		}
	}

	return nil
}

func GetAttribute(node *html.Node, attrName string) string {
	attrValue := ""
	for _, attr := range node.Attr {
		if attr.Key == attrName {
			attrValue = attr.Val
		}
	}
	return attrValue
}

func FindByTag(doc *html.Node, tag string, foundTags chan<- *html.Node) {
	var rec func(*html.Node)
	rec = func(node *html.Node) {
		if node.Type == html.ElementNode && node.Data == tag {
			foundTags <- node
		}

		for child := node.FirstChild; child != nil; child = child.NextSibling {
			rec(child)
		}
	}

	rec(doc)
}

type Peer struct {
	SelfAddr, NextAddr string
	nextPeerConn       *net.TCPConn
	closed             bool
	searchResults      chan<- SearchResults
}

func NewPeer(addr, nextAddr string, results chan<- SearchResults) *Peer {
	return &Peer{
		SelfAddr:      addr,
		NextAddr:      nextAddr,
		searchResults: results,
	}
}

func (p *Peer) ConnectToTheNext() error {
	if p.closed {
		return peerClosedErr
	}

	if p.nextPeerConn != nil {
		return nil
	}

	addr, err := net.ResolveTCPAddr("tcp", p.NextAddr)
	if err != nil {
		return err
	}
	conn, err := net.DialTCP("tcp", nil, addr)
	if err != nil {
		return err
	}
	p.nextPeerConn = conn
	return nil
}

func (p *Peer) ServeConnections() error {
	if p.closed {
		return peerClosedErr
	}

	tcpAddr, err := net.ResolveTCPAddr("tcp", p.SelfAddr)
	if err != nil {
		return err
	}

	listener, err := net.ListenTCP("tcp", tcpAddr)
	if err != nil {
		return err
	}

	for !p.closed {
		err = listener.SetDeadline(time.Now().Add(time.Millisecond * 100))
		if err != nil {
			_ = listener.Close()
			return err
		}

		if conn, err := listener.Accept(); err != nil {
			if isTimeoutErr(err) {
				continue
			}
			_ = listener.Close()
			return err
		} else {
			err = p.receive(conn)
			if err != nil {
				fmt.Printf("Error occurred during receiving messages from %s: %v\n", conn.RemoteAddr(), err)
			}
		}
	}
	return nil
}

func (p *Peer) Close() error {
	if p.closed {
		return peerClosedErr
	}

	p.closed = true

	if p.nextPeerConn != nil {
		err := p.nextPeerConn.Close()
		p.nextPeerConn = nil
		return err
	}
	return nil
}

func (p *Peer) FindSubstringInDoc(url, substring string, depth int) error {
	if _, err := url2.Parse(url); err != nil {
		return err
	}

	results := make(chan SearchResults, 1)
	nextHrefs := make(chan string, 128)
	go func() {
		ProcessDocs([]string{url}, substring, results, nextHrefs)
		close(results)
		close(nextHrefs)
	}()
	go func() {
		for result := range results {
			p.searchResults <- result
		}
	}()
	go p.collectAndFrowardHrefs(p.SelfAddr, substring, nextHrefs, depth)

	return nil
}

func (p *Peer) forwardToTheNext(request Request) error {
	if p.nextPeerConn == nil {
		return nextPeerNotConnErr
	}

	err := p.nextPeerConn.SetWriteDeadline(time.Now().Add(time.Second))
	if err != nil {
		return err
	}
	enc := json.NewEncoder(p.nextPeerConn)
	err = enc.Encode(&request)
	if err != nil {
		return err
	}
	return nil
}

func (p *Peer) receive(conn net.Conn) error {
	defer func() { _ = conn.Close() }()
	for !p.closed {
		err := conn.SetReadDeadline(time.Now().Add(time.Second))
		if err != nil {
			return err
		}
		dec := json.NewDecoder(conn)
		req := Request{}
		if err = dec.Decode(&req); err != nil {
			if isTimeoutErr(err) {
				continue
			}
		}
		go p.processIncomingRequest(req)

	}

	return nil
}

func (p *Peer) processIncomingRequest(req Request) error {
	if req.Type == ResultRequest {
		if req.InitiatorAddr == p.SelfAddr {
			res := SearchResults{}
			err := json.Unmarshal(req.Payload, &res)
			if err != nil {
				return err
			}
			p.searchResults <- res
		} else {
			if err := p.forwardToTheNext(req); err != nil {
				fmt.Printf("Unable to forward result to the next peer: %v\n", err)
			}
		}
	} else if req.Type == SearchInDocsRequest {
		searchRequest := DocsToSearchIn{}
		err := json.Unmarshal(req.Payload, &searchRequest)
		if err != nil {
			return err
		}
		fmt.Printf("SearchInDocs request received with depth: %d\n", searchRequest.Depth)
		results := make(chan SearchResults, len(searchRequest.Hrefs))
		nextHrefs := make(chan string, 128)
		go func() {
			ProcessDocs(searchRequest.Hrefs, searchRequest.Substring, results, nextHrefs)
			close(results)
			close(nextHrefs)
		}()
		go p.collectAndForwardResults(req.InitiatorAddr, results)
		go p.collectAndFrowardHrefs(req.InitiatorAddr, searchRequest.Substring, nextHrefs, searchRequest.Depth)
	}

	return nil
}

func (p *Peer) collectAndForwardResults(initiatorAddr string, results <-chan SearchResults) {
	for result := range results {
		bytes, err := json.Marshal(result)
		if err != nil {
			fmt.Printf("Unable to marshal search result: %v\n", err)
			continue
		}
		if err = p.forwardToTheNext(Request{
			InitiatorAddr: initiatorAddr,
			Type:          ResultRequest,
			Payload:       bytes,
		}); err != nil {
			fmt.Printf("Unable to forward results to the next peer: %v\n", err)
		}
	}
}

func (p *Peer) collectAndFrowardHrefs(initiatorAddr, substring string, nextHrefs <-chan string, depth int) {
	if depth <= 0 {
		return
	}

	var hrefs []string
	for href := range nextHrefs {
		hrefs = append(hrefs, href)
	}

	if len(hrefs) == 0 {
		return
	}

	fmt.Printf("Collected %d hrefs on depth %d\n", len(hrefs), depth)

	searchRequestToTheNext := DocsToSearchIn{
		Substring: substring,
		Hrefs:     hrefs,
		Depth:     depth - 1,
	}

	bytes, err := json.Marshal(searchRequestToTheNext)
	if err != nil {
		fmt.Printf("Unable to marshal search request: %v\n", err)
		return
	}
	if err = p.forwardToTheNext(Request{
		InitiatorAddr: initiatorAddr,
		Type:          SearchInDocsRequest,
		Payload:       bytes,
	}); err != nil {
		fmt.Printf("Unable to forward hrefs to the next peer: %v\n", err)
	}
}

func (p *Peer) closeTheNextPeer() error {
	err := p.nextPeerConn.Close()
	p.nextPeerConn = nil
	return err
}

func displayResults(results <-chan SearchResults) {
	for result := range results {
		if result.OccurrencesCount != 0 {
			fmt.Printf("[Result][URL: %s] Count of occourencies of the substring \"%s\": %d\n", result.Url, result.Substring, result.OccurrencesCount)
		}
	}
}

func isTimeoutErr(err error) bool {
	netErr, ok := err.(net.Error)
	return ok && netErr.Timeout()
}

func loop(p *Peer) {
	var command string

	for {
		fmt.Print("Enter command: ")
		fmt.Scan(&command)
		switch command {
		case "connect":
			{
				err := p.ConnectToTheNext()
				if err != nil {
					fmt.Printf("Error occoured during connecting to the next peer: %s\n", err.Error())
				} else {
					fmt.Printf("Successfully connected to the next peer with address %s\n", p.NextAddr)
				}
			}
		case "quit":
			{
				_ = p.Close()
				fmt.Println("Successfully closed!")
				return
			}
		case "find":
			{
				var url, substr string
				var depth int
				fmt.Print("Enter full url: ")
				fmt.Scan(&url)
				fmt.Print("Enter substring: ")
				fmt.Scan(&substr)
				fmt.Print("Enter depth: ")
				fmt.Scan(&depth)
				if err := p.FindSubstringInDoc(url, substr, depth); err != nil {
					fmt.Printf("Error occoured during searching substring: %s\n", err.Error())
				}
			}
		}
	}
}

func main() {
	selfAddr := flag.String("self", ":8000", "self address")
	nextAddr := flag.String("next", ":8001", "address of the next peer")
	flag.Parse()
	results := make(chan SearchResults, 16)
	p := NewPeer(*selfAddr, *nextAddr, results)

	go displayResults(results)
	go func() {
		err := p.ServeConnections()
		if err != nil {
			fmt.Printf("Error occoured during serving connections: %s\n", err)
		}
		os.Exit(1)
	}()
	loop(p)
}
//https://www.bmstu.ru
