package main
import(
	"fmt"
)
func search(array []string, s string) bool{
	for i := 0; i < len(array); i++{
		if array[i] == s  {return true}
	}
	return false
}
func main() {
	var s string
	fmt.Scan(&s)
	arr := []rune(s)
	var repeat []string 	
	var index []int
	for i, elem := range arr{
		if elem == '(' {
			index = append(index,i)
		} else if elem == ')'{
			openInd := index[len(index) - 1]
			index = index[:len(index) - 1]
			slice := string(arr[openInd : i + 1])
			if !search(repeat, slice) {
				repeat = append(repeat,slice)
			}
		}
		
	}
	fmt.Print(len(repeat))
}