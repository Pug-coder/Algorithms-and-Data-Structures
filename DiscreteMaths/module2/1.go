package main 
import "fmt"
//import "math"
import "sort"
type IntArray []int
func del(x int) IntArray {
	var arr IntArray

	for i := 1; i * i <= x; i++ {
		if x % i == 0 {
			arr = append(arr, i)
			if i * i != x {
				arr = append(arr, x/i)
			}
		}
	}
	return arr
}
func prime(ch int, div int) bool {
	k := ch / div
	if ch % div != 0 { return false }
	for i := 2; i <= k / 2; i++ {
		if k % i == 0{
			return false
		}
	}
	return true
}
func (arr IntArray) Len() int {return len(arr)}
func (arr IntArray) Less(i,j int) bool {
	a, b := arr[i], arr[j]
	return a > b
}
func (arr IntArray) Swap(i, j int) {
	arr[i], arr[j] = arr[j], arr[i]
}
func main() {
	var x int
	fmt.Scanf("%d", &x)
	arr := del(x);
	sort.Sort(arr)
	fmt.Println("graph {")
	for i := 0; i < len(arr); i++ {fmt.Println("\t", arr[i])}
	for j := 0; j < len(arr); j++ {
		for i := j + 1; i < len(arr); i++ {
			if prime(arr[j] , arr[i]) {
				fmt.Println("\t", arr[j], "--", arr[i])
			}
		}
	}
	fmt.Println("}")
	
}	
