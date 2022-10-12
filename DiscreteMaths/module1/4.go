package main 

import "fmt"

func partiton(low int, high int, less func(i, j int )bool, swap func(i, j int)) int{
	i := low
	for j := low; j < high; j++ {
		if less(j,high) {
			swap(i,j)
			i++
		}
	}
	swap(i,high)
	return i
}
func quickSortRec(low int, high int, less func(i, j int) bool, swap func(i, j int)){
	if low < high{
		q := partiton(low, high, less ,swap)
		quickSortRec(low , q - 1, less, swap)
		quickSortRec(q + 1, high, less, swap)
	}
}
func qsort(n int, less func(i, j int) bool,swap func(i, j int)) { 
    quickSortRec(0, n - 1, less, swap)
}



func main(){
	var n int
	var m int
	fmt.Scan(&n)
	arr := make([]int, n)
	for i:=0; i<n; i++ {
		fmt.Scan(&m)
		arr[i] = m
	}
	qsort(n, func(i, j int) bool {return arr[i]<arr[j]}, func(i, j int) { arr[i], arr[j] = arr[j], arr[i] })
	for _, x := range arr{
		fmt.Printf("%d ", x)
	}
}
