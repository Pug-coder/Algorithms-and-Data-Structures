package main

import (
	"fmt"
	"strconv"
	"sort"
)
func pow10(a, b int64) int64 {
	ch := a
	var p int64
	p = 1
	for ; b > 0 ; {
		if b & 1 != 0 {
			p *= ch
		}
		ch *= ch
		b >>= 1
	}
	return p
}
type arrInt []int
func(arr arrInt) Less(i,j int) bool {
		a := strconv.Itoa(arr[i])
		b := strconv.Itoa(arr[j])
		ch1, _ := strconv.Atoi(a + b)
		ch2, _ := strconv.Atoi(b + a)
		return ch1 > ch2
	}	


func(arr arrInt) Swap(i,j int) {
 arr[i], arr[j] = arr[j], arr[i]
}
func (arr arrInt) Len() int { return len(arr) }
func main(){
	var n int
	var a, b int64
	fmt.Scan(&n)
	arr := make([]int, n)
	for i := 0; i < n; i++ {
		fmt.Scan(&arr[i])
	}
	sort.Sort(arrInt(arr)) 
	/*for i := 0; i < n; i++ {
		fmt.Print(arr[i])
	}*/
	fmt.Scan(&a)
	fmt.Scan(&b)
	fmt.Print(pow10(a,b))
}