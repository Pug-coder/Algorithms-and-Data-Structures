package main

import (
	"fmt"
)

var qs []int
var ys []string
type AutoMealy struct{
	n, m, m1 int
	inputAlphabet, outputAlphabet []string
	crossover [][]int
	exit [][]string
	ex []string
}

func Print(crossover [][]int, indices []int, mealy AutoMealy)  {
	fmt.Println("digraph {")
	fmt.Println("rankdir = LR")
	for i, _ := range indices {
		fmt.Printf("%d [label = \"(%d,%s)\"]\n", i, qs[indices[i]], ys[indices[i]])
	}
	for i, _ := range crossover {

		for j, x := range crossover[i] {
			fmt.Printf("%d -> %d [label = \"%s\"]\n", i, x, mealy.inputAlphabet[j])
		}
	}
	fmt.Println("}")
}

func Search(indices []int)  int {
	for i, s := range indices {
		if qs[len(qs) - 1] == qs[s] && ys[len(qs) - 1] == ys[s] {
			return i
		}
	}
	return -1
}
func partiton( low int, high int, less func(i, j int )bool, swap func(i, j int)) int{
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
		quickSortRec( q + 1, high, less, swap)
	}
}
func QuickSort(n int, less func(i, j int) bool,swap func(i, j int)) {
	quickSortRec(0, n - 1, less, swap)
}
func (newAuto *AutoMealy) NewMealy() *AutoMealy{
	var m,m1,n int
	fmt.Scan(&m)
	newAuto.m = m
	inputAlphabet := make([]string, m)
	for i := 0; i < m; i++ {
		fmt.Scan(&inputAlphabet[i])
	}
	fmt.Scan(&m1)
	newAuto.m1 = m1
	newAuto.inputAlphabet = inputAlphabet
	outputAlphabet := make([]string, m1)
	for i := 0; i < m1; i++ {
		fmt.Scan(&outputAlphabet[i])
	}
	fmt.Scan(&n)
	newAuto.n = n
	newAuto.outputAlphabet = outputAlphabet
	crossover := make([][]int, n)

	for i := 0; i < n; i++ {
		crossover[i] = make([]int, m )
		for j := 0; j < m; j++ {
			fmt.Scan(&crossover[i][j])
		}
	}
	newAuto.crossover = crossover
	exit := make([][]string, n)
	for i := 0; i < n; i++ {
		exit[i] = make([]string, m)
		for j := 0; j < m; j++ {
			fmt.Scan(&exit[i][j])
		}
	}
	newAuto.exit = exit
	return newAuto
}
func main() {
	var mealy AutoMealy
	mealy.NewMealy()
	// Составим массив состояний Мура
	states := make([]int, 0)
	for i := range mealy.crossover {
		for j, x := range mealy.crossover[i] {
			qs = append(qs, x)
			ys = append(ys, mealy.exit[i][j])
			if s := Search(states); s == -1 {
				states = append(states, j + i * mealy.m)
			}
		}
	}
	if len(states) > 1 {
		QuickSort(len(states), func(i, j int) bool {
			return states[i] < states[j]
		},
			func(i, j int) { states[i], states[j] = states[j], states[i] },
		)
	}
	newCrossover := make([][]int, len(states))
	for i := 0; i < len(states); i++ {
		newCrossover[i] = make([]int, mealy.m)
		for j := 0; j < mealy.m; j++ {
			qs = append(qs, mealy.crossover[qs[states[i]]][j])
			ys = append(ys, mealy.exit[qs[states[i]]][j])
			newCrossover[i][j] = Search(states)
		}
	}
	Print(newCrossover, states, mealy)
}