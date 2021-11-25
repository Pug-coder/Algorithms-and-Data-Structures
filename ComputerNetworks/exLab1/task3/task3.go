package main

import (
	"encoding/xml"
	"fmt"
	"log"
	"net/http"
)
type Enclosure struct {
	Url    string `xml:"url,attr"`
	Length int64  `xml:"length,attr"`
	Type   string `xml:"type,attr"`
}
type Item struct {
	Title     string    `xml:"title"`
	Link      string    `xml:"link"`
	Desc      string    `xml:"description"`
	Guid      string    `xml:"guid"`
	Enclosure Enclosure `xml:"enclosure"`
	PubDate   string    `xml:"pubDate"`
}

type Channel struct {
	Title string `xml:"title"`
	Link  string `xml:"link"`
	Desc  string `xml:"description"`
	Items []Item `xml:"item"`
}

type Rss struct {
	Channel Channel `xml:"channel"`
}

func HomeRouterHandler(w http.ResponseWriter, r *http.Request) {
	resp, err := http.Get("https://lenta.ru/rss")
	if err != nil {
		fmt.Printf("Error GET: %v\n", err)
		return
	}
	defer resp.Body.Close()

	rss := Rss{}

	decoder := xml.NewDecoder(resp.Body)
	err = decoder.Decode(&rss)
	if err != nil {
		fmt.Printf("Error Decode: %v\n", err)
		return
	}

	var html string

	html += "<h1>" + rss.Channel.Title + "</h1>"
	html += "<a href=\"" + rss.Channel.Link + "\">Ссылка </a>"

	for _, item := range rss.Channel.Items {
		html += "<div>"
		html += "<h2>" + item.Title + "</h2>"
		html += "<div>" + item.Desc + "</div>"
		html += "<a href=\"" + item.Link + "\">Подробнее </a>"
		html += "</div>"
	}
	fmt.Fprintln(w, html)
}

func main() {
	http.HandleFunc("/", HomeRouterHandler) // установим роутер
	err := http.ListenAndServe(":9000", nil) // задаем слушать порт
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}