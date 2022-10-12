package main

import (
	"fmt"
	"github.com/skorobogatov/input"
)

type Edge struct {
	firstIndex, secondIndex int
	color bool
}

var (
	
	marked      []bool
	comp        []int
	graph       [][]int
	vertexCount int
	edgeCount   int
	maxComp     []int
	Edges       []Edge
)

func findMinVertex(component []int) int {
	min := component[0]
	for i := 1; i < len(component); i++ {
		if component[i] < min {
			min = component[i]
		}
	}
	return min
}

func countEdgesInComponent(component []int) int {
	result := 0
	for i := 0; i < len(component); i++ {
		result += len(graph[component[i]])
	}
	return result / 2
}

/*func dfs(v int) {
	var to int
	used[v] = true
	comp = append(comp, v)
	for i := 0; i < len(graph[v]); i++ {
		to = graph[v][i]
		if ! used[to] {
			dfs(to)
		}
	}

}*/
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
func findComps() {
	//for i := 0; i < vertexCount; i++ {
		//if !visited[i] {
			comp = nil
			dodfs(graph)
		//}
		if len(comp) > len(maxComp) {
			maxComp = comp
		} else if len(comp) == len(maxComp) {
			if countEdgesInComponent(comp) > countEdgesInComponent(maxComp) {
				maxComp = comp
			} else if countEdgesInComponent(comp) == countEdgesInComponent(maxComp) {
				if findMinVertex(comp) < findMinVertex(maxComp) {
					maxComp = comp
				}
			}
		}
	}
//}

func PrintPeaks() {
	fmt.Printf("graph {\n")
	for i := 0; i < vertexCount; i++ {
		if marked[i] == true {
			fmt.Printf("\t%d%s\n", i, " [color = red]")
		} else {
			fmt.Printf("\t%d\n", i)
		}
	}
}

func PrintGraph() {
	for i := 0; i < edgeCount; i++ {
		if Edges[i].color == true {
			fmt.Printf("\t%d -- %d%s\n", Edges[i].firstIndex, Edges[i].secondIndex, " [color = red]")
		} else {
			fmt.Printf("\t%d -- %d\n",Edges[i].firstIndex, Edges[i].secondIndex)
		}
	}
}

func main() {
	var a, b, number int
	input.Scanf("%d \n %d", &vertexCount, &edgeCount)

	marked = make([]bool, vertexCount)
	visited = make([]bool, vertexCount)
	graph = make([][]int, vertexCount)
	Edges = make([]Edge, 0)

	for i := 0; i < vertexCount; i++ {
		graph[i] = make([]int, 0)
	} 

	//считываем все рёбра и создаём массив структур, состоящий из этих рёбер
	for i := 0; i < edgeCount; i++ {
		input.Scanf("%d %d", &a, &b)
		Edges = append(Edges, Edge{a, b, false})
		graph[a] = append(graph[a], b)
		//graph[b] = append(graph[b], a)

	}

	findComps()
	//помечаем вершины из максимальной компоненты красным цветом
	for i := 0; i < len(maxComp); i++ {
		marked[maxComp[i]] = true
	}
	//помечаем рёбра, входящие в максимальную компоненту красным цветом
	for i := 0; i < edgeCount; i++ {
		number = Edges[i].firstIndex
		if marked[number] == true {
			Edges[i].color = true
		}
	}

	PrintPeaks()
	PrintGraph()
	fmt.Printf("}")
}