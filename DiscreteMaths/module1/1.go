package main
import "fmt"
func pow10(a, b int64) int64 {
	ch := a
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
func main() {
var (
	x int64
	pa int64
	now int64
)
fmt.Scanf("%d", &x)
pa = 1
for ; x - pa * 9 * pow10(10, (pa - 1)) > 0 ; {
    x -= pa * 9 * pow10(10, (pa - 1))
    pa += 1
} 
now = pow10(10, (pa - 1)) + (x/pa)
var i int64
for i = 0; i < (pa - 1 - (x % pa)); i++ {
	now = (now / 10)
}
now %= 10
fmt.Print(now)
}