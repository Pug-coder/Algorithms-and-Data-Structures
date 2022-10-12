package main

import (
	"fmt"
	"github.com/skorobogatov/input"
)




type Vertex struct {
	neighbors []int
	distance []int
}
type Queue struct {
Storage []int
}
func BFS(graph []Vertex, rootIndex, rootRelativeIndex int) {
	var queue []int
	queue = append(queue,rootIndex)
	visited := make([]bool, len(graph))

	for len(queue) != 0 {
		index := queue[0]
		queue = queue[1 : ]
		visited[index] = true
		for _, uIndex := range graph[index].neighbors {
			if visited[uIndex] == true {
				continue
			}
			visited[uIndex] = true
			graph[uIndex].distance[rootRelativeIndex] = graph[index].distance[rootRelativeIndex] + 1
			queue = append(queue,uIndex)
		}
	}
}

func main() {
	var n, m int
	var graph []Vertex
	input.Scanf("%d \n %d", &n, &m)
	for i := 0; i < n; i++ {
		var ver Vertex
		ver.neighbors = make([]int, 0)
		ver.distance = make([]int, 0)
		graph = append(graph, ver)
	}
	for i := 0; i < m; i++ {
		var indexA, indexB int
		input.Scanf("%d %d", &indexA, &indexB)
		graph[indexA].neighbors = append(graph[indexA].neighbors, indexB)
		graph[indexB].neighbors = append(graph[indexB].neighbors, indexA)
	}
	var k int
	input.Scanf("%d", &k)

	for i := 0; i < k; i++ {
		var v int
		input.Scanf("%d", &v)
		for j := 0; j < n; j++ {
			graph[j].distance = append(graph[j].distance, n)
		}
		BFS(graph, v, i)
	}
	//for i := 0; i < m; i++ {fmt.Println(graph[i])}
	count := 0
	for i := 0; i < n; i++ {
		equal := true
		for j := 1; j < k; j++ {
			if graph[i].distance[j] != graph[i].distance[j - 1] || graph[i].distance[j] == n {
				equal = false
				break
			}
		}
		if equal {
			fmt.Printf("%d ", i)
			count ++
		}
	}
	if count == 0 {
		fmt.Println("-")
	}
	//fmt.Printf("%d : len = %d\n", i, graph[i].distance[0])
}
