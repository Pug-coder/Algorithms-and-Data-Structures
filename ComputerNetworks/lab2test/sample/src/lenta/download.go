package main

import (
	"fmt"
	"github.com/mgutz/logxi/v1"
	"golang.org/x/net/html"
	"net/http"
)

func getAttr(node *html.Node, key string) string {
	for _, attr := range node.Attr {
		if attr.Key == key {
			return attr.Val
		}
	}
	return ""
}

func getChildren(node *html.Node) []*html.Node {
	var children []*html.Node
	for c := node.FirstChild; c != nil; c = c.NextSibling {
		children = append(children, c)
	}
	return children
}

func isElem(node *html.Node, tag string) bool {
	return node != nil && node.Type == html.ElementNode && node.Data == tag
}

func isText(node *html.Node) bool {
	return node != nil && node.Type == html.TextNode
}

func isDiv(node *html.Node, class string) bool {
	return isElem(node, "div") && getAttr(node, "class") == class
}

type Item struct {
	Ref, Price, Title string
}

func readItem(item *html.Node) *Item {
	if a := item.FirstChild; isElem(a, "a") {
		if cs := getChildren(a); len(cs) == 1 &&  isText(cs[0]) {
			return &Item{
				Ref:   getAttr(a, "href"),
				Title: cs[0].Data,
			}
		}
	}
	return nil
}

func getElementsByClassName(node *html.Node, className string) []*html.Node {
	var nodes []*html.Node
	if getAttr(node, "class") == className {
			nodes = append(nodes, node)
	}
	for c := node.FirstChild; c != nil; c = c.NextSibling {
		if found := getElementsByClassName(c, className); found != nil {
			nodes = append(nodes, found...)
		}
	}
	return nodes
}
func search(doc *html.Node) []*Item{
	founds := getElementsByClassName(doc, "product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing js--ProductCardInWishlist")
	var items []*Item
	for _, elem := range founds {
		links := getElementsByClassName(elem, "ProductCardHorizontal__title  Link js--Link Link_type_default")

		if len(links) != 1 {
			continue
		}
		prices := getElementsByClassName(elem, "ProductCardHorizontal__price_current-price js--ProductCardHorizontal__price_current-price ")

		if len(prices) != 1 {
			continue
		}
		ref := getAttr(links[0], "href")
		fmt.Println(links[0].Data)
		if ref == "" {
			continue
		}
		fmt.Println(!isText(links[0].FirstChild))
		if !isText(links[0].FirstChild){
			continue
		}
		title := links[0].FirstChild.Data
		fmt.Println(!isText(prices[0].FirstChild))
		if !isText(prices[0].FirstChild) {
			continue
		}
		price := prices[0].FirstChild.Data
		items = append(items, &Item{
			Ref: ref,
			Title: title,
			Price: price,
		})

	}
	fmt.Println(items)
	return items
}
func downloadNews() []*Item {
	log.Info("sending request to citilink.ru")
	if response, err := http.Get("https://www.citilink.ru/catalog/processory/"); err != nil {
		log.Error("request to citilink.ru failed", "error", err)
	} else {
		defer response.Body.Close()
		status := response.StatusCode
		log.Info("got response from citilink.ru", "status", status)
		if status == http.StatusOK {
			if doc, err := html.Parse(response.Body); err != nil {
				log.Error("invalid HTML from citilink.ru", "error", err)
			} else {
				log.Info("HTML from citilink.ru parsed successfully")

				return search(doc)
			}
		}
	}
	return nil
}
