package main

import (
	"fmt"
	"github.com/skorobogatov/input"
)

var (
	used []bool
	timer int
	tin []int
	fup []int
)
func min(a, b int) int  {
	if a>b {
		return b
	}
	return a
}
/*func isBridge() int{
	var c int
	c++
	fmt.Println("c:", c)
	return c
}*/
func dfs(v int, p int,graph[][]int, timer int,used []bool, k *int) /*int*/ {
	used[v] = true
	timer += 1
	tin[v] = timer
	fup[v] = timer
	for i := 0; i < len(graph[v]); i++ {
		to := graph[v][i]
		if to == p {
			continue
		}
		if used[to] {
			fup[v] = min (fup[v], tin[to])
		} else {
			dfs(to, v, graph,timer,used,k)
			fup[v] = min (fup[v], fup[to])
			if fup[to] > tin[v] {
				(*k)++

			}
		}
	}
	//return k
}



func main() {
	var n, m int
	var graph [][]int
	input.Scanf("%d \n %d", &n, &m)
	graph = make([][]int, n)
	used = make([]bool, n)
	tin = make([]int, n)
	fup = make([]int , n)
	for i := 0; i < n; i++ {
		graph[i] = make([]int, 0)
	}
	for i := 0; i < m; i++ {
		var indexA, indexB int
		input.Scanf("%d %d", &indexA, &indexB)
		graph[indexA] = append(graph[indexA], indexB)
		graph[indexB] = append(graph[indexB], indexA)
	}
	/*for i := 0; i < n; i++ {
		fmt.Println(graph[i])
	}*/
	timer = 0
	var k int = 0
	//var count int
	for i := 0; i < n; i++ {
		used[i] = false
	}
	for i := 0; i < n; i++ {
		if !used[i] {
			dfs(i, -1 ,graph,timer,used,&k)
			//fmt.Println(count)
		}
	}
	fmt.Println(k)
}