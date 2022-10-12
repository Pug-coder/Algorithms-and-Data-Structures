package main
import "fmt"
import "github.com/skorobogatov/input"
import "strconv"
type peak struct{
//    id int;
    name string;
    comp int;
    list []*peak;
    T1 int;
    low int;
    value int;
    color int;
    sum int;
    marker bool;
    list_sum []*peak;
    out []*peak;
  //  deg int;
}

func QuickSort(data []*peak, l int, r int, less func(i, j int) bool, swap func(i, j int)){
    if r == l {
        return
    }

    i, j := l, r
    op := (l+r)/2
    for i <= j{
        for less(i, op) == true {i++}
        for less(op, j) == true {j--}
        if i < j{
            swap(i, j)
            i++
            j--
        }else{
            break
        }
    }
    QuickSort(data, l, j, less, swap)
    QuickSort(data, j+1, r, less, swap)
}



var time = 1
var count = 1
var index = 0
var stack []*peak
func Tarjan(l []*peak, stack []*peak){
  for _, v := range l{
    if v.T1 == 0{
      VisitVertex_Tarjan(l, v, stack)
    }
  }
}

func VisitVertex_Tarjan(l []*peak, v *peak, stack []*peak){
    v.T1 = time
    v.low = time
    time++
    stack[index] = v
    index++
    for _, i := range v.list{
      u := i
      if u.T1 == 0{
        VisitVertex_Tarjan(l, u, stack)
      }
      if u.comp == 0 && v.low > u.low{
        v.low = u.low
      }
    }
    if v.T1 == v.low{
      index--
      u := stack[index]
      //fmt.Println(u.id)
      u.comp = count
      for u != v{
        index--
        u = stack[index]
        u.comp = count
        //fmt.Printf("%d %d\n",u.id, v.id)
      }
      //fmt.Println("lol")
      count++
    }
}

