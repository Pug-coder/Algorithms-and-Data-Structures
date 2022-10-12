package main

import (
	"fmt"
	"github.com/skorobogatov/input"
	"math"
)
 
func main() {
	s := input.Gets()
	input.Scanf("\n")
	var (
		first, second rune
		indf, inds, temp int
)
	indf, inds = -1, -1
	minDistance := 1000001
	input.Scanf("%c %c", &first, &second)
	arr := ([]rune)(s)
	for i, elem := range arr {
		if elem == first {indf = i}
		if elem == second {inds = i}	
		if indf != -1 && inds != -1 {
			temp = int(math.Abs(float64(inds - indf))) - 1
			//fmt.Println(temp)
			//fmt.Println("indf = ", indf)
			//fmt.Println("inds = ",inds)
			if temp < minDistance {minDistance = temp}
		}
	}
	fmt.Println(minDistance)
}