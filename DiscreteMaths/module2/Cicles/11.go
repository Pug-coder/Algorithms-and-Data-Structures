package main

import (
	"fmt"
)

func main() {
	cancelCh := make(chan struct{})
	dataCh := make(chan int, 1)

	go func(cancelCh chan struct{}, dataCh chan int) {
		value := 0
		for {
			select {
			case dataCh <- value:
				value++
			case <-cancelCh:
				return
			}
		}
	}(cancelCh, dataCh)

	for currentValue := range dataCh {
		fmt.Println("read", currentValue)
		if currentValue > 3 {
			fmt.Println("send cancel")
			cancelCh <- struct{}{}
		}
	}
}