func dfs(data_name []*peak){
  queue := make([]*peak, len(data_name))
  indexin := 0
  for _, w := range data_name{
  //  w := data_name[0]
    if !w.marker && w.color == -1{
      w.marker = true
      queue[indexin] = w
      indexin++
      //w.list_sum = append(w.list_sum, w)
      //w.sum = w.value
      for indexin > 0{
        indexin--
        v := queue[indexin]
        for _, u := range v.list{
          if ! u.marker{
            u.marker = true
            queue[indexin] = u
            indexin++
            u.color = -1
          }
        }
      }
    }
  }
}
func in(t *peak, out []*peak)(bool){
  for _, i := range out{
    if i == t{
      return true
    }
  }
  return false
}
func main() {
    //fmt.Println("Hello World")
    symbol := ';'
    data_name := make([]*peak, 0)
  //  data_minut := make([]int, 0)
    for symbol == ';'{
      str := input.Gets()
      for str[len(str)-1] == '<'{
        str += input.Gets()
      }
    //  index := 0
      name := &peak{}
      i := 0
      symbol = '.'
      for i < len(str){
        //fmt.Println(i)
        if str[i] == '('{
          //data_name = append(data_name, str[index:i])
        //  minut := ""
          j := i+1
          for j = i+1; str[j] != ')'; j++{
            //minut = ""

          }
          //data_minut = append(data_minut, str[i+1:j])
          name.value, _ = strconv.Atoi(str[i+1: j])
          i = j
        }else if (str[i] >= 'a' && str[i] <= 'z') || (str[i] >= 'A' && str[i] <= 'Z'){
          j := i
          for j < len(str) && str[j] != ';' && str[j] != '(' && str[j] != ' '{
            j++
          }
          //name
          n := str[i:j]
          flag := 0
          var k *peak
          for _, chek := range data_name{
            if chek.name == n{
              flag = 1
              k = chek
              break
            }
          }
          if flag == 0{
            k = &peak{
              name: n,
              comp: 0,
              T1: 0,
              color: 0,
              sum: 0,
              marker: false,
            }
            data_name = append(data_name, k)
          }
          if name != nil{
          //  fmt.Println("lol")
            if name.name == k.name{
              name.color = -1
            }
            flag = 1
            for _, h := range name.list{
              if h == k{
                flag = 0
              }
            }
            if flag == 1{
              name.list = append(name.list, k)
            }
          }
          name = k
          i = j
        }else if str[i] == ' ' || str[i] == '<'{
          i++
        }else if str[i] == ';'{
          symbol = ';'
          i++
        }else{
          i++
        }
      }
      //fmt.Println(symbol)
    }



    stack = make([]*peak, len(data_name))
//    indexin = 0
//    indexout = 0
    Tarjan(data_name, stack)
    inf := make([]int, count)

    for _, i := range data_name{
      inf[i.comp - 1]++
    }
    for _, i := range data_name{
      if inf[i.comp - 1] >= 2{
        i.color = -1
        for _, j := range i.list{
          j.color = -1
        }
      }
    }
    dfs(data_name)
    queue := make([]*peak, len(data_name))
    indexin := 0
    for _, w := range data_name{
    //  w := data_name[0]
      if !w.marker && w.color != -1{
        w.marker = true
        queue[indexin] = w
        indexin++
        w.list_sum = append(w.list_sum, w)
        w.sum = w.value
        for indexin > 0{
          indexin--
          v := queue[indexin]
          for _, u := range v.list{
            if u.color != -1 && (! u.marker || v.sum + u.value > u.sum){
              u.marker = true
              queue[indexin] = u
              indexin++
              u.sum = v.sum + u.value
              u.list_sum = make([]*peak, 0)
              for _, k := range v.list_sum{
                u.list_sum = append(u.list_sum, k)
              }
              u.list_sum = append(u.list_sum, u)
              u.out = make([]*peak, 0)
              u.out = append(u.out, v)
            }else if u.color != -1 && v.sum + u.value == u.sum{
              u.marker = true
              queue[indexin] = u
              indexin++
              //u.list_sum = v.list_sum
              u.out = append(u.out, v)
              for _, k := range v.list_sum{
                u.list_sum = append(u.list_sum, k)
              }
            }
          }
        }
      }
    }
    /*
    for _, i := range data_name{
      if i.color != -1 && i.marker == false{
        i.sum = i.value
        i.list_sum = append(i.list_sum, i)
      }
    }*/

    if len(data_name) > 1{
       QuickSort(data_name, 0, len(data_name) - 1,
            func (i, j int) bool {
                return data_name[i].sum > data_name[j].sum},
           func (i, j int) { data_name[i], data_name[j] = data_name[j], data_name[i]},
        )
   }
   max := data_name[0].sum
   for _, i := range data_name{
      if i.sum == max{
        for _, k := range i.list_sum{
          k.color = 1
        }
      }else{
        break
      }
   }

   if len(data_name) > 1{
      QuickSort(data_name, 0, len(data_name) - 1,
           func (i, j int) bool {
               return data_name[i].name < data_name[j].name},
          func (i, j int) { data_name[i], data_name[j] = data_name[j], data_name[i]},
       )
  }
   fmt.Println("digraph {")
   for _, i := range data_name{
     if i.color == 1{
       a := i.name
       fmt.Printf(`  %s [label = "%s(%d)", color = red]`, a, a, i.value)
       fmt.Printf("\n")
     }else if i.color == -1{
       a := i.name
       fmt.Printf(`  %s [label = "%s(%d)", color = blue]`, a, a, i.value)
       fmt.Printf("\n")
     }else{
       a := i.name
       fmt.Printf(`  %s [label = "%s(%d)"]`, a, a, i.value)
       fmt.Printf("\n")
     }
   }
   for _, t := range data_name{

     if len(t.list) > 1{
        QuickSort(t.list, 0, len(t.list) - 1,
             func (i, j int) bool {
                 return t.list[i].name < t.list[j].name},
            func (i, j int) { t.list[i], t.list[j] = t.list[j], t.list[i]},
         )
     }
     for _, i := range t.list{
      if t.color == 1 && i.color == 1 && in(t, i.out){
        //t in i.out
        fmt.Printf("  %s -> %s [color = red]\n", t.name, i.name)
      }else if t.color == -1 && i.color == -1{
        fmt.Printf("  %s -> %s [color = blue]\n", t.name, i.name)
      }else {
        fmt.Printf("  %s -> %s\n", t.name, i.name)
      }
     }
   }
   fmt.Println("}")
}
