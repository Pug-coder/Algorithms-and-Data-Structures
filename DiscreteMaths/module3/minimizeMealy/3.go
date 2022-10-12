package main

import "fmt"

type AutoMealy struct {
	n, m, q int
	state, stateNew [][]int
	exSignals, exSignalsNew [][]string
}

func (mealy *AutoMealy) input(n, m, q int) {
	mealy.n = n
	mealy.m = m
	mealy.q = q
	mealy.state = make([][]int, n)
	mealy.exSignals = make([][]string, n)
	mealy.stateNew = make([][]int, n)
	mealy.exSignalsNew = make([][]string, n)
	for i := 0; i < n; i++ {
		mealy.state[i] = make([]int, m)
		mealy.exSignals[i] = make([]string, m)
		mealy.stateNew[i] = make([]int, m)
		mealy.exSignalsNew[i] = make([]string, m)
	}
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
}


func DFS(mealy AutoMealy, used []int, index *int, begin int) {
	used[begin] = *index
	*index++
	for i := 0; i < mealy.m; i++ {
		if used[mealy.state[begin][i]] == -1 {
			DFS(mealy, used, index, mealy.state[begin][i])
		}
	}
}

func Canon(mealy AutoMealy) AutoMealy {
	used := make([]int, mealy.n)
	for i := 0; i < mealy.n; i++ {
		used[i] = -1
	}
	index := 0
	DFS(mealy, used, &index, mealy.q)
	for i := 0; i < mealy.n; i++ {
		if used[i] != -1 {
			mealy.exSignalsNew[used[i]] = mealy.exSignals[i]
			for j := 0; j < mealy.m; j++ {
				mealy.stateNew[used[i]][j] = used[mealy.state[i][j]]
			}
		}
	}
	mealy.n = index
	mealy.q = 0
	mealy.state = mealy.stateNew
	mealy.exSignals = mealy.exSignalsNew

	return mealy
}

func Find(a []int, x int) int {
	if a[x] == x {
		return x
	} else {
		a[x] = Find(a, a[x])
		return a[x]
	}
}

func Union(a []int, x int, y int) {
	newX := Find(a, x)
	newY := Find(a, y)
	if newX == newY {
		return
	}
	if newX != newY {
		newX, newY = newY, newX
	}
	a[newX] = newY
}
func Split(m *int, help []int, mealy AutoMealy) {
	*m = mealy.n
	a := make([]int, *m)
	for i := 0; i < *m; i++ {
		a[i] = i
	}
	for i := 0; i < mealy.n; i++ {
		for j := i + 1; j < mealy.n; j++ {
			if help[i] == help[j] && Find(a, i) != Find(a, j) {
				eq := true
				for k := 0; k < mealy.m; k++ {
					if help[mealy.state[i][k]] != help[mealy.state[j][k]] {
						eq = false
						break
					}
				}
				if eq {
					Union(a, i, j)
					*m--
				}
			}
		}
	}
	for i := 0; i < mealy.n; i++ {
		help[i] = Find(a, i)
	}
}
func Split1(q *int, help []int, mealy AutoMealy) {
	*q = mealy.n
	a := make([]int, *q)
	for i := 0; i < *q; i++ {
		a[i] = i
	}
	for i := 0; i < mealy.n; i++ {
		for j := i + 1; j < mealy.n; j++ {
			if Find(a, i) != Find(a, j) {
				eq := true
				for k := 0; k < mealy.m; k++ {
					if mealy.exSignals[i][k] != mealy.exSignals[j][k] {
						eq = false
						break
					}
				}
				if eq {
					Union(a, i, j)
					*q--
				}
			}
		}
	}
	for i := 0; i < mealy.n; i++ {
		help[i] = Find(a, i)
	}
}
func AufenkampHohn(mealy AutoMealy) AutoMealy{
	pi := make([]int, mealy.n)
	var m1, m int
	Split1(&m1, pi, mealy)
	Split(&m, pi, mealy)
	for m != m1 {
		m1 = m
		Split(&m, pi, mealy)
	}

	a := make([]int, mealy.n)
	b := make([]int, mealy.n)
	c := 0
	for i := 0; i < mealy.n; i++ {
		if pi[i] == i {
			a[c] = i
			b[i] = c
			c++
		}
	}
	mealy.n = m1
	mealy.q = b[pi[mealy.q]]

	p := make([][]string, mealy.n)
	for i := 0; i < mealy.n; i++ {
		p[i] = make([]string, mealy.m)
	}

	for i := 0; i < mealy.n; i++ {
		for j := 0; j < mealy.m; j++ {
			mealy.state[i][j] = b[pi[mealy.state[a[i]][j]]]
			p[i][j] = mealy.exSignals[a[i]][j]
		}
	}
	mealy.exSignals = p

	return mealy
}
func Print(mealy AutoMealy) {
	fmt.Println("digraph { \n" +
		"\trankdir = LR\n" +
		"\tdummy [label = \"\", shape = none]")
	for i := 0; i < mealy.n; i++ {
		fmt.Printf("\t%d %s\n", i, "[shape = circle]")
	}
	fmt.Println("\tdummy ->", 0)
	for i := 0; i < mealy.n; i++ {
		for j := 0; j < mealy.m; j++ {
			fmt.Print("\t", i)
			fmt.Print(" -> ", mealy.state[i][j], " [label = \"")
			fmt.Printf("%c", rune(97+j))
			fmt.Print("(", mealy.exSignals[i][j], ")", "\"", "]", "\n")
		}
	}
	fmt.Println("}")
}
func main() {
	var mealy AutoMealy
	var n, m, q int
	fmt.Scan(&n, &m, &q)
	mealy.input(n, m, q)
	mealy = AufenkampHohn(mealy)
	mealy = Canon(mealy)
	Print(mealy)
}