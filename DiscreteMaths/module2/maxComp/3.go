package main

import (
	"fmt"
)
type Edge struct {
	u, v int
	marked bool
}
var visited []bool
var dfs func(to int)
func dodfs(graph [][]int) {
	//var visited []bool
	visited = make([]bool, len(graph))
	//var dfs func(to int)
	for i := 0; i < len(graph); i++ {
		visited[i] = false
	}
	dfs = func(to int) {
		visited[to] = true
		for i := 0; i < len(graph); i++ {
			ch := graph[to][i]
			if !visited[ch] {
				dfs(i)
			}
		}
	}
	for i := 1; i < len(graph); i++ {
		if !visited[i]{
			dfs(i)
		}
	}
}
func main() {
	var (
		a,b int
		m int
		n int
		graph [][]int
		edges []Edge
	)

	fmt.Scanf("%d", &n)
	fmt.Scanf("%d", &m)
	graph = make([][]int, n)
	edges = make([]Edge,0)
	for i := 0; i < n; i++ {
		graph[i] = make([]int,0)
	}
	for i := 0; i < m; i++ {
		fmt.Scanf("%d %d", &a, &b)
		graph[a] = append(graph[a], b)
		edges = append(edges,Edge{a,b,false})
	}
	for i := 0; i < n; i++ {
		fmt.Println(graph[i])
	}
}