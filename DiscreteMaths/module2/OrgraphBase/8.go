package main

import (
	"fmt"
)

type Vertex struct {
	connections []int
	used bool
	visited bool
	comp int
	ins int
	min_v int // Used for condensation
	T1           int
	Low          int
}
func refresh(graph []Vertex) {
	for i := 0; i < len(graph); i++ {
		graph[i].used = false
	}
}
func tarjan(graph []Vertex) int {
	var stack []int
	var time, count = 1, 1

	var visitVertex func(int)
	visitVertex = func(index int) {
		graph[index].T1 = time
		graph[index].Low = time
		time++

		stack = append(stack, index)
		for _, uIndex := range graph[index].connections {
			if graph[uIndex].T1 == 0 {
				visitVertex(uIndex)
			}

			if graph[uIndex].comp == 0 && graph[index].Low > graph[uIndex].Low {
				graph[index].Low = graph[uIndex].Low
			}
		}
		if graph[index].T1 == graph[index].Low {
			var vIndex int
			for {
				vIndex = stack[len(stack)-1]
				stack = stack[:len(stack)-1]
				graph[vIndex].comp = count
				if index == vIndex {
					break
				}
			}
			count++
		}
	}
	for i := 0; i < len(graph); i++ {
		if graph[i].T1 == 0 {
			visitVertex(i)
		}
	}
	return count
}
func topsort(graph []Vertex, v int, order *[]int) {
	graph[v].used = true
	for i := 0; i < len(graph[v].connections); i++ {
		to := graph[v].connections[i]
		if graph[to].used { continue }
		topsort(graph, to, order)
	}
	graph[v].visited = true
	*order = append(*order, v)
}

func unite(graph []Vertex, v int, cond []Vertex, comp int) {
	graph[v].used = true
	graph[v].comp = comp
	if v < cond[comp].min_v {
		cond[comp].min_v = v
	}
	for i := 0; i < len(graph[v].connections); i++ {
		to := graph[v].connections[i]
		if graph[to].used {
			if graph[to].comp != comp {
				cond[comp].connections = append(cond[comp].connections, graph[to].comp)
				cond[graph[to].comp].ins ++
			}
			continue
		}
		unite(graph, to, cond, comp)
	}
}

func main() {
	var n, m int
	fmt.Scanf("%d \n %d", &n, &m)
	graph := make([]Vertex, n)
	for i := 0; i < m; i++ {
		var indexA, indexB int
		fmt.Scanf("%d %d", &indexA, &indexB)
		graph[indexA].connections = append(graph[indexA].connections, indexB)
	}
	count := tarjan(graph)
	order := make([]int, 0)
	for i := 0; i < len(graph); i++ {
		if !graph[i].used {
			topsort(graph, i, &order)
		}
	}
	refresh(graph)
	cond := make([]Vertex, 0)
	for i := 0; i < len(order); i++ {
		v := order[i]
		if !graph[v].used {
			var ver Vertex
			ver.connections = make([]int, 0)
			ver.min_v = 100000
			cond = append(cond, ver)
			unite(graph, v, cond, len(cond) - 1)
		}
	}
	condensationsMinimalIndices := make([]int, count)
	useCondensationInBase := make([]bool, count)
	for i := 0; i < count; i++ {
		useCondensationInBase[i] = true
		condensationsMinimalIndices[i] = -1
	}
	for _, vertex := range graph {
		for _, uIndex := range vertex.connections {
			uComp := graph[uIndex].comp
			if vertex.comp != uComp {
				useCondensationInBase[uComp] = false
			}
		}
	}

	for i := 0; i < len(cond); i++ {
		if useCondensationInBase[i] == true {
			fmt.Print(cond[i].min_v, " ")
		}
	}
	fmt.Println()
}