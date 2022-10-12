package main

import (
	"fmt"
	"github.com/skorobogatov/input"
	"math"
	"sort"
)
func pow(a float64, b int64) int64 {
	ch := int64(a)
	var p int64
	p = 1
	for ; b > 0 ; {
		if b & 1 != 0 {
			p *= ch
		}
		ch *= ch
		b >>= 1
	}
	return p
}

type Edge struct {
	IndexA, IndexB int
	Weight float64
}
type EdgesAreSorted []Edge

type Point2D struct {
	X, Y float64
}
func getAbs(n float64) float64{
	if n < 0 {return -n}
	return n
}

func sortedData(data EdgesAreSorted){
	sort.Slice(data, func(i, j int) bool {
		if data[i].Weight < data[j].Weight {
			return true
		} else {return false}
	})
}

func GetDistanceX(point Point2D,another Point2D) float64 {
	legA := getAbs(point.X - another.X)
	return float64(pow(legA,2))
}
func GetDistanceY(point Point2D,another Point2D) float64 {
	legB := getAbs(point.Y - another.Y)
	return float64(pow(legB,2))
}
func calcDistance(point Point2D, another Point2D) float64{
	a := GetDistanceY(point ,another)
	b := GetDistanceX(point ,another)
	return math.Sqrt(a + b)
}
func Kruskal(edges []Edge, ids []int)  float64{
	summaryWeight := 0.0
	counter := 0
	for i := 0; counter < len(ids) - 1; i++ {
		indexA, indexB := edges[i].IndexA, edges[i].IndexB
		if ids[indexA] != ids[indexB] {
			counter++
			summaryWeight += edges[i].Weight
			oldId, newId := ids[indexB], ids[indexA]
			for j := 0; j < len(ids); j++ {
				if ids[j] == oldId {
					ids[j] = newId
				}
			}
		}
	}
	return summaryWeight
}
func insertionSort(data []Edge) {
	for i := 0; i < len(data); i++ {
		temp := data[i]
		j := i - 1
		for ; j >= 0 && data[j].Weight > temp.Weight; j-- {
			data[j+1] = data[j]
		}
		data[j+1] = temp
	}
}
func MSTKruscal(edges []Edge, ids []int) {
	sortedData(edges)
	fmt.Printf("%.2f\n", Kruskal(edges, ids))
}
func main() {
	var n int
	input.Scanf("%d",&n)
	points := make([]Point2D, n)
	for i := 0; i < n; i++ {
		var x, y float64
		input.Scanf("%f %f", &x, &y)
		points[i] = Point2D{x, y}
	}
	edges := make([]Edge, (n - 1) * n / 2)
	k := 0
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			edges[k] = Edge{i, j, calcDistance(points[i],points[j])}
			k++
		}
	}
	ids := make([]int, n)
	for i := range ids {
		ids[i] = i
	}
	MSTKruscal(edges,ids)
}