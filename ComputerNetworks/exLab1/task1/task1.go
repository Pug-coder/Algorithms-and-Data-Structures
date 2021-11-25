package main

import (
	"fmt"      // пакет для форматированного ввода вывода
	"log"      // пакет для логирования
	"net/http" // пакет для поддержки HTTP протокола
)

func ProcessHandler(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	name := r.Form["name"][0]
	lastname := r.Form["lastname"][0]
	fmt.Fprintln(w, "Ваше имя: "+name+" Ваша фамилия: "+lastname)
}
func HomeRouterHandler(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "./client.html")
}

func main() {
	http.HandleFunc("/", HomeRouterHandler) // установим роутер
	http.HandleFunc("/process", ProcessHandler)
	err := http.ListenAndServe(":9000", nil) // задаем слушать порт
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}