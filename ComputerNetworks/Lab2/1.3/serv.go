package main

import (
	"fmt"
	"github.com/jlaffaye/ftp"
	"io/ioutil"
	"path/filepath"
	"strings"
	"time"
)

func getTransferParticipants(connections []*ftp.ServerConn) (*ftp.ServerConn, *ftp.ServerConn, bool) {
	var indexA, indexB int
	fmt.Print("Введите индекс сервера-отправителя: ")
	fmt.Scan(&indexA)
	fmt.Print("Введите индекс сервера-получателя: ")
	fmt.Scan(&indexB)

	if indexA < 0 || indexA >= len(connections) || indexB < 0 || indexB > len(connections) {
		fmt.Println("Вы указали некорректный индекс")
		return nil, nil, false
	}

	return connections[indexA], connections[indexB], true
}

func download(connection *ftp.ServerConn) *ftp.Response {
	var filePath string
	fmt.Print("Введите путь до файла на сервере: ")
	fmt.Scan(&filePath)

	response, err := connection.Retr(filePath)

	if err != nil {
		fmt.Println("Произошла ошибка во время открытия файла на сервере:", err)
		return nil
	}

	return response
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
func upload(response *ftp.Response, connection *ftp.ServerConn) bool {
	var fileName string
	fmt.Print("Введите путь до файла для сохранения на сервере-получателе: ")
	fmt.Scan(&fileName)

	err := connection.MakeDir(filepath.Dir(fileName))
	if err != nil {
		fmt.Println("Не удалось создать нужную директорию для созранения")
		return false
	}

	if err = connection.Stor(fileName, response); err != nil {
		fmt.Println("Произошла ошибка во время загрузки:", err)
		return false
	}

	return true
}

func loop(connection1 *ftp.ServerConn, connection2 *ftp.ServerConn) {
	defer func() {
		connection1.Quit()
		connection2.Quit()
	}()

	for {
		var command string
		fmt.Print("Введите комманду: ")
		fmt.Scan(&command)

		switch strings.ToLower(command) {
		case "send":

			response := download(connection1)

			if response == nil {
				continue
			}

			if !upload(response, connection2) {
				response.Close()
				continue
			}

			fmt.Println("Успешно")
		case "exit":
			connection1.Quit()
			connection2.Quit()
			return
		default:
			fmt.Println("Неизвестная комманда")
		}
	}
}

func getConnection() *ftp.ServerConn {
	var url, login, password string

	fmt.Print("Введите адрес: ")
	fmt.Scan(&url)
	fmt.Print("Введите имя пользователя: ")
	fmt.Scan(&login)
	fmt.Print("Введите пароль: ")
	fmt.Scan(&password)

	connection, err := ftp.Dial(url, ftp.DialWithTimeout(5 * time.Second))

	if err != nil {
		fmt.Println("Ошибка подключения:", err)
		return nil
	}

	if err = connection.Login(login, password); err != nil {
		fmt.Println("Ошибка авторизации:", err)
		return nil
	}

	return connection
}

func main() {
	fmt.Println("Введите данные сервера-отправителя")
	connection1 := getConnection()
	fmt.Println("Введите данные сервера-получателя")
	connection2 := getConnection()

	loop(connection1, connection2)
}
