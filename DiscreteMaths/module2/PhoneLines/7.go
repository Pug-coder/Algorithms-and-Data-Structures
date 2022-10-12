package main

import (
	"fmt"
	"github.com/skorobogatov/input"
)
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
type Graph struct {
	value [][]int
	used []bool
	min_e []int
	sel_e []int
}
const INF = 2147483647
func PRIM(graph Graph) int{
	graph.min_e[0] = 0
	res := 0
	for i := 0; i < len(graph.value); i++ {
		min1 := INF
		var u int
		for j := 0; j < len(graph.value); j++ {
			if !graph.used[j] && graph.min_e[j] < min1 {
				min1 = graph.min_e[j]
				u = j
			}
		}
		res += min1
		graph.used[u] = true
		for v := 0; v < len(graph.value); v++ {
			graph.min_e[v] = min(graph.min_e[v],graph.value[u][v])
		}
	}
	return res
}

func main() {
	var n, m int
	var graph Graph
	input.Scanf("%d \n %d", &n, &m)
	graph.value = make([][]int, n)
	graph.used = make([]bool, n)
	graph.min_e = make([]int, n)
	//graph.sel_e = make([]int,n)
	for i := 0; i < n; i++ {
		graph.value[i] = make([]int, n)
		for j := 0; j < n; j++ {
			graph.value[i][j] = INF
		}
	}
	for i := 0; i < n; i++ {
		graph.min_e[i] = INF
	}

	//for i := 0; i < n; i++ {
	//	graph.sel_e[i] = -1
	//}
	for i := 0; i < m; i++ {
		var indexA, indexB, dist int
		input.Scanf("%d %d %d", &indexA, &indexB, &dist)
		graph.value[indexA][indexB] = dist
		graph.value[indexB][indexA] = dist
	}
	fmt.Println(PRIM(graph))
}
