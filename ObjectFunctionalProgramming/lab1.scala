val reverseP: (List[Int], Int => Boolean) => List[Int] = 
	(x, pred) => 
	if (x.length == 0) List()
	else (if (pred(x.head)) reverseP(x.tail, pred) :+ x.head
	else reverseP(x.tail, pred))


object Reverser {
	def main(args: Array[String]) = {
		println(reverseP(List(), (x: Int) => x % 2 == 0))
	}
}

/*
Простой вариант для REPL
val reverseP: (List[Int], Int => Boolean) => List[Int] = 
{
	case (List(), p) => List() 
	case (x :: xs, p) if (p(x)) => reverseP(xs, p) ::: List(x) 
	case (x :: xs, p) => reverseP(xs,p) 
}
*/