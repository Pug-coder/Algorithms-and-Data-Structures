package main

import (
	"fmt"
	"sort"
)

type Vertex struct {
	Edges        []*Vertex
	Group, Index int
	Visited      bool
	neighbors []int
}

func sortedData(data []*Vertex){
	if len(data) > 1{
		QuickSort(len(data) ,
			func (i, j int) bool {
				return data[i].Index < data[j].Index},
			func (i, j int) { data[i], data[j] = data[j], data[i]},
		)
	}
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
type Division struct {
	Balance           int
	LeftSideVertices  map[*Vertex]bool
	RightSideVertices map[*Vertex]bool
}

type Set struct {
	Storage map[*Vertex]bool
}

func NewSet() *Set {
	return &Set{map[*Vertex]bool{}}
}

func (set *Set) Add(value *Vertex) {
	set.Storage[value] = true
}

func (set *Set) Size() int {
	return len(set.Storage)
}

func (set *Set) AsSlice() []*Vertex {
	values := make([]*Vertex, len(set.Storage))
	i := 0
	for key := range set.Storage {
		values[i] = key
		i++
	}
	return values
}

func (set *Set) Compare(another *Set) bool {
	if set.Size() != another.Size() {
		return set.Size() < another.Size()
	}
	sliceA, sliceB := set.AsSlice(), another.AsSlice()
	sortedData(sliceA)
	sortedData(sliceB)
	for i := 0; i < len(sliceA); i++ {
		if sliceA[i].Index < sliceB[i].Index {
			return true
		}
		if sliceA[i].Index > sliceB[i].Index {
			return false
		}
	}
	return false
}
func min(a, b int) int  {
	if a < b {
		return a
	}
	return b
}
func DFSInner(vertex *Vertex,component *Division) {
	vertex.Visited = true
	if vertex.Group < 0 {
		component.LeftSideVertices[vertex] = true
	} else {
		component.RightSideVertices[vertex] = true
	}
	component.Balance += vertex.Group
	for _, u := range vertex.Edges {
		if vertex.Group*u.Group == 1 {
			panic("no solution")
		}
		if !u.Visited {
			u.Group = -vertex.Group
			DFSInner(u,component)
		}
	}
}
func DFS(start *Vertex, component *Division) (result bool) {
	defer func() {
		if x := recover(); x != nil {
			result = false
			fmt.Printf("No solution")
		}
	}()

	DFSInner(start,component)

	return true
}
func getAbs(n int) int{
	if n < 0 {return -n}
	return n
}
func Input(n int) []*Vertex{
	var graph []*Vertex
	for i := 0; i < n; i++ {
		var ver Vertex
		ver.neighbors = make([]int, 0)
		ver.Group = 0
		ver.Visited = false
		graph = append(graph, &ver)
		graph[i] = &Vertex{Index: i}
	}
	return graph
}
func generateMasks(n int) [][]bool {
	var masks [][]bool
	var generateMasksInner func([]bool, int)
	generateMasksInner = func(mask []bool, i int) {
		if i == n {
			masks = append(masks, mask)
			return
		}
		maskWithTrueEnding := make([]bool, len(mask)+1)
		maskWithFalseEnding := make([]bool, len(mask)+1)
		for j, value := range mask {
			maskWithTrueEnding[j] = value
			maskWithFalseEnding[j] = value
		}
		maskWithTrueEnding[len(mask)] = true
		maskWithFalseEnding[len(mask)] = false
		generateMasksInner(maskWithTrueEnding, i+1)
		generateMasksInner(maskWithFalseEnding, i+1)
	}
	generateMasksInner([]bool{}, 0)
	return masks
}
func main() {
	var n int
	fmt.Scanf("%d", &n)
	graph := Input(n)
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			var connection string
			fmt.Scanf("%s", &connection)
			if connection[0] == '+' {
				graph[i].Edges = append(graph[i].Edges, graph[j])
			}
		}
	}
	var components []*Division
	for _, vertex := range graph {
		if !vertex.Visited {
			vertex.Group = 1
			component := &Division{LeftSideVertices: map[*Vertex]bool{}, RightSideVertices: map[*Vertex]bool{}}
			components = append(components, component)
			if !DFS(vertex, component) {return}
		}
	}
	// Generating masks
	masks := generateMasks(len(components))
	sumsOfMasks := make([]int, len(masks))
	minimalSum := n
	for i := 0; i < len(masks); i++ {
		sum := 0
		for j := 0; j < len(components); j++ {
			if !masks[i][j] {
				sum -= components[j].Balance
			} else {
				sum += components[j].Balance
			}
		}
		sum = getAbs(sum)
		if sum < minimalSum {
			minimalSum = sum
		}
		sumsOfMasks[i] = sum
	}
	minimals := NewSet()
	for i := 0; i < len(masks); i++ {
		if sumsOfMasks[i] == minimalSum {
			mergedSet := NewSet()
			for j := 0; j < len(components); j++ {
				subset := components[j].RightSideVertices
				if masks[i][j] {
					subset = components[j].LeftSideVertices
				}
				for key := range subset {
					mergedSet.Add(key)
				}
			}
			keys := make([]int, mergedSet.Size())
			i := 0
			for k, _ := range mergedSet.Storage {
				keys[i] = k.Group
				i++
			}
			sort.Ints(keys)
			if minimals.Size() == 0 || mergedSet.Compare(minimals) {
				minimals = mergedSet
			}
		}
	}
	minimalsSlice := minimals.AsSlice()
	sortedData(minimalsSlice)
	s := " "
	for _, vertex := range minimalsSlice {
		fmt.Print(vertex.Index + 1, s)
	}
	fmt.Println("")
}