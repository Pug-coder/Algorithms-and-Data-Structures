package main 
import (
	"fmt"
)
type edge struct {
	mark bool
	color string
	u int 
	v int
}
//func DFS()
func main() {
	var (
		n int //количество вершин
		m int //количество ребер
		a int
		b int
		graph [][]int
		edges []edge
	)
	fmt.Scanf("%d \n %d", &n, &m)
	graph = make([][]int, n)
	edges = make([]edge, 0)
	// Матрица n x n
	for i := 0; i < n; i++ {
		graph[i] = make([]int,0)
	}
	for i := 0; i < m; i++ {
		fmt.Scanf("%d %d", &a, &b)
		edges = append(edges, edge{false,"white",a,b})
		graph[a] = append(graph[a], b)
		//graph[b] = append(graph[b], a)
	}
	for i := 0; i < n; i ++ {
		fmt.Println(graph[i])
	}
	fmt.Println("edges:")
	for i := 0; i < m; i++ {
		fmt.Println(edges[i])
	}

}