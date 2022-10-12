package main

import "fmt"

type AutoMealy struct {
	start int
	state [][]int
	exSignals [][]string
}

type UsedMealy struct {
	state [][]int
	exSignals [][]string
	used []int
}
func input(n int, m int, q int, mealy AutoMealy) AutoMealy {
	for i := 0; i < n; i++ {
		for j := 0; j < m; j++ {
			fmt.Scan(&mealy.state[i][j])
		}
	}
	for i := 0; i < n; i++ {
		for j := 0; j < m; j++ {
			fmt.Scan(&mealy.exSignals[i][j])
		}
	}
	mealy.start = q
	return mealy
}
func (newAuto *AutoMealy) NewMealy(n int ,m int) *AutoMealy {
	newAuto.state = make([][]int, n)
	newAuto.exSignals = make([][]string, n)
	for i := 0; i < n; i++ {
		newAuto.state[i] = make([]int, m)
		newAuto.exSignals[i] = make([]string, m)
	}
	return newAuto
}
func (newAuto *UsedMealy) UsedMealy(n int ,m int) *UsedMealy {
	newAuto.state = make([][]int, n)
	newAuto.exSignals = make([][]string, n)
	newAuto.used = make([]int,n)
	for i := 0; i < n; i++ {
		newAuto.state[i] = make([]int, m)
		newAuto.exSignals[i] = make([]string, m)

	}
	for i := 0; i < n; i++ {
		newAuto.used[i] = -1
	}
	return newAuto
}
func DFS(usedAuto UsedMealy, mealy AutoMealy, index *int, begin, m int) {
	usedAuto.used[begin] = *index
	(*index)++
	for i := 0; i < m; i++ {
		if usedAuto.used[mealy.state[begin][i]] == -1 {
			DFS(usedAuto, mealy, index, mealy.state[begin][i], m)
		}
	}
}

func main() {
	var n, m, q, index int
	var mealy AutoMealy
	var usedAuto UsedMealy
	index = 0
	fmt.Scanf("%d\n", &n)
	fmt.Scanf("%d\n", &m)
	fmt.Scanf("%d\n", &q)
	mealy.NewMealy(n, m)
	usedAuto.UsedMealy(n, m)
	input(n, m, q, mealy)

	DFS(usedAuto, mealy, &index, q, m)

	for i := 0; i < n; i++ {
		if usedAuto.used[i] != -1 {
			usedAuto.exSignals[usedAuto.used[i]] = mealy.exSignals[i]
			for j := 0; j < m; j++ {
				usedAuto.state[usedAuto.used[i]][j] = usedAuto.used[mealy.state[i][j]]
			}
		}
	}
	fmt.Print(index,"\n",m,"\n",0,"\n")
	for i := 0; i < index; i++ {
		for j := 0; j < m; j++ {
			fmt.Print(usedAuto.state[i][j], " ")
		}
		fmt.Println()
	}
	for i := 0; i < index; i++ {
		for j := 0; j < m; j++ {
			fmt.Print(usedAuto.exSignals[i][j], " ")
		}
		fmt.Println()
	}
